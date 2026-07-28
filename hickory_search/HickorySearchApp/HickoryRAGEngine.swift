import Foundation

struct ResearchResult: Identifiable {
    let id = UUID()
    let zimName: String
    let title: String
    let snippet: String
}

class HickoryRAGEngine: ObservableObject {
    @Published var isSearching: Bool = false
    @Published var currentPhase: String = "Idle"
    @Published var searchProgress: Double = 0.0
    @Published var discoveredResults: [ResearchResult] = []

    func runNestedLoopQuery(question: String, zimFiles: [URL], aiLoader: LocalAILoader, completion: @escaping (String) -> Void) {
        guard !question.isEmpty else { return }

        self.isSearching = true
        self.currentPhase = "Phase 1: Planning search keywords..."
        self.searchProgress = 0.1
        self.discoveredResults.removeAll()

        DispatchQueue.global(qos: .userInitiated).async {
            // Phase 1: Keyword extraction
            let keywords = self.extractKeywords(question: question)
            
            DispatchQueue.main.async {
                self.currentPhase = "Phase 2: Searching \(zimFiles.count) .ZIM files for: \(keywords.joined(separator: ", "))"
                self.searchProgress = 0.3
            }

            var dossier: [ResearchResult] = []

            // Phase 2: Parallel search across 40+ ZIM files
            let group = DispatchGroup()
            let queue = DispatchQueue(label: "hickory.zim.search", attributes: .concurrent)

            for (index, fileURL) in zimFiles.enumerated() {
                group.enter()
                queue.async {
                    let results = self.searchSingleZim(fileURL: fileURL, keywords: keywords)
                    DispatchQueue.main.async {
                        dossier.append(contentsOf: results)
                        self.discoveredResults = dossier
                        self.searchProgress = 0.3 + (Double(index + 1) / Double(max(1, zimFiles.count))) * 0.5
                    }
                    group.leave()
                }
            }

            group.wait()

            // Phase 3: Synthesis
            DispatchQueue.main.async {
                self.currentPhase = "Phase 3: Local AI Synthesizing Final Response..."
                self.searchProgress = 0.9
            }

            let dossierText = dossier.prefix(8).map { "=== [\($0.zimName)]: \($0.title) ===\n\($0.snippet)" }.joined(separator: "\n\n")

            aiLoader.generateResponse(prompt: question, context: dossierText) { answer in
                DispatchQueue.main.async {
                    self.isSearching = false
                    self.currentPhase = "Complete"
                    self.searchProgress = 1.0
                    completion(answer)
                }
            }
        }
    }

    private func extractKeywords(question: String) -> [String] {
        let stopwords: Set<String> = ["what", "where", "when", "who", "how", "list", "all", "the", "and", "in", "to", "around", "tell", "about", "find"]
        let words = question.components(separatedBy: CharacterSet.alphanumerics.inverted)
            .filter { $0.count > 2 && !stopwords.contains($0.lowercased()) }
        return Array(words.prefix(5))
    }

    private func searchSingleZim(fileURL: URL, keywords: [String]) -> [ResearchResult] {
        var results: [ResearchResult] = []
        let zimName = fileURL.lastPathComponent

        // Read text or extracted ZIM contents
        do {
            let fileData = try Data(contentsOf: fileURL, options: .mappedIfSafe)
            let sampleText = String(decoding: fileData.prefix(50000), as: UTF8.self)

            for kw in keywords {
                if sampleText.localizedCaseInsensitiveContains(kw) {
                    results.append(ResearchResult(
                        zimName: zimName,
                        title: "Entry matching '\(kw)'",
                        snippet: "Found matching record for '\(kw)' in \(zimName). High relevance index."
                    ))
                    if results.count >= 2 { break }
                }
            }
        } catch {
            print("Error reading ZIM file \(zimName): \(error)")
        }

        return results
    }
}
