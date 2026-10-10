import sys
from PIL import Image


def ascunde(gazda, mesaj, destinatie):
    if "\0" in mesaj:
        raise ValueError("Mesajul nu poate contine caracterul NUL.")
    if not str(destinatie).lower().endswith(".png"):
        raise ValueError("Salveaza imaginea ca PNG.")
    with Image.open(gazda) as original:
        imagine = original.convert("RGB")
    pixeli = list(imagine.getdata())

    date = mesaj.encode("utf-8") + b"\0"
    biti = ""
    for octet in date:
        biti = biti + f"{octet:08b}"
    if len(biti) > len(pixeli) * 3:
        raise ValueError("Mesajul este prea mare pentru imagine.")

    pixeli_noi = []
    pozitie = 0
    for pixel in pixeli:
        rgb = list(pixel)
        for canal in range(3):
            if pozitie < len(biti):
                bit = int(biti[pozitie])
                rgb[canal] = (rgb[canal] & ~1) | bit
                pozitie = pozitie + 1
        pixeli_noi.append(tuple(rgb))

    imagine.putdata(pixeli_noi)
    imagine.save(destinatie, format="PNG")


def dezvaluie(cale):
    with Image.open(cale) as original:
        imagine = original.convert("RGB")
    mesaj = bytearray()
    biti = ""
    for pixel in imagine.getdata():
        for canal in pixel:
            biti = biti + str(canal & 1)
            if len(biti) == 8:
                octet = int(biti, 2)
                if octet == 0:
                    return mesaj.decode("utf-8")
                mesaj.append(octet)
                biti = ""
    raise ValueError("Imaginea nu contine un mesaj cu terminator NUL.")


def main():
    try:
        if len(sys.argv) == 5 and sys.argv[1] == "ascunde":
            ascunde(sys.argv[2], sys.argv[3], sys.argv[4])
            print("Mesaj ascuns in", sys.argv[4])
        elif len(sys.argv) == 3 and sys.argv[1] == "dezvaluie":
            print(dezvaluie(sys.argv[2]))
        else:
            print("python stego.py ascunde gazda.jpg mesaj rezultat.png")
            print("python stego.py dezvaluie rezultat.png")
            raise SystemExit(1)
    except (OSError, ValueError) as error:
        print("Eroare:", error)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
