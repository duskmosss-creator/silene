from libzim.reader import Archive

z = Archive(r'c:\wikipedia\custom zim\National_Geographic_Appalachian_Collection.zim')

idx = z.get_entry_by_path('index.html')
item = idx.get_item()
print('Size:', item.size)

# Use .content property
content_bytes = bytes(item.content)
content = content_bytes.decode('utf-8', errors='replace')
print('Content length:', len(content))
print()
print(content[:1500])

with open(r'c:\wikipedia\custom zim\extracted_index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("\nSaved to extracted_index.html")
