import fitz
import os
import io
import glob
from PIL import Image

natgeo_dir = 'natgeo_collection'
orig_dir = f'{natgeo_dir}/pdfs_original'
new_dir = f'{natgeo_dir}/pdfs'

os.makedirs(new_dir, exist_ok=True)
if not os.path.exists(orig_dir):
    print("WARNING: pdfs_original does not exist. Backing up pdfs...")
    os.rename(new_dir, orig_dir)
    os.makedirs(new_dir, exist_ok=True)

def compress_pdf(input_path, output_path, quality=60):
    try:
        doc = fitz.open(input_path)
        for i in range(len(doc)):
            page = doc[i]
            image_list = page.get_images(full=True)
            for img in image_list:
                xref = img[0]
                try:
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    
                    image = Image.open(io.BytesIO(image_bytes))
                    if image.mode in ("RGBA", "P"): image = image.convert("RGB")
                    
                    out_bytes = io.BytesIO()
                    image.save(out_bytes, format="JPEG", quality=quality, optimize=True)
                    new_image_bytes = out_bytes.getvalue()
                    
                    if len(new_image_bytes) < len(image_bytes) * 0.9:
                        doc.update_stream(xref, new_image_bytes)
                except Exception as e:
                    pass
        doc.save(output_path, garbage=4, deflate=True)
        doc.close()
    except Exception as e:
        print(f"Failed to compress {input_path}, copying original... {e}")
        import shutil
        shutil.copy2(input_path, output_path)

pdfs = glob.glob(f'{orig_dir}/*.pdf')
if not pdfs:
    pdfs = glob.glob(f'{new_dir}/*.pdf')
    print("Using pdfs/ as source because pdfs_original is empty.")

total = len(pdfs)
for i, p in enumerate(pdfs):
    filename = os.path.basename(p)
    out_p = f'{new_dir}/{filename}'
    # If the file already exists in pdfs/ and is smaller than original, skip it
    orig_sz = os.path.getsize(p)
    if os.path.exists(out_p):
        out_sz = os.path.getsize(out_p)
        if out_sz < orig_sz or out_sz == orig_sz:
            print(f"[{i+1}/{total}] Skipping {filename}, already processed.")
            continue
            
    print(f"[{i+1}/{total}] Compressing {filename}...")
    compress_pdf(p, out_p, quality=60)
    if os.path.exists(out_p):
        new_sz = os.path.getsize(out_p)
        print(f"  -> {orig_sz/1024/1024:.1f} MB to {new_sz/1024/1024:.1f} MB")
    else:
        print(f"  -> Failed to generate {out_p}")

print("Finished compressing all PDFs!")
