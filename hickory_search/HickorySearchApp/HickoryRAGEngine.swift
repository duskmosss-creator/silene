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

    // Thread-safe result accumulation
    private var pendingResults: [ResearchResult] = []
    private let resultLock = NSLock()

    func runNestedLoopQuery(question: String, zimFiles: [URL], aiLoader: LocalAILoader, completion: @escaping (String) -> Void) {
        guard !question.isEmpty else { return }

        DispatchQueue.main.async {
            self.isSearching = true
            self.currentPhase = "Phase 1: Planning search keywords..."
            self.searchProgress = 0.1
            self.discoveredResults.removeAll()
            self.pendingResults.removeAll()
        }

        DispatchQueue.global(qos: .userInitiated).async {
            let keywords = self.extractKeywords(question: question)

            DispatchQueue.main.async {
                self.currentPhase = "Phase 2: Searching \(zimFiles.count) .ZIM files for: \(keywords.joined(separator: ", "))"
                self.searchProgress = 0.3
            }

            // Phase 2: Parallel ZIM search with thread-safe result accumulation
            let group = DispatchGroup()
            let searchQueue = DispatchQueue(label: "hickory.zim.search", attributes: .concurrent)

            for (index, fileURL) in zimFiles.enumerated() {
                group.enter()
                searchQueue.async {
                    let results = self.searchSingleZim(fileURL: fileURL, keywords: keywords)

                    // Thread-safe append
                    self.resultLock.lock()
                    self.pendingResults.append(contentsOf: results)
                    let snapshot = self.pendingResults
                    self.resultLock.unlock()

                    let progress = 0.3 + (Double(index + 1) / Double(max(1, zimFiles.count))) * 0.5
                    DispatchQueue.main.async {
                        self.discoveredResults = snapshot
                        self.searchProgress = progress
                    }
                    group.leave()
                }
            }

            group.wait()

            // Phase 3: Synthesis
            let finalResults: [ResearchResult]
            self.resultLock.lock()
            finalResults = self.pendingResults
            self.resultLock.unlock()

            DispatchQueue.main.async {
                self.currentPhase = "Phase 3: Local AI Synthesizing Final Response..."
                self.searchProgress = 0.9
            }

            let dossierText = finalResults.prefix(8)
                .map { "=== [\($0.zimName)]: \($0.title) ===\n\($0.snippet)" }
                .joined(separator: "\n\n")

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
        let stopwords: Set<String> = ["what", "where", "when", "who", "how", "list", "all",
                                       "the", "and", "in", "to", "around", "tell", "about",
                                       "find", "give", "show", "can", "you"]
        let words = question.components(separatedBy: CharacterSet.alphanumerics.inverted)
            .filter { $0.count > 2 && !stopwords.contains($0.lowercased()) }
        return Array(words.prefix(5))
    }

    private func searchSingleZim(fileURL: URL, keywords: [String]) -> [ResearchResult] {
        var results: [ResearchResult] = []
        let zimName = fileURL.lastPathComponent

        do {
            // Read first 50KB of the ZIM file for header/content matching
            let fileData = try Data(contentsOf: fileURL, options: .mappedIfSafe)
            let sampleText = String(decoding: fileData.prefix(50000), as: UTF8.self)

            for kw in keywords {
                if sampleText.localizedCaseInsensitiveContains(kw) {
                    results.append(ResearchResult(
                        zimName: zimName,
                        title: "Match for '\(kw)'",
                        snippet: "Found '\(kw)' in \(zimName)."
                    ))
                    // One result per keyword per archive to avoid flooding
                    break
                }
            }
        } catch {
            // Silently skip unreadable files; they're reported on load
        }

        return results
    }
}
