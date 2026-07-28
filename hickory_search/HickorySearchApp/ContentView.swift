import SwiftUI

struct ContentView: View {
    @StateObject private var folderManager = ZimFolderManager()
    @StateObject private var aiLoader = LocalAILoader()
    @StateObject private var ragEngine = HickoryRAGEngine()

    @State private var queryText: String = ""
    @State private var responseText: String = ""
    @State private var showFolderPicker: Bool = false
    @State private var showModelPicker: Bool = false

    var body: some View {
        NavigationView {
            ZStack {
                Color(red: 15/255, green: 23/255, blue: 42/255)
                    .ignoresSafeArea()

                VStack(spacing: 16) {
                    // Header Bar
                    HStack {
                        VStack(alignment: .leading, spacing: 4) {
                            Text("HICKORY SEARCH")
                                .font(.system(size: 20, weight: .bold))
                                .foregroundColor(Color(red: 56/255, green: 189/255, blue: 248/255))
                            Text("Off-Grid Multi-ZIM RAG Engine")
                                .font(.system(size: 12, weight: .medium))
                                .foregroundColor(.gray)
                        }
                        Spacer()

                        Button(action: { showFolderPicker = true }) {
                            HStack(spacing: 6) {
                                Image(systemName: "folder.badge.gearshape")
                                Text("Select Folder")
                            }
                            .font(.system(size: 13, weight: .semibold))
                            .padding(.horizontal, 12)
                            .padding(.vertical, 8)
                            .background(Color(red: 30/255, green: 41/255, blue: 59/255))
                            .foregroundColor(.white)
                            .cornerRadius(8)
                            .overlay(RoundedRectangle(cornerRadius: 8).stroke(Color.gray.opacity(0.3), lineWidth: 1))
                        }
                    }
                    .padding(.horizontal)

                    // Folder & Model Status Bar
                    VStack(alignment: .leading, spacing: 6) {
                        HStack {
                            Image(systemName: "doc.zipper")
                                .foregroundColor(Color(red: 56/255, green: 189/255, blue: 248/255))
                            Text("Active ZIM Archives: \(folderManager.discoveredZimFiles.count) files")
                                .font(.system(size: 13, weight: .semibold))
                                .foregroundColor(.white)
                            Spacer()
                        }

                        HStack {
                            Image(systemName: "cpu")
                                .foregroundColor(.green)
                            Text("AI Model: \(aiLoader.loadedModelName)")
                                .font(.system(size: 12))
                                .foregroundColor(.gray)
                            Spacer()
                        }
                    }
                    .padding(12)
                    .background(Color(red: 30/255, green: 41/255, blue: 59/255))
                    .cornerRadius(10)
                    .padding(.horizontal)

                    // Search Query Box
                    HStack {
                        TextField("Ask anything across 40+ ZIM files...", text: $queryText)
                            .padding(12)
                            .background(Color(red: 15/255, green: 23/255, blue: 42/255))
                            .foregroundColor(.white)
                            .cornerRadius(8)
                            .overlay(RoundedRectangle(cornerRadius: 8).stroke(Color.gray.opacity(0.4), lineWidth: 1))

                        Button(action: runSearch) {
                            HStack {
                                Image(systemName: "magnifyingglass")
                                Text("Search")
                            }
                            .font(.system(size: 14, weight: .bold))
                            .padding(.horizontal, 16)
                            .padding(.vertical, 12)
                            .background(Color(red: 56/255, green: 189/255, blue: 248/255))
                            .foregroundColor(Color(red: 15/255, green: 23/255, blue: 42/255))
                            .cornerRadius(8)
                        }
                        .disabled(ragEngine.isSearching)
                    }
                    .padding(.horizontal)

                    // Search Progress Indicator
                    if ragEngine.isSearching {
                        VStack(spacing: 8) {
                            ProgressView(value: ragEngine.searchProgress)
                                .accentColor(Color(red: 56/255, green: 189/255, blue: 248/255))

                            Text(ragEngine.currentPhase)
                                .font(.system(size: 12, weight: .medium))
                                .foregroundColor(Color(red: 56/255, green: 189/255, blue: 248/255))
                        }
                        .padding(.horizontal)
                    }

                    // Main Answer Display Box
                    ScrollView {
                        VStack(alignment: .leading, spacing: 12) {
                            if !responseText.isEmpty {
                                Text(responseText)
                                    .font(.system(size: 15))
                                    .foregroundColor(.white)
                                    .lineSpacing(6)
                            } else {
                                Text("Select an iOS Files folder containing your 40+ .zim archives and custom GGUF models to begin querying.")
                                    .font(.system(size: 14))
                                    .foregroundColor(.gray)
                                    .multilineTextAlignment(.center)
                                    .padding(.top, 40)
                            }
                        }
                        .padding()
                        .frame(maxWidth: .infinity, alignment: .leading)
                    }
                    .background(Color(red: 30/255, green: 41/255, blue: 59/255))
                    .cornerRadius(12)
                    .padding(.horizontal)

                    Spacer()
                }
            }
            .navigationBarHidden(true)
            .sheet(isPresented: $showFolderPicker) {
                DocumentPickerView(manager: folderManager)
            }
        }
    }

    private func runSearch() {
        guard !queryText.isEmpty else { return }
        ragEngine.runNestedLoopQuery(
            question: queryText,
            zimFiles: folderManager.discoveredZimFiles,
            aiLoader: aiLoader
        ) { answer in
            self.responseText = answer
        }
    }
}
