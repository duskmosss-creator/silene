import fitz
import os
import io
from PIL import Image

def compress_pdf(input_path, output_path, quality=60):
    doc = fitz.open(input_path)
    print(f"Compressing {input_path}...")
    for i in range(len(doc)):
        page = doc[i]
        image_list = page.get_images(full=True)
        for img in image_list:
            xref = img[0]
            try:
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                
                # Load with PIL
                image = Image.open(io.BytesIO(image_bytes))
                
                # Convert to RGB if needed
                if image.mode in ("RGBA", "P"): image = image.convert("RGB")
                
                # Save compressed
                out_bytes = io.BytesIO()
                image.save(out_bytes, format="JPEG", quality=quality, optimize=True)
                new_image_bytes = out_bytes.getvalue()
                
                if len(new_image_bytes) < len(image_bytes):
                    # Replace image
                    doc.update_stream(xref, new_image_bytes)
            except Exception as e:
                pass
                
    doc.save(output_path, garbage=4, deflate=True)
    doc.close()

if __name__ == "__main__":
    p = 'natgeo_collection/pdfs/nationalgeographicusa-june2019.pdf'
    orig = os.path.getsize(p)
    compress_pdf(p, 'test_compress.pdf')
    new_sz = os.path.getsize('test_compress.pdf')
    print(f'Original: {orig/1024/1024:.1f} MB')
    print(f'New: {new_sz/1024/1024:.1f} MB')
