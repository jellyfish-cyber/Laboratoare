# Laboratorul 5 Forensics și steganografie

Nume și prenume: necompletate

Grupa: necompletată

Probele sunt generate cu scriptul furnizat `probe_pregateste.py`, integrat ca `probe/pregateste.py`. Secțiunea pentru probele bonus a fost omisă. Fotografia și metadatele sunt date de exercițiu create de generator.

## Lucrarea A

| Probă | Rezultat |
| --- | --- |
| mesaj.txt | base64 → base64 → hex → `FLAG{straturi_de_encoding}` |
| xor.bin | cheia 128 (0x80); `Un singur octet tine tot secretul... gaseste-l! FLAG{xor_un_octet}` |
| hashuri.txt | cinci hashuri MD5; parolele `password`, `dragon`, `qwerty`, `letmein`, `monkey` |

Decoderul încearcă toate cele 256 de chei XOR și compară hashurile cuvintelor din `wordlist.txt` cu țintele. Fișa mesajului este `arsenal/forensics/fisa.json`. Testul base64 cerut la A7 trece.

## Lucrarea B

Tipuri reale: `foto.jpg` este JPEG, `ascuns.png` este PNG. Fișierul `xor.bin` nu are o semnătură cunoscută. Extragerea strings identifică și numele `secret.txt` în PNG.

Metadate EXIF: Make `Apple`, Model `iPhone 13`, DateTime `2026:09:14 10:30:00`. Aceste valori sunt stabilite de generator.

GPS: 47° 1′ 0″ N și 28° 51′ 27″ E. Coordonate zecimale: latitudine **47.016666666666666**, longitudine **28.8575**.

Arhiva ZIP începe la octetul **782**, după PNG IEND. `rezultate/gasit.zip` conține `secret.txt`, cu mesajul **`FLAG{ascuns_prin_carving}`**.

În `stego.png` mesajul este scris în biții LSB ai canalelor RGB, urmat de octetul NUL. Mesajul dezvăluit este **`FLAG{ascuns_in_pixeli}`**. Rezultatul este PNG, pentru păstrarea biților.

Outputul tuturor exercițiilor și al testului este reunit în `rezultate/output.txt`.
