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
Olyan módszer, amely lehetővé teszi információk rejtését más adatokban úgy, hogy az rejtett információ nem látható vagy érzékelhető a külső szemlélők számára. Ez gyakran digitális képekben, hangfájlokban vagy más médiafájlokban történik pl.: képekben elrejtett adatok, későbbi azonosítás miatt.[^1]

### Least Significant Bit
Egy technika a steganográfiában. Az alapelve az, hogy digitális adatokban (például egy képfájlban) minden pixelnek vagy bájtnak van egy legkevésbé jelentős bitje, ami a legkevésbé határozza meg az adat értékét. Ezek az LSB-k általában kis változásokat jelentenek a pixel vagy bájt értékében, amelyeket az emberi észlelés általában nem vesz észre.[^2]

## Szöveg elrejtése a képben

A ```encode``` metódussal valósítom meg az első lépést ami a szöveg elrejtése.

### PIL könyvtár

Az Image modulból importálom a PIL könyvtárat, amivel képekkel dolgozhatunk Pythonban.[^3]

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

width * height * 3 : kép összes pixelének száma és a pixelek RGB lehetőségei

```
if text_length > width * height * 3:
        print("Error: Kép méret túl kicsi hogy elrejtesem a szöveget:", text)
        return
```
5. Hozzáadom a jelölőt a ```binary_text```-hez, ami szöveg végét jelzi majd a későbbi dekódoláskor.
```
binary_text += '1111111111111110'
```
6. Inicializálom a ```data_index```, amely segít nyomon követni, hogy hol tartunk a beágyazandó bináris szövegben.
```
data_index = 0
```
7. Bejárom a kép sorait ```y```, azon belül az aktuális sor pixeleit ```x```, az adott pixel értékét lekérem ```img.getpixel((x, y))```. Bejárom az RGB-t a pixelen ```i```
Lecsekkolom, hogy van-e még beágyazandó adat a bináris szövegben ```if data_index < text_length```.  Kiválasztom a következő bitet a bináris szövegből és átalakítom egész számmá ```bit = int(binary_text[data_index])```. 
Beállítom az aktuális RGB csatorna legkevésbé jelentős bitjét a kiválasztott bitre a ```set_bit``` függvény segítségével ```pixel = set_bit(pixel, i, bit)```. 
Növelem az adatindexet, hogy a következő bitet válassza ki a bináris szövegből ```data_index += 1```.
Beállítom az aktuális pixel értékét a módosított értékre a beágyazott szöveg legkevésbé jelentős bitjeinek beállítása után ```img.putpixel((x, y), pixel)```.  

Teljes kód:
```
for y in range(height):
        for x in range(width):
            pixel = img.getpixel((x, y))
            for i in range(3):
                if data_index < text_length:
                    bit = int(binary_text[data_index])
                    pixel = set_bit(pixel, i, bit)
                    data_index += 1
            img.putpixel((x, y), pixel)
```
6. Elmentem a módosított képet az output_path-re.
```
image.save(output_path)
```

## Bit beállítása 
A legkevésbé jelentős bit beállításáért a ```set_bit``` segédfüggvény felel.

### Paraméterei
- ```value```: Az az érték, amelyben a bitet módosítom.
- ```bit_index```: A bit indexe, amelyet módosítani kell.
- ```bit```: A bit értéke (0 vagy 1), amelyre a megadott bitet be kell állítani.

### Lépések
1. Ellenőrzöm, hogy a bit változó értéke igaz-e (1). Ha igen, akkor a következő lépésben az adott bitet be kell állítani az értékben ```if bit```.

2. Ha a bit igaz, akkor az ```or``` műveletet használjuk az érték megadott bitjének beállítására. Az ```(1 << bit_index)``` megadott ```bit_index``` bitet tartalmazó maszkot hozza létre, amelyet az ```or``` operátorral kombinálva beállítom az értékben ```return value | (1 << bit_index)```.

3. Ha a bit hamis (0), akkor a következő lépésben az adott bitet törölni kell az értékből ```else::```. 

