from PIL import Image

def hide_text(image_path, text, output_path):
    image = Image.open(image_path)
    image = image.convert("RGB")
    binary_text = ''.join(format(ord(char), '08b') for char in text)
    text_length = len(binary_text)
    
    if text_length > image.width * image.height * 3:
        print("Error: Kép méret túl kicsi hogy elrejtesem a szöveget:", text)
        return
    
    pixel_index = 0
    for char in binary_text:
        x = pixel_index % image.width
        y = pixel_index // image.width
        r, g, b = image.getpixel((x, y))
        new_r = r & 0xFE | int(char)
        image.putpixel((x, y), (new_r, g, b))
        pixel_index += 1
    
    image.save(output_path)

def extract_text(image_path):
    image = Image.open(image_path)
    binary_text = ''
    for y in range(image.height):
        for x in range(image.width):
            pixel = image.getpixel((x, y))
            binary_text += bin(pixel[0])[-1]
            binary_text += bin(pixel[1])[-1]
            binary_text += bin(pixel[2])[-1]
    text = ''
    for i in range(0, len(binary_text), 8):
        text += chr(int(binary_text[i:i+8], 2))
        if text.endswith('\x00'):
            break
    return text.rstrip('\x00')

input_path = "input.bmp"
text = "Teszt"
output_path = "output.bmp"

hide_text(input_path, text, output_path)
print("Elrejtettem a szöveget.")

extracted_text = extract_text(output_path)
print("Kinyert szöveg:", extracted_text)
