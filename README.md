#   Szoftverrendszerek biztonsága (mil-geiakK689-ml) - Bitmap képben elrejtett üzenet
## Gyakorlati feladat ismertetése

### Leírás
Vizsgálja meg a steganográfiában használatos LSB - Least Significant Bit eljárást
Válassza ki azt a módszert, amelyik a legalkalmasabb a szöveg BMP fájlban való elrejtésére, figyelembe véve az adatbiztonságot és a képfájl minőségének megőrzését.

Készítsen egy olyan python programot, amely képes adott szöveges információt elrejteni egy megadott BMP képben.
A programnak biztosítania kell a titkosított szöveg későbbi visszanyerését.
A program biztosítson grafikus vagy parancssoros felületet a következő két funkciókhoz:

### Lépések

1. Szöveg beágyazása egy BMP fájlba.
2. Szöveg kiolvasása egy BMP fájlból.
3. A beágyazott adat méretének és elérhetőségének ellenőrzése.


### Dokumentáció

Készítsen leírást a program felépítéséről, működéséről és a felhasznált steganográfiai módszerről.

### Steganográfia 
Olyan módszer, amely lehetővé teszi információk rejtését más adatokban úgy, hogy az rejtett információ nem látható vagy érzékelhető a külső szemlélők számára. Ez gyakran digitális képekben, hangfájlokban vagy más médiafájlokban történik pl.: képekben elrejtett adatok, későbbi azonosítás miatt.

### Least Significant Bit
Egy technika a steganográfiában. Az alapelve az, hogy digitális adatokban (például egy képfájlban) minden pixelnek vagy bájtnak van egy legkevésbé jelentős bitje, ami a legkevésbé határozza meg az adat értékét. Ezek az LSB-k általában kis változásokat jelentenek a pixel vagy bájt értékében, amelyeket az emberi észlelés általában nem vesz észre.

## Szöveg elrejtése a képben

A ```hide_text``` metódussal valósítom meg az első lépést ami a szöveg elrejtése.

### PIL könyvtár

Az Image modulból importálom a PIL könyvtárat, amivel képekkel dolgozhatunk Pythonban.

### Paraméterei
- ```image_path```: a kép elérési útja, egy szmájlit készítettem Paint-ben, input.bmp néven hoztam létre
- ```text```: elrejtendő szöveg a képben 
- ```output_path```: a kimeneti kép elérési útja, output.bmp néven hoztam létre

### Lépések
1. Megnyitom a képet az image_path-ból, majd RGB formátumra konvertálom.
```
image = Image.open(image_path)
image = image.convert("RGB")
```
2. A paraméterül adott text-et bináris formátumra alakítom át. Minden karaktert 8 bites bináris számként egybeilleszti egy hosszú stringbe.
```
binary_text = ''.join(format(ord(char), '08b') for char in text)
```
3. Megnézem a szöveg hosszát bitben, ami szükséges a dekódoláshoz.
```
text_length = len(binary_text)
```
4. A rejtendő szöveg mérete nem lehet nagyobb, mint a kép pixeleinek száma. Minden karaktert elrejtünk a kép pixeleiben, egy bitet használva minden karakterhez. Ha a rejtendő szöveg mérete meghaladja a rendelkezésre álló pixelek számát, akkor nem lehetséges minden karaktert rejtett módon elhelyezni a képen.
```
if text_length * 3 > image.width * image.height:
        print("Error: Kép méret túl kicsi hogy elrejtesem a szöveget:", text)
        return
```
5. Bejárom a bináris szöveget, és az egyes bitjeit elrejti a kép pixeleiben, az RGB komponensek utolsó bitjének módosítása.
```
pixel_index = 0
    for char in binary_text:
        x = pixel_index % image.width
        y = pixel_index // image.width
        r, g, b = image.getpixel((x, y))
        new_r = r & 0xFE | int(char)
        image.putpixel((x, y), (new_r, g, b))
        pixel_index += 1
```
6. Elmentem a módosított képet az output_path-re.
```
image.save(output_path)
```

### Rejtett szöveg kinyerése képből

A ```extract_text``` metódussal valósítom meg a szöveg kinyerését.

### Paramétere
- ```image_path```: vizsgált kép elérési útját jelenti

### Lépések
1. Megnyitom az ```image_path```-et.
```
image = Image.open(image_path)
```
2. A ```binary_text```-be olvasom be a rejtett szöveget binárisan.
```
binary_text = ''
```
3. Végigmegyek a kép pixelein, minden pixelből kiszedem az RGB értékeket, és a pixel utolsó bitjét hozzáadom a ```binary_text``` stringhez.
```
for y in range(image.height):
        for x in range(image.width):
            pixel = image.getpixel((x, y))
            binary_text += bin(pixel[-1])[-1]
```
4. Bejárom a ```binary_text```-et, és visszaalakítom azt szöveggé, ahol minden 8 bit egy karaktert jelent. Amikor elérem a NULL karaktert ```\x00```, ami a szöveg vége, abbahagyom a dekódolást.
```
for i in range(0, len(binary_text), 8):
        text += chr(int(binary_text[i:i+8], 2))
        if text.endswith('\x00'):
            break
```
5. Visszatérek a dekódolt szöveggel, eltávolítva a NULL karaktereket a szöveg végéről ```rstrip('\x00')```.
```
return text.rstrip('\x00')
```
## Használat

Megadom az eredeti kép forrását az ```input_path``` változóba. Létrehoztam erre egy teszt képet, input.bmp néven.
```
input_path = "input.bmp"
```
Megadom az elrejtendő szöveget a ```text``` változóba. Nem voltam annyira ötletes, így a 'Rejts el' szöveget rejtem el.
```
text = "Rejts el"
```
Megadom a kimeneti, elrejtett szöveget tartalmazó kép forráshelyét az ```output_path``` változóba. Létrehoztam erre egy teszt képet, output.bmp néven, mint üres fájl.
```
output_path = "output.bmp"
```
A szükséges változók deklarálása és érték adása után, meghívom a szöveg elrejtését a szükséges paraméterekkel és kiíratom konzolra, hogy sikeresen "Elrejtettem a szöveget."
```
hide_text(input_path, text, output_path)
print("Elrejtettem a szöveget.")
```
Végül ellenőrzés képen az új output.bmp képbe mentett szöveget nyerem ki, az ```extract_text``` függvénnyel
Kiírom a konzolra az elrejtett szöveget.