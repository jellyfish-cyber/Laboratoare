import os
import argparse
import base64
import binascii
import hashlib
import json
import re
from urllib.parse import unquote_to_bytes


def text_si_octeti():
    text = "Salut"
    octeti = text.encode()
    print(octeti, octeti[0])
    hex_text = octeti.hex()
    print(hex_text)
    print(bytes.fromhex(hex_text))


def ghici_strat(text):
    if re.search(r"%[0-9a-fA-F]{2}", text):
        return "url"
    if len(text) > 0 and len(text) % 2 == 0:
        if re.fullmatch(r"[0-9a-fA-F]+", text):
            return "hex"
    if len(text) > 0 and len(text) % 4 == 0:
        if re.fullmatch(r"[A-Za-z0-9+/]+={0,2}", text):
            return "base64"
    return "necunoscut"


def desfa(text):
    strat = ghici_strat(text)
    if strat == "url":
        return strat, unquote_to_bytes(text)
    if strat == "hex":
        return strat, bytes.fromhex(text)
    if strat == "base64":
        try:
            return strat, base64.b64decode(text, validate=True)
        except binascii.Error:
            return "necunoscut", text.encode()
    return strat, text.encode()


def citibil(octeti):
    for octet in octeti:
        if octet < 32 or octet > 126:
            return False
    return True


def decode_layers(text):
    straturi = []
    for incercare in range(8):
        strat, octeti = desfa(text)
        if strat == "necunoscut":
            break
        if not citibil(octeti):
            break
        text_nou = octeti.decode("utf-8")
        if text_nou == text:
            break
        straturi.append(strat)
        text = text_nou
    return {"strat": straturi, "rezultat": text}


def sparge_xor(date):
    rezultate = []
    for cheie in range(256):
        clar = bytearray()
        for octet in date:
            clar.append(octet ^ cheie)
        if citibil(clar):
            rezultate.append({"cheie": cheie, "rezultat": clar.decode("ascii")})
    return rezultate


def sparge_hash(tinta, cuvinte):
    tinta = tinta.strip().lower()
    if re.fullmatch(r"[0-9a-f]+", tinta) is None:
        raise ValueError("Hashul trebuie sa fie un sir hex.")
    if len(tinta) == 32:
        algoritm = "md5"
    elif len(tinta) == 40:
        algoritm = "sha1"
    elif len(tinta) == 64:
        algoritm = "sha256"
    else:
        raise ValueError("Lungime de hash necunoscuta.")

    for cuvant in cuvinte:
        cuvant = cuvant.rstrip("\r\n")
        if algoritm == "md5":
            hash_cuvant = hashlib.md5(cuvant.encode()).hexdigest()
        elif algoritm == "sha1":
            hash_cuvant = hashlib.sha1(cuvant.encode()).hexdigest()
        else:
            hash_cuvant = hashlib.sha256(cuvant.encode()).hexdigest()
        if hash_cuvant == tinta:
            return {"algoritm": algoritm, "hash": tinta, "parola": cuvant}
    return {"algoritm": algoritm, "hash": tinta, "parola": None}


def main():
    folder = os.path.dirname(os.path.abspath(__file__))
    wordlist = os.path.join(folder, "..", "..", "probe", "wordlist.txt")
    parser = argparse.ArgumentParser(description="Decoder pentru laboratorul 5")
    parser.add_argument("intrare")
    parser.add_argument("--fisier", action="store_true")
    parser.add_argument("--mod", choices=["auto", "straturi", "xor", "hash"], default="auto")
    parser.add_argument("--wordlist", default=wordlist)
    parser.add_argument("--output", default=os.path.join(folder, "fisa.json"))
    args = parser.parse_args()

    try:
        if args.fisier:
            with open(args.intrare, "rb") as file:
                date = file.read()
        else:
            date = args.intrare.encode()

        mod = args.mod
        if mod == "auto":
            if not citibil(date.strip()):
                mod = "xor"
            else:
                text = date.decode().strip()
                linii = text.splitlines()
                prima_linie = ""
                if len(linii) > 0:
                    prima_linie = linii[0]
                if len(prima_linie) in [32, 40, 64] and ghici_strat(prima_linie) == "hex":
                    mod = "hash"
                else:
                    mod = "straturi"

        if mod == "xor":
            candidati = sparge_xor(date)
            primul = None
            if len(candidati) > 0:
                primul = candidati[0]
            rezultat = {"strat": "xor", "rezultat": primul,
                        "candidati": candidati, "chei_incercate": 256}
        elif mod == "hash":
            with open(args.wordlist, "r", encoding="latin1") as file:
                cuvinte = file.read().splitlines()
            parole = []
            for linie in date.decode().splitlines():
                if linie.strip() != "":
                    parole.append(sparge_hash(linie, cuvinte))
            rezultat = {"strat": "hash", "rezultat": parole}
        else:
            rezultat = decode_layers(date.decode().strip())

        with open(args.output, "w", encoding="utf-8") as file:
            json.dump(rezultat, file, indent=2, ensure_ascii=False)
        print(json.dumps(rezultat, indent=2, ensure_ascii=False))
    except (OSError, ValueError) as error:
        parser.exit(1, "Eroare: " + str(error) + "\n")


if __name__ == "__main__":
    main()