4. Ha a bit hamis, akkor az ```and``` műveletet használjuk az érték megadott bitjének törlésére. Az ```(1 << bit_index)``` kifejezést először megfordítom a ~ bitenkénti negációval, majd az ```and``` operátorral kombinálva törlöm az értékben az adott bitet ```return value & ~(1 << bit_index)```. 

Teljes kód: 

```
def set_bit(value, bit_index, bit):
    if bit:
        return value | (1 << bit_index)
    else:
        return value & ~(1 << bit_index)

```

### Rejtett szöveg kinyerése képből

A ```decode``` metódussal valósítom meg a szöveg kinyerését.

### Paramétere
- ```image_path```: vizsgált kép elérési útját jelenti

### Lépések

1. Megnyitom az ```image_path```-et.
```
image = Image.open(image_path)
```
2. Lekérem a kép szélességét és magasságát.
```
width, height = img.size: 
```
3. Inicializálom a ```binary_text```, a bináris adatokat  tároló változót.
```
binary_text = ''
``` 
4. Bejárom a kép sorait ```y```, azon belül az aktuális sor pixeleit ```x```, az adott pixel értékét lekérem ```img.getpixel((x, y))```. Bejárom az RGB-t a pixelen ```i``` Ezek a lépések megegyeznek az ```encode``` függvénnyel.
5. Kiválasztom az aktuális pixel legkevésbé jelentős bitjét az ```and``` művelet segítségével ```bit = pixel & 1```.
6. Hozzáadom a kiválasztott bitet a ```binary_text``` változóhoz stringként ```binary_text += str(bit)```.
7.  Lecsekkolom, hogy a ```binary_text``` változó végén található rész megegyezik-e a szöveg végét jelölő```delimiter``` változóval. Ha igen, elértem a beágyazott adatok végét, és kiléphetünk a ciklusból ```if binary_text[-len(delimiter):] == delimiter```.
8. Visszaadom a kinyert szöveget, ami a bináris adatokat kódolja vissza ASCII karakterekké. Ez történik a bináris adatokat 8 bitenként konvertálva egész számmá ```(int(binary_text[i:i+8], 2))```, majd az egész számokat átalakítva ASCII karakterekké ```chr()```, és ezeket összefűzöm a ```join()``` függvény segítségével ```return ''.join(chr(int(binary_text[i:i+8], 2)) for i in range(0, len(binary_text)-len(delimiter), 8))```
9. Ha nem találja meg a ```delimiter```-t a ```binary_text```-ben, a ciklusok végén ```None```-t ad vissza, mert ez azt jelenti, hogy nem találtunk adatot a képen.

Teljes kód:
```
def decode(image_path):
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
```
## Használat

Felhasznált forrásom egy medium cikk volt[^4] illetve egy hivatalos Python dokumentáció[^5].

Megadom az eredeti kép forrását az ```input_path``` változóba. Létrehoztam erre egy teszt képet, input.bmp néven.
```
input_path = "input.bmp"
```
Megadom a kimeneti, elrejtett szöveget tartalmazó kép forráshelyét az ```output_path``` változóba. Létrehoztam erre egy teszt képet, output.bmp néven, mint üres fájl.
```
output_path = "output.bmp"
```
Megadom az elrejtendő szöveget a ```text``` változóba. Nem voltam annyira ötletes, így a 'Rejts el' szöveget rejtem el.
```
text = "Rejts el"
```
A szükséges változók deklarálása és érték adása után, meghívom a szöveg elrejtését a szükséges paraméterekkel és kiíratom konzolra, hogy sikeresen "Elrejtettem a szöveget."
```
encode(image_path, text, output_path)
print("Elrejtettem a szöveget.")
```
Végül ellenőrzés képen az új output.bmp képbe mentett szöveget nyerem ki, az ```decode``` függvénnyel
Kiírom a konzolra az elrejtett szöveget.

[^1]: https://hu.wikipedia.org/wiki/Szteganogr%C3%A1fia
[^2]: https://en.wikipedia.org/wiki/Bit_numbering
[^3]: https://pypi.org/project/pillow/
[^4]: https://lorenzobn.medium.com/hiding-data-inside-an-image-randomized-lsb-steganography-with-python-6c10caafad98
[^5]: https://thepythoncode.com/article/hide-secret-data-in-images-using-steganography-python