# -*- coding: utf-8 -*-
"""Laboratorul 8 - partea A. Scoate si numara esecurile din auth.log.
Generat din programul de laborator, cu codul scris de student."""
import re
import sys
from collections import Counter

TIPAR = re.compile(r"Failed password for (?:invalid user )?(\S+) from (\S+) port")


def esec(linie):
    """Sarcina 1. Scoate (user, ip) dintr-un rand de esec.

    Foloseste TIPAR, definit mai sus. Daca randul nu e un esec de
    autentificare, TIPAR.search intoarce None - atunci si tu intorci None.
    None nu e o eroare, e un semnal ca randul nu ne intereseaza.

    esec("x Failed password for root from 203.0.113.9 port 51230 ssh2")
        ->  ('root', '203.0.113.9')
    esec("<linie stricata>")  ->  None
    """
    potrivire = TIPAR.search(linie)
    if potrivire is None:
        return None
    return potrivire.groups()

def citeste_esecuri(cale):
    """Sarcina 2. Lista de esecuri din fisier, robusta la randuri stricate.

    Parcurge fisierul si strange fisele {"user": ..., "ip": ...} intr-o
    lista. Randurile care nu sunt esecuri (esec intoarce None) se sar.

    Daca fisierul nu exista, prinde FileNotFoundError, scrie un mesaj si
    intoarce o lista goala - nu lasa programul sa crape.

    citeste_esecuri("start/auth.log")  ->  lista cu 15 dictionare
    """
    esecuri = []
    try:
        with open(cale, encoding="utf-8", errors="replace") as jurnal:
            for linie in jurnal:
                rezultat = esec(linie)
                if rezultat is not None:
                    user, ip = rezultat
                    esecuri.append({"user": user, "ip": ip})
    except FileNotFoundError:
        print(f"Nu gasesc fisierul: {cale}", file=sys.stderr)
    return esecuri

def pe_ip(esecuri):
    """Sarcina 3. Numara esecurile pe fiecare adresa IP.

    Primeste lista de la citeste_esecuri si intoarce un Counter al
    adreselor: cheia e IP-ul, valoarea de cate ori apare.

    Vezi Counter(e["ip"] for e in esecuri).
    """
    return Counter(e["ip"] for e in esecuri)

def rezumat(cale):
    """Sarcina 4. Leaga totul: citeste, numara, intoarce rezumatul.

    Intoarce un dictionar cu doua chei:
        {"esecuri": cate esecuri in total,
         "pe_ip": Counter-ul adreselor}

    Nu tipari nimic aici; doar intoarce. Afisarea o face programul.
    """
    esecuri = citeste_esecuri(cale)
    return {"esecuri": len(esecuri), "pe_ip": pe_ip(esecuri)}


# ---------------------------------------------------------------------------
#  PARTEA B - detectorul de brute force
# ---------------------------------------------------------------------------

def main():
    from pathlib import Path
    implicit = Path(__file__).with_name('start') / 'auth.log'
    cale = sys.argv[1] if len(sys.argv) > 1 else implicit
    esecuri = citeste_esecuri(cale)
    counts = pe_ip(esecuri)
    print('Esecuri de autentificare:', len(esecuri))
    for ip, n in counts.most_common():
        print('  %s: %d' % (ip, n))


if __name__ == '__main__':
    main()
