import os
from PIL import Image

def convert_to_webp(folder_path):
    print(f"Compressing PNGs significantly using WebP (Near Lossless)...")
    
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.png') and "_compressed" not in filename:
            filepath = os.path.join(folder_path, filename)
            
            try:
                img = Image.open(filepath)
                
                original_size = os.path.getsize(filepath)
                print(f"\nProcessing {filename} (Original: {original_size / 1024 / 1024:.2f} MB)")
                
                quantized = img.quantize(colors=256, method=2)
                
                if img.mode == 'RGBA':
                    quantized = quantized.convert('RGBA')
                else:
                    quantized = quantized.convert('RGB')
                
                temp_path = filepath.replace(".png", "_temp.png")
                quantized.save(temp_path, format="PNG", optimize=True)
                
                new_size = os.path.getsize(temp_path)
                
                if new_size < original_size:
                    os.replace(temp_path, filepath)
                    print(f"--> Saved! Color quantization reduced size by {100 - (new_size/original_size * 100):.1f}% (Now {new_size / 1024 / 1024:.2f} MB)")
                else:
                    os.remove(temp_path)
                    print("--> Skipping, quantization didn't help.")
                    
            except Exception as e:
                print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    folder_target = "static/pics"
    convert_to_webp(folder_target)
