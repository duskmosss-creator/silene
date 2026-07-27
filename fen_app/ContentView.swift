import SwiftUI

struct ContentView: View {
    @StateObject private var engine = FenRAGEngine()
    @State private var inputQuery: String = ""
    @State private var selectedFontSize: Double = 16.0
    @State private var isScrollLocked: Bool = false
    
    var body: some View {
        NavigationView {
            VStack(spacing: 0) {
                // Header & Reader Settings Bar
                HStack {
                    Text("fen")
                        .font(.system(size: 22, weight: .bold, design: .serif))
                        .foregroundColor(Color.green)
                    
                    Spacer()
                    
                    // Font Size Controls
                    HStack(spacing: 8) {
                        Button("S") { selectedFontSize = 14.0 }
                            .buttonStyle(.bordered)
                        Button("M") { selectedFontSize = 16.0 }
                            .buttonStyle(.borderedProminent)
                        Button("L") { selectedFontSize = 18.0 }
                            .buttonStyle(.bordered)
                        Button("XL") { selectedFontSize = 20.0 }
                            .buttonStyle(.bordered)
                    }
                    
                    // Scroll Lock Toggle
                    Button(action: { isScrollLocked.toggle() }) {
                        Image(systemName: isScrollLocked ? "lock.fill" : "lock.open.fill")
                            .foregroundColor(isScrollLocked ? .red : .gray)
                    }
                    .padding(.leading, 8)
                }
                .padding()
                .background(Color(uiColor: .secondarySystemBackground))
                
                // Scrollable Response & ZIM Reference View
                ScrollViewReader { proxy in
                    ScrollView {
                        VStack(alignment: .leading, spacing: 16) {
                            if !engine.responseText.isEmpty {
                                Text(engine.responseText)
                                    .font(.system(size: selectedFontSize))
                                    .padding()
                                    .background(Color(uiColor: .systemBackground))
                                    .cornerRadius(10)
                                    .shadow(radius: 1)
                                
                                Text("ZIM Citations & References")
                                    .font(.headline)
                                    .padding(.top, 8)
                                
                                ForEach(engine.references) { item in
                                    VStack(alignment: .leading, spacing: 4) {
                                        Text(item.title)
                                            .font(.subheadline.bold())
                                            .foregroundColor(.blue)
                                        Text(item.snippet)
                                            .font(.caption)
                                            .foregroundColor(.secondary)
                                        Text("Source: \(item.zimSource)")
                                            .font(.caption2)
                                            .foregroundColor(.gray)
                                    }
                                    .padding(10)
                                    .frame(maxWidth: .infinity, alignment: .leading)
                                    .background(Color(uiColor: .tertiarySystemBackground))
                                    .cornerRadius(8)
                                }
                            } else {
                                Text("Query offline ZIM archives via local VLM & embedding models.")
                                    .font(.subheadline)
                                    .foregroundColor(.secondary)
                                    .padding()
                            }
                        }
                        .padding()
                    }
                    .disabled(isScrollLocked)
                }
                
                // Input Bar
                HStack {
                    TextField("Ask fen about Appalachian trails, flora, weather...", text: $inputQuery)
                        .textFieldStyle(.roundedBorder)
                    
                    Button(action: {
                        Task {
                            await engine.query(userPrompt: inputQuery)
                        }
                    }) {
                        Image(systemName: "arrow.up.circle.fill")
                            .font(.title2)
                    }
                    .disabled(inputQuery.trimmingCharacters(in: .whitespaces).isEmpty || engine.isProcessing)
                }
                .padding()
                .background(Color(uiColor: .systemBackground))
            }
            .navigationTitle("fen :: Mobile ZIM AI")
            .navigationBarTitleDisplayMode(.inline)
        }
    }
}
