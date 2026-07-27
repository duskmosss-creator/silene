import os
import urllib.request

os.makedirs("content/images", exist_ok=True)
os.makedirs("natgeo_collection/images", exist_ok=True)

ia_cover_items = [
    ('westernnorthcar00arth', 'content/images/westernnorthcar00arth_cover.jpg'),
    ('historyofwataug00arth', 'content/images/historyofwataug00arth_cover.jpg'),
    ('folksongsofengli00shar', 'content/images/folksongsofengli00shar_cover.jpg'),
    ('nurserysongsfrom00shar', 'content/images/nurserysongsfrom00shar_cover.jpg'),
    ('riflemakingingre13nati', 'content/images/riflemakingingre13nati_cover.jpg'),
    ('checklistoffungi00pete', 'content/images/checklistoffungi00pete_cover.jpg'),
    ('floraofgreatsmok00whit', 'content/images/floraofgreatsmok00whit_cover.jpg'),
    ('statushistoryofm00culb', 'content/images/statushistoryofm00culb_cover.jpg'),
    ('whitetaileddeero00wath', 'content/images/whitetaileddeero00wath_cover.jpg'),
    ('carologueaccesst00hoff', 'content/images/carologueaccesst00hoff_cover.jpg'),
    ('nationalgeograph11889nati', 'natgeo_collection/images/nationalgeograph11889nati_cover.jpg'),
    ('nationalgeograph37natiuoft', 'natgeo_collection/images/nationalgeograph37natiuoft_cover.jpg'),
    ('194701to12', 'natgeo_collection/images/194701to12_cover.jpg'),
    ('194905', 'natgeo_collection/images/194905_cover.jpg'),
    ('195011', 'natgeo_collection/images/195011_cover.jpg'),
    ('195105', 'natgeo_collection/images/195105_cover.jpg'),
    ('195204', 'natgeo_collection/images/195204_cover.jpg'),
    ('195304', 'natgeo_collection/images/195304_cover.jpg'),
    ('jishankhan_hotmail_1954', 'natgeo_collection/images/jishankhan_hotmail_1954_cover.jpg')
]

print("Downloading real archival magazine and article cover page photos from Internet Archive...")
for ia_id, save_path in ia_cover_items:
    if os.path.exists(save_path) and os.path.getsize(save_path) > 500:
        print(f"Verified cover: {save_path}")
        continue
        
    url = f"https://archive.org/services/img/{ia_id}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
            if len(data) > 500:
                with open(save_path, 'wb') as f:
                    f.write(data)
                print(f"Downloaded cover: {save_path} ({len(data)} bytes)")
    except Exception as e:
        print(f"Notice downloading cover for {ia_id}: {e}")

print("Real archival cover downloading complete.")
