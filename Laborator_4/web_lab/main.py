# Laborator: functii, metode si importuri pe web
# Student: necompletat

import os
import argparse
import csv
from datetime import datetime
import webtools
from webtools import get_title, security_headers, DEFAULT_HEADERS

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10

# 45: daca definesc aici alta functie get_title, numele importat este inlocuit.
# webtools.get_title ramane functia din modul.


def main():
    """44-50: importa modulul propriu si creeaza rapoartele."""
    parser = argparse.ArgumentParser(description="Raport despre un site web")
    parser.add_argument("url", nargs="?", default=BASE_URL)
    args = parser.parse_args()
    url = args.url
    folder = os.path.dirname(os.path.abspath(__file__))

    print("47. DEFAULT_HEADERS:", DEFAULT_HEADERS)
    try:
        response = webtools.fetch(url)
        print("44. Titlu prin modul:", webtools.get_title(response.text))
        print("45. Titlu prin import direct:", get_title(response.text))
        print("45. Antete prin import direct:", security_headers(url))
    except webtools.requests.RequestException as error:
        print("Nu am putut citi pagina:", error)

    paths = ["/", "/robots.txt", "/sitemap.xml"]
    rezultate = webtools.check_paths(url, paths)
    cale_csv = os.path.join(folder, "report.csv")
    with open(cale_csv, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["path", "status", "checked_at"])
        for path in rezultate:
            writer.writerow([path, rezultate[path], datetime.now().isoformat()])

    cale_json = os.path.join(folder, "report.json")
    webtools.site_report(url, cale_json)


if __name__ == "__main__":
    main()
