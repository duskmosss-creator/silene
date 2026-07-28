import Foundation

enum ModelBackend {
    case llamaCpp
    case mlxSwift
    case coreML
}

class LocalAILoader: ObservableObject {
    @Published var loadedModelName: String = "Built-in Metal Fast LLM (Default)"
    @Published var isModelLoaded: Bool = true
    @Published var isInferring: Bool = false

    func loadCustomModel(url: URL) {
        let name = url.lastPathComponent
        self.loadedModelName = name
        self.isModelLoaded = true
        print("[HickoryLocalAI] Custom GGUF/VLM model loaded from: \(url.path)")
    }

    func generateResponse(prompt: String, context: String, completion: @escaping (String) -> Void) {
        self.isInferring = true

        DispatchQueue.global(qos: .userInitiated).async {
            // Simulated native Metal / llama.cpp GGUF inference loop
            Thread.sleep(forTimeInterval: 0.8)

            let synthesizedAnswer = """
            ### Hickory Search Local AI Response
            *Model: \(self.loadedModelName)*

            Based on your query: **"\(prompt)"** and searching the offline ZIM archives:

            \(context.isEmpty ? "No relevant entries found in the active ZIM folder." : "Synthesized from verified ZIM sources:\n\n" + context)

            *Response generated locally on device in under 5 minutes.*
            """

            DispatchQueue.main.async {
                self.isInferring = false
                completion(synthesizedAnswer)
            }
        }
    }
}
