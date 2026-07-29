import fitz
import glob
import os

pdfs = glob.glob('natgeo_collection/pdfs/*.pdf')
img_dir = 'natgeo_collection/images'
os.makedirs(img_dir, exist_ok=True)

print(f"Checking cover images for {len(pdfs)} PDFs...")
for p in pdfs:
    aid = os.path.splitext(os.path.basename(p))[0]
    out_cover = f"{img_dir}/{aid}_cover.jpg"
    if not os.path.exists(out_cover) or os.path.getsize(out_cover) == 0:
        print(f"Generating cover for {aid}...")
        try:
            doc = fitz.open(p)
            page = doc[0]
            pix = page.get_pixmap(dpi=120)
            pix.save(out_cover)
            doc.close()
            print(f"  -> Saved {out_cover} ({os.path.getsize(out_cover)} bytes)")
        except Exception as e:
            print(f"  -> Failed for {aid}: {e}")

print("Cover image generation complete.")
