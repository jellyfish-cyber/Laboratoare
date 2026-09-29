# Laborator: functii, metode si importuri pe web
# Student: necompletat

import os
import requests
from webtools import parse_url, join_urls, extract_links, split_links
from webtools import ImageFinder, page_fingerprint, save_headers
from webtools import resolve, cert_days_left, fetch

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10


def test_image_finder():
    """39: verifica parserul pe fragmentul HTML din fisa."""
    html = '''<html><body>
      <img src="/logo.png" alt="Logo">
      <IMG SRC="poza.jpg">
      <img alt="imagine fara src">
      <img src="https://cdn.example.com/banner.webp" />
      <a href="/despre">Aceasta nu este o imagine</a>
    </body></html>'''
    finder = ImageFinder()
    finder.feed(html)
    print("39. Imagini de test:", finder.images)
    assert finder.images == ["/logo.png", "poza.jpg", "https://cdn.example.com/banner.webp"]
    print("39. Testul a trecut!")


def main():
    """Rezolvarile exercitiilor 35-43."""
    parts = parse_url(BASE_URL + "/path?x=1#top")
    print("35. Partile URL-ului:", parts)
    links = ["/about", "contact.html", "../index.html"]
    print("36. URL-uri complete:", join_urls(BASE_URL, links))

    test_image_finder()
    try:
        response = fetch(BASE_URL)
        links = extract_links(response.text)
        print("37. Legaturi:", links)
        interne, externe = split_links(links, BASE_URL)
        print("38. Interne:", interne)
        print("38. Externe:", externe)
        finder = ImageFinder()
        finder.feed(response.text)
        print("39. Numar de imagini:", len(finder.images))
        print("39. Numar de taguri img:", response.text.lower().count("<img"))
        for src in finder.images:
            print(src)
    except requests.RequestException as error:
        print("37-39. Eroare:", error)

    try:
        prima = page_fingerprint(BASE_URL)
        a_doua = page_fingerprint(BASE_URL)
        print("40. Prima amprenta:", prima)
        print("40. A doua amprenta:", a_doua)
        print("40. Sunt egale:", prima == a_doua)
        # Amprentele difera daca se modifica octetii paginii.
    except requests.RequestException as error:
        print("40. Eroare:", error)

    try:
        folder = os.path.dirname(os.path.abspath(__file__))
        cale = os.path.join(folder, "headers.json")
        antete = save_headers(BASE_URL, cale)
        print("41. Antet recitit:", antete.get("Content-Type", "lipsește"))
    except requests.RequestException as error:
        print("41. Eroare:", error)

    try:
        print("42. IP:", resolve("cybercor.org"))
    except OSError as error:
        print("42. Eroare DNS:", error)

    try:
        print("43. Zile certificat:", cert_days_left("cybercor.org"))
    except (OSError, ValueError) as error:
        print("43. Eroare TLS:", error)
    # feed() apeleaza automat handle_starttag() cand gaseste un tag.


if __name__ == "__main__":
    main()
