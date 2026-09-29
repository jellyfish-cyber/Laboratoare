# Laborator: functii, metode si importuri pe web
# Student: necompletat

import requests
from webtools import fetch, get_status, get_title, page_exists, check_paths
from webtools import get_header, security_headers, score_headers
from webtools import fetch_robots, disallowed_paths, response_times, log

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10


def main():
    """Apeleaza functiile pentru exercitiile 21-34."""
    try:
        response = fetch(BASE_URL)
        print("21. Cod HTTP:", response.status_code)
        print("24. Titlu:", get_title(response.text))
        response = fetch(BASE_URL, timeout=3)
        print("23. Cod HTTP cu timeout=3:", response.status_code)
    except requests.RequestException as error:
        print("21-24. Eroare:", error)

    paths = ["/", "/robots.txt", "/sitemap.xml"]
    for path in paths:
        try:
            status = get_status(BASE_URL + path)
            print("22.", path, status)
        except requests.RequestException as error:
            print("22.", path, error)

    print("24. Titlu de test:", get_title("<title> Test </title>"))
    help(get_title)

    # 26: adnotarile nu opresc apelul. requests respinge URL-ul numeric.
    try:
        print("26.", get_status(123))
    except requests.RequestException as error:
        print("26. Argumentul nu este un URL valid:", error)

    print("27. Domeniu invalid:", page_exists("https://this-domain-does-not-exist.invalid"))
    print("28. Cai:", check_paths(BASE_URL, paths))

    try:
        antet = get_header(BASE_URL, name="Server")
        print("29. Server:", antet)
        antete = security_headers(BASE_URL)
        print("30. Antete de securitate:", antete)
        print("31. Scor:", score_headers(antete))
    except requests.RequestException as error:
        print("29-31. Eroare:", error)

    robots = fetch_robots(BASE_URL)
    print("32. robots.txt:", robots)
    print("32. Cai Disallow:", disallowed_paths(robots))
    print("33. Timpi:", response_times(BASE_URL, BASE_URL + "/robots.txt"))
    log("34. verificat", url=BASE_URL, status="vezi rezultatele")
    # print afiseaza pe ecran. return da rezultatul codului care a apelat functia.


if __name__ == "__main__":
    main()
