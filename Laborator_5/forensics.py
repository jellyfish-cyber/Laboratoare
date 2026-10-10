import os
import re
import json
import zipfile
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS


def tip_real(cale):
    with open(cale, "rb") as file:
        cap = file.read(8)
    if cap.startswith(b"%PDF"):
        return "pdf"
    if cap.startswith(b"\x89PNG"):
        return "png"
    if cap.startswith(b"\xff\xd8"):
        return "jpeg"
    if cap.startswith(b"PK\x03\x04"):
        return "zip/docx"
    return cap.hex()


def strings(cale):
    with open(cale, "rb") as file:
        date = file.read()
    texte = re.findall(rb"[ -~]{4,}", date)
    rezultat = []
    for text in texte:
        rezultat.append(text.decode("ascii"))
    return rezultat


def gps_decimal(coordonate, emisfera):
    grade = float(coordonate[0])
    minute = float(coordonate[1])
    secunde = float(coordonate[2])
    rezultat = grade + minute / 60 + secunde / 3600
    if emisfera == "S" or emisfera == "W":
        rezultat = -rezultat
    return rezultat


def read_metadata(cale):
    with Image.open(cale) as imagine:
        exif = imagine._getexif()
    if exif is None:
        return {}

    metadate = {}
    for cod in exif:
        if cod != 34853:
            nume = TAGS.get(cod, str(cod))
            metadate[nume] = str(exif[cod])

    gps = exif.get(34853, {})
    date_gps = {}
    for cod in gps:
        nume = GPSTAGS.get(cod, str(cod))
        date_gps[nume] = str(gps[cod])
    metadate["GPSInfo"] = date_gps
    if 1 in gps and 2 in gps and 3 in gps and 4 in gps:
        metadate["latitude"] = gps_decimal(gps[2], gps[1])
        metadate["longitude"] = gps_decimal(gps[4], gps[3])
    return metadate


def carve_zip(cale, destinatie):
    with open(cale, "rb") as file:
        date = file.read()
    pozitie = date.find(b"PK\x03\x04")
    if pozitie == -1:
        raise ValueError("Nu am gasit o arhiva ZIP.")

    os.makedirs(destinatie, exist_ok=True)
    cale_zip = os.path.join(destinatie, "gasit.zip")
    with open(cale_zip, "wb") as file:
        file.write(date[pozitie:])
    with zipfile.ZipFile(cale_zip) as arhiva:
        nume_fisiere = arhiva.namelist()
        arhiva.extractall(destinatie)
    return {"offset": pozitie, "arhiva": cale_zip, "fisiere": nume_fisiere}


def main():
    folder = os.path.dirname(os.path.abspath(__file__))
    probe = os.path.join(folder, "probe")
    rezultate = os.path.join(folder, "rezultate")
    try:
        tipuri = {}
        for nume in ["foto.jpg", "ascuns.png", "xor.bin"]:
            tipuri[nume] = tip_real(os.path.join(probe, nume))

        raport = {
            "tipuri": tipuri,
            "strings": strings(os.path.join(probe, "ascuns.png")),
            "metadate": read_metadata(os.path.join(probe, "foto.jpg")),
            "carving": carve_zip(os.path.join(probe, "ascuns.png"), rezultate)
        }
        print(json.dumps(raport, indent=2, ensure_ascii=False))
    except (OSError, ValueError, zipfile.BadZipFile) as error:
        print("Eroare:", error)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
