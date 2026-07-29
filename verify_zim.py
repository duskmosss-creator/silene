from libzim.reader import Archive
z = Archive('National_Geographic_Appalachian_Collection.zim')
print('Entry count:', z.entry_count)
print('Main path:', z.main_entry.get_item().path)
idx = z.get_entry_by_path('index.html')
item = idx.get_item()
content = bytes(item.content).decode('utf-8', errors='replace')
print('index.html size in ZIM:', len(content), 'bytes')
print('Static cards (magazine-card):', content.count('magazine-card'))
print('Has cardGrid:', 'cardGrid' in content)
pos = content.find('cardGrid')
print()
print('cardGrid area:')
print(content[pos:pos+400])

with open('verify_zim_index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('\nSaved full index to verify_zim_index.html')
