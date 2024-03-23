#   Szoftverrendszerek biztonsága (mil-geiakK689-ml) - Caesar-kód gyakorlati feladat

## Gyakorlati feladat ismertetése
A Caesar-kód vagy Caesar-rejtjel az egyik legegyszerűbb és legelterjedtebb titkosírási módszer. Ez egy helyettesítő rejtjel, ami azt jelenti, hogy minden egyes betűt az ábécében egy tőle meghatározott távolságra lévő betűvel kell helyettesíteni. Így például, ha mondjuk az eltolódás 3, az angol ábécében az A-t a D-vel, a B-t az E-vel stb. kell helyettesíteni. A magyar ábécére vonatkoztatva ez az A betű helyett C-t, az Á betű helyett CS-t jelent. Az elnevezését Julius Caesar után kapta, aki ennek a segítségével kommunikált tábornokaival. [^1]


## Kódolás

A titkosítás két ábécével megvalósítható úgy, hogy az egyiket a másik alá írva 'n' betűhellyel eltoljuk.

### Karakter abc és mappelés beállítása
```generateMapping(key)```függvény egy karakter leképezést hoz létre, ahol minden betűt egy másik betűre cserél. Lépések:

1. Létrehoz egy angol abc tömböt.
2. Lemásolja az abc tömböt egy ```shuffled``` változóba, ez lesz ahol megkeveri a következő lépésben.
3. A shuffled tömb elemeit keveri (megzavarja) az alábbi módon:
    - Végigmegy a tömbön hátulról előre.
    - Minden iterációban kiszámít egy pseudoRandom értéket a megadott key és az iteráció jelenlegi indexe alapján, amit egy modulo művelettel korlátoz a tömb hosszára, hogy biztosan a tömb indexein belül maradjon
    - Megcseréli a jelenlegi elemet (shuffled[i]) a pseudoRandom indexű elemmel a shuffled tömbön belül.
    - Létrehoz egy új objektumot (acc), ahol az eredeti ábécé minden betűjét (abc) hozzárendeli a megzavart ábécé egy-egy betűjéhez (shuffled), tehát lényegében egy leképezést hoz létre az eredeti és a megzavart ábécé között
    - Visszatér az elkészült leképezéssel

### Kódolás

```encrypt(text, key)``` függvény egy szöveget titkosít a fenti ```generateMapping(key)``` függvénnyel generált leképezés alapján. Lépések:

1. Meghívja a ```generateMapping``` függvényt a megadott ```key```-el, hogy megkapja a karakterek leképezését
2. A megadott szöveget karakterekre bontja, majd minden karaktert lecserél a leképezésben található megfelelőjére. Amennyiben egy karakter nem szerepel a leképezésben (pl. számjegy vagy speciális karakter), akkor azt változatlanul hagyja
3. Az így kapott karaktereket összefűzi egy új szöveggé, ami lesz a titkosított üzenet

## Dekódolás

```decrypt(text, key)``` függvény egy korábban titkosított szöveget fejt vissza a ```generateMapping(key)``` függvény által generált leképezés használatával. Lépések:

1. Meghívja a ```generateMapping(key)``` függvényt a megadott ```key```-el, hogy megkapja a titkosításkor használt karakterek leképezését

2. Létrehoz egy új, invertált leképezést ```invCharMap```, amely a titkosított betűket rendeli hozzá az eredeti betűkhöz
    - Végigmegy a titkosítási leképezés kulcs-érték párokon (original, encrypted)
    - Új leképezésben az ```encrypted``` betűket teszi meg kulcsként, míg az ```original``` betűket értékként

3. Titkosított szöveget ```text``` karakterenként feldolgozza:
    - Minden karaktert megpróbál leképezni az invertált leképezés segítségével az ```encrypted``` (titkosított) betűből vissza az ```original``` (eredeti) betűbe
    - Amennyiben a karakter nem szerepel a leképezésben (pl. számjegyek vagy speciális karakterek, amelyek nem részei a titkosításnak), a karakter változatlan marad
    - Az így visszafejtett karaktereket összefűzi, létrehozva ezzel a dekódolt szöveget

## Feltörés
```hack(text)```  függvény nem konkrét eltolási értékkel dekódol, hanem kipróbál minden lehetséges eltolást (1-től 25-ig, mivel a 26 eltolás már az eredeti szöveget adná vissza) a titkosított szöveg dekódolására. Lépések:

1. Változóban eltárolja az angol ábécé kisbetűit

2. Tömbben gyűjti a lehetséges dekódolt szövegeket

3. Végigmegy az összes lehetséges eltoláson (1-től 25-ig), és minden iterációban:
    - Szétszedi a titkosított szöveget karakterekre
    - Minden karakterre elvégzi az alábbi műveleteket:
        - Ellenőrzi, hogy az adott karakter betű-e (figyelmen kívül hagyja a nem betű karaktereket)
        - Ellenőrzi, hogy az adott karakter nagybetű-e
        - Karaktert kisbetűvé alakítja, ha szükséges
        - Megkeresi a karakter jelenlegi indexét az ábécében
        - Kiszámítja az új indexet az eltolás figyelembevételével, az index értéke ne legyen negatív (a JavaScript modulo operátora negatív értéket is adhat)
        - Új index alapján megkeresi a megfelelő karaktert az ábécében
        - Karaktert nagybetűvé alakítja vissza, ha eredetileg is az volt
- Módosított karaktereket összefűzi egy szöveggé
- Hozzáadja a dekódolt szöveget a lehetséges dekódolt szövegek tömbjéhez
- Kiírja a konzolra a dekódolt szöveget

## Használat
Elég egy böngésző (bármilyen), nyisd meg a DevTool-t (F12). Lépések:

1. Másold a kódot DevTool-ba
2. Kikommentelt részt vond vissza
3. Futasd le

[^1]: https://hu.wikipedia.org/wiki/Caesar-rejtjel