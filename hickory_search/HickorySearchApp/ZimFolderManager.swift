import Foundation
import UIKit
import SwiftUI

class ZimFolderManager: ObservableObject {
    @Published var selectedFolderURL: URL?
    @Published var discoveredZimFiles: [URL] = []
    @Published var discoveredModelFiles: [URL] = []
    @Published var statusMessage: String = "No folder selected. Pick your iOS Files folder containing 40+ .zim archives."

    private let bookmarkKey = "HickorySearch_FolderBookmark"

    init() {
        restorePersistedBookmark()
    }

    func loadFolder(url: URL) {
        guard url.startAccessingSecurityScopedResource() else {
            statusMessage = "Permission denied to access selected folder."
            return
        }

        defer { url.stopAccessingSecurityScopedResource() }

        self.selectedFolderURL = url
        saveBookmark(url: url)
        scanFolderContents(url: url)
    }

    private func scanFolderContents(url: URL) {
        let fileManager = FileManager.default
        do {
            let keys: [URLResourceKey] = [.nameKey, .isDirectoryKey, .fileSizeKey]
            let fileURLs = try fileManager.contentsOfDirectory(at: url, includingPropertiesForKeys: keys, options: [.skipsHiddenFiles])

            self.discoveredZimFiles = fileURLs.filter { $0.pathExtension.lowercased() == "zim" }
            self.discoveredModelFiles = fileURLs.filter { ["gguf", "bin", "mlmodel", "onnx"].contains($0.pathExtension.lowercased()) }

            statusMessage = "Loaded \(discoveredZimFiles.count) .ZIM archives and \(discoveredModelFiles.count) custom AI models."
        } catch {
            statusMessage = "Error scanning folder: \(error.localizedDescription)"
        }
    }

    private func saveBookmark(url: URL) {
        do {
            let bookmarkData = try url.bookmarkData(options: .minimalBookmark, includingResourceValuesForKeys: nil, relativeTo: nil)
            UserDefaults.standard.set(bookmarkData, forKey: bookmarkKey)
        } catch {
            print("Failed to save folder bookmark: \(error)")
        }
    }

    private func restorePersistedBookmark() {
        guard let bookmarkData = UserDefaults.standard.data(forKey: bookmarkKey) else { return }
        var isStale = false
        do {
            let url = try URL(resolvingBookmarkData: bookmarkData, options: [], relativeTo: nil, bookmarkDataIsStale: &isStale)
            if url.startAccessingSecurityScopedResource() {
                self.selectedFolderURL = url
                scanFolderContents(url: url)
                url.stopAccessingSecurityScopedResource()
            }
        } catch {
            print("Failed to restore bookmark: \(error)")
        }
    }
}

struct DocumentPickerView: UIViewControllerRepresentable {
    @ObservedObject var manager: ZimFolderManager

    func makeUIViewController(context: Context) -> UIDocumentPickerViewController {
        let picker = UIDocumentPickerViewController(forOpeningContentTypes: [.folder, .item], asCopy: false)
        picker.allowsMultipleSelection = false
        picker.delegate = context.coordinator
        return picker
    }

    func updateUIViewController(_ uiViewController: UIDocumentPickerViewController, context: Context) {}

    func makeCoordinator() -> Coordinator {
        Coordinator(self)
    }

    class Coordinator: NSObject, UIDocumentPickerDelegate {
        var parent: DocumentPickerView

        init(_ parent: DocumentPickerView) {
            self.parent = parent
        }

        func documentPicker(_ controller: UIDocumentPickerViewController, didPickDocumentsAt urls: [URL]) {
            guard let url = urls.first else { return }
            parent.manager.loadFolder(url: url)
        }
    }
}
