# Laborator: functii, metode si importuri pe web
# Student: necompletat

import requests
import urllib.request
import requests as rq
from requests import get
import time

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10


def main():
    # 1: requests este extern; urllib este inclus in Python.
    print("1. Versiunea requests:", requests.__version__)

    try:
        # 2: numele modulului arata de unde vine functia.
        response = requests.get(BASE_URL, timeout=TIMEOUT)
        print("2. requests.get:", response.status_code)
        time.sleep(1)

        # Acest import permite un apel mai scurt.
        response = get(BASE_URL, timeout=TIMEOUT)
        print("2. get:", response.status_code)
        time.sleep(1)

        # 3: un alias cunoscut scurteaza apelul; unul neclar face codul greu de citit.
        response = rq.get(BASE_URL, timeout=TIMEOUT)
        print("3. rq.get:", response.status_code)
        time.sleep(1)
    except requests.RequestException as error:
        print("Eroare la cerere:", error)
        time.sleep(1)

    try:
        with urllib.request.urlopen(BASE_URL, timeout=TIMEOUT) as response:
            text = response.read().decode("utf-8", errors="replace")
            print("4. Status urllib:", response.status)
            print(text[:200])
    except OSError as error:
        print("Eroare urllib:", error)
    time.sleep(1)

    # 5: get este functie, Session este clasa, sessions este modul.
    print("5. Numele din requests:", dir(requests))

    help(requests.get)
    try:
        response = requests.get(BASE_URL, timeout=TIMEOUT)
        print("6. Cerere cu timeout:", response.status_code)
    except requests.RequestException as error:
        print("Eroare la cerere:", error)
    time.sleep(1)

    try:
        start = time.perf_counter()
        response = requests.get(BASE_URL, timeout=TIMEOUT)
        end = time.perf_counter()
        print("7. Durata totala:", end - start)
        print("7. response.elapsed:", response.elapsed.total_seconds())
    except requests.RequestException as error:
        print("Eroare la cronometrare:", error)

    try:
        import bs4
        print("8. bs4 este instalat:", bs4.__version__)
    except ImportError:
        print("Instalați modulul cu: pip install beautifulsoup4")

    # Modul = un fisier cu cod. Pachet = mai multe module grupate.
    # Biblioteca = cod reutilizabil, care poate contine mai multe pachete.


if __name__ == "__main__":
    main()
