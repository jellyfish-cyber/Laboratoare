# Laborator: functii, metode si importuri pe web
# Student: necompletat

import requests
from webtools import fetch, get_title, pause_between_requests

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10


def main():
    try:
        response = fetch(BASE_URL)
        print("9. Status:", response.status_code)  # atribut
        print("9. OK:", response.ok)               # atribut
        print("9. URL:", response.url)             # atribut
        print("9. Encoding:", response.encoding)   # atribut

        for name, value in response.headers.items():
            print(name + ": " + value)

        print("12. Server:", response.headers.get("Server", "lipsește"))
        print("12. Content-Type:", response.headers.get("Content-Type", "lipsește"))
        print("12. content-type:", response.headers.get("content-type", "lipsește"))

        # 13: lower() da un nou text, pe care putem apela count().
        print("13. Aparitii cyber:", response.text.lower().count("cyber"))
        print("14. Titlu:", get_title(response.text))

        lines = response.text.splitlines()
        print("15. Numar de linii:", len(lines))
        if len(lines) > 0:
            longest = max(lines, key=len)
            print("15. Lungimea maxima:", len(longest))
        else:
            print("15. Lungimea maxima: 0")

        if response.url.startswith("https://"):
            print("16. Conexiune securizată")
        else:
            print("16. Conexiune nesecurizată")

        if len(response.cookies) == 0:
            print("19. Niciun cookie setat.")
        else:
            for cookie in response.cookies:
                print("19.", cookie.name, cookie.secure)

        response.raise_for_status()
        print("10. Pagina principala a raspuns fara eroare HTTP.")
    except requests.RequestException as error:
        print("Eroare la pagina principala:", error)

    try:
        response = fetch(BASE_URL + "/this-page-does-not-exist")
        response.raise_for_status()
        print("10. Serverul a raspuns cu", response.status_code, "pentru calea de test.")
    except requests.HTTPError:
        print("10. Pagina ceruta nu este disponibila.")
    except requests.RequestException as error:
        print("10. Eroare de conectare:", error)

    try:
        response = fetch("http://cybercor.org")
        for old_response in response.history:
            print("17.", old_response.status_code, old_response.url)
        print("17. URL final:", response.url)
    except requests.RequestException as error:
        print("17. Eroare:", error)

    # 18: HEAD primeste antetele, iar GET primeste si corpul paginii.
    try:
        pause_between_requests()
        head_response = requests.head(BASE_URL, timeout=TIMEOUT, allow_redirects=True)
        get_response = fetch(BASE_URL)
        print("18. Corp HEAD:", len(head_response.content))
        print("18. Corp GET:", len(get_response.content))
    except requests.RequestException as error:
        print("18. Eroare:", error)

    try:
        with requests.Session() as session:
            session.headers.update({"User-Agent": "WebLab-Student"})
            pause_between_requests()
            response = session.get(ECHO_URL + "/headers", timeout=TIMEOUT)
            response.raise_for_status()
            date = response.json()
            antet = date["headers"].get("User-Agent")
            print("20. User-Agent primit:", antet)
            print("20. Antet confirmat:", antet == "WebLab-Student")
    except (requests.RequestException, KeyError) as error:
        print("20. Eroare:", error)

    # response.text este atribut. response.json() este metoda care citeste JSON.


if __name__ == "__main__":
    main()
