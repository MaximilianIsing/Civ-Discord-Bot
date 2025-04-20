from PIL import Image
import os

input_folder = "wonder WEBP"
output_folder = "wonder PNG"

os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.endswith(".webp"):
        img_path = os.path.join(input_folder, filename)
        img = Image.open(img_path).convert("RGBA")

        output_name = filename.replace(".webp", ".png")
        img.save(os.path.join(output_folder, output_name), "PNG")