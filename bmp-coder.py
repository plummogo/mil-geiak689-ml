from PIL import Image

DELIMITER = '1111111111111110'

def encode(image_path, text, output_path):
    img = Image.open(image_path)
    width, height = img.size

    binary_text = ''.join(format(ord(t), '08b') for t in text)
    text_length = len(binary_text)

    if text_length > width * height * 3:
        print("Error: Kép méret túl kicsi hogy elrejtesem a szöveget:", text)

    binary_text += DELIMITER
    data_index = 0
    for y in range(height):
        for x in range(width):
            pixel = img.getpixel((x, y))
            for i in range(3):
                if data_index < text_length:
                    bit = int(binary_text[data_index])
                    pixel = set_bit(pixel, i, bit)
                    data_index += 1
            img.putpixel((x, y), pixel)

    img.save(output_path)

def set_bit(value, bit_index, bit):
    if bit:
        return value | (1 << bit_index)
    else:
        return value & ~(1 << bit_index)

def decode(image_path, delimiter = '11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111110'):
    img = Image.open(image_path)
    width, height = img.size
    binary_text = ''
    for y in range(height):
        for x in range(width):
            pixel = img.getpixel((x, y))
            for i in range(3):
                bit = pixel & 1
                binary_text += str(bit)
                if binary_text[-len(delimiter):] == delimiter:
                    return ''.join(chr(int(binary_text[i:i+8], 2)) for i in range(0, len(binary_text)-len(delimiter), 8))
                pixel >>= 1
    return None

image_path = 'input.bmp'
output_path = 'output.bmp'
text = 'Rejts el'

encode(image_path, text, output_path)
print("Elrejtettem a szöveget.")

decoded_text = decode(output_path)
print("Visszafejtett elrejtett szöveg:", decoded_text)