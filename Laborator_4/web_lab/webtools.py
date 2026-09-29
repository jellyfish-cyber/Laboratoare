# Laborator: functii, metode si importuri pe web
# Student: necompletat

import requests
import time
import re
import json
import hashlib
import socket
import ssl
import html as html_module
from datetime import datetime
from urllib.parse import urlparse, urljoin
from html.parser import HTMLParser

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10
DEFAULT_HEADERS = {"User-Agent": "WebLab-Student"}

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy"
]


def pause_between_requests():
    """Asteapta o secunda inainte de cerere."""
    time.sleep(1)


def fetch(url: str, timeout: int = 10) -> requests.Response:
    """21, 23: descarca pagina si returneaza raspunsul."""
    pause_between_requests()
    domeniu = urlparse(str(url)).hostname
    if domeniu == "httpbin.org":
        response = requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)
    else:
        response = requests.get(url, timeout=timeout)
    return response


def get_status(url: str) -> int:
    """22, 26: returneaza codul HTTP al paginii."""
    response = fetch(url)
    return response.status_code


def get_title(html: str) -> str:
    """24, 25: extrage textul dintre tagurile title."""
    text_mic = html.lower()
    start = text_mic.find("<title>")
    end = text_mic.find("</title>", start)
    if start == -1 or end == -1:
        return ""
    start = start + len("<title>")
    titlu = html[start:end].strip()
    return html_module.unescape(titlu)


def page_exists(url: str) -> bool:
    """27: verifica pagina fara sa opreasca programul la o eroare de retea."""
    try:
        response = fetch(url)
        return response.ok
    except requests.RequestException:
        return False


def check_paths(base, paths):
    """28: returneaza codul HTTP pentru fiecare cale primita."""
    rezultate = {}
    for path in paths:
        url = urljoin(base, path)
        try:
            rezultate[path] = get_status(url)
        except requests.RequestException:
            rezultate[path] = None
    return rezultate


def get_header(url, name, default="lipsește"):
    """29: returneaza un antet sau valoarea implicita."""
    response = fetch(url)
    return response.headers.get(name, default)


def security_headers(url):
    """30: verifica prezenta celor cinci antete de securitate."""
    response = fetch(url)
    rezultate = {}
    for name in SECURITY_HEADERS:
        rezultate[name] = name in response.headers
    return rezultate


def score_headers(results):
    """31: numara antetele prezente si returneaza scorul."""
    prezente = 0
    for name in results:
        if results[name]:
            prezente = prezente + 1
    return str(prezente) + "/" + str(len(results))


def fetch_robots(base):
    """32: citeste robots.txt sau returneaza None daca nu este disponibil."""
    url = urljoin(base, "/robots.txt")
    try:
        response = fetch(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException:
        return None


def disallowed_paths(robots_text):
    """32: extrage valorile Disallow din robots.txt."""
    paths = []
    if robots_text is None:
        return paths
    for line in robots_text.splitlines():
        line = line.split("#")[0].strip()
        if line.lower().startswith("disallow:"):
            path = line.split(":", 1)[1].strip()
            if path != "" and path not in paths:
                paths.append(path)
    return paths


def response_times(*urls):
    """33: masoara durata fiecarei cereri, fara pauza de o secunda."""
    rezultate = {}
    for url in urls:
        pause_between_requests()
        start = time.perf_counter()
        try:
            requests.get(url, timeout=TIMEOUT)
            end = time.perf_counter()
            rezultate[url] = end - start
        except requests.RequestException:
            rezultate[url] = None
    return rezultate


def log(message, **details):
    """34: afiseaza mesajul si detaliile primite."""
    text = message
    for name in details:
        text = text + " | " + name + "=" + str(details[name])
    print(text)


def parse_url(url):
    """35: returneaza partile unui URL."""
    rezultat = urlparse(url)
    return {
        "scheme": rezultat.scheme,
        "netloc": rezultat.netloc,
        "path": rezultat.path,
        "query": rezultat.query,
        "fragment": rezultat.fragment
    }


def join_urls(base, links):
    """36: transforma legaturile relative in URL-uri complete."""
    rezultate = []
    for link in links:
        rezultate.append(urljoin(base, link))
    return rezultate


def extract_links(html):
    """37: extrage legaturile href, fara duplicate."""
    legaturi = re.findall(r'href="([^"]+)"', html)
    rezultate = []
    for link in legaturi:
        link = html_module.unescape(link)
        if link not in rezultate:
            rezultate.append(link)
    return rezultate


def split_links(links, domain):
    """38: imparte legaturile in interne si externe."""
    if "://" not in domain:
        domain = "https://" + domain
    domeniu = urlparse(domain).netloc
    interne = []
    externe = []
    for link in links:
        url = urljoin(domain, link)
        parts = urlparse(url)
        if parts.scheme == "http" or parts.scheme == "https":
            if parts.netloc == domeniu:
                if url not in interne:
                    interne.append(url)
            else:
                if url not in externe:
                    externe.append(url)
    return interne, externe


class ImageFinder(HTMLParser):
    def __init__(self):
        """Pregateste lista de imagini."""
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        """Adauga src pentru fiecare tag img care il contine."""
        if tag == "img":
            atribute = dict(attrs)
            src = atribute.get("src")
            if src is not None:
                self.images.append(src)


def page_fingerprint(url):
    """40: calculeaza SHA-256 pentru continutul paginii."""
    response = fetch(url)
    amprenta = hashlib.sha256(response.content)
    return amprenta.hexdigest()


def save_headers(url, path="headers.json"):
    """41: salveaza antetele in JSON si le citeste inapoi."""
    response = fetch(url)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(dict(response.headers), file, indent=2)
    with open(path, "r", encoding="utf-8") as file:
        antete = json.load(file)
    return antete


def resolve(hostname):
    """42: returneaza adresa IPv4 a domeniului."""
    return socket.gethostbyname(hostname)


def cert_days_left(hostname):
    """43: calculeaza zilele ramase pana la expirarea certificatului."""
    pause_between_requests()
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443), timeout=TIMEOUT) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as connection:
            certificat = connection.getpeercert()
    secunde = ssl.cert_time_to_seconds(certificat["notAfter"])
    data_expirarii = datetime.utcfromtimestamp(secunde)
    zile_ramase = data_expirarii - datetime.utcnow()
    return zile_ramase.days


def site_report(url, output="report.json"):
    """50: aduna informatiile despre site si salveaza raportul."""
    parts = urlparse(url)
    if parts.scheme not in ["http", "https"] or parts.hostname is None:
        raise ValueError("Scrie un URL complet, cu http:// sau https://.")

    raport = {
        "url": url,
        "checked_at": datetime.now().isoformat(),
        "status": None,
        "final_url": None,
        "title": None,
        "ip": None,
        "redirects": None,
        "redirect_final_url": None,
        "security_headers": None,
        "security_score": None,
        "certificate_days_left": None,
        "internal_links": None,
        "external_links": None,
        "disallowed_paths": None,
        "errors": {}
    }

    try:
        response = fetch(url)
        raport["status"] = response.status_code
        raport["final_url"] = response.url
        raport["title"] = get_title(response.text)
        links = extract_links(response.text)
        interne, externe = split_links(links, response.url)
        raport["internal_links"] = len(interne)
        raport["external_links"] = len(externe)
    except requests.RequestException as error:
        raport["errors"]["page"] = str(error)

    try:
        raport["ip"] = resolve(parts.hostname)
    except OSError as error:
        raport["errors"]["ip"] = str(error)

    try:
        antete = security_headers(url)
        raport["security_headers"] = antete
        raport["security_score"] = score_headers(antete)
    except requests.RequestException as error:
        raport["errors"]["security_headers"] = str(error)

    try:
        raport["certificate_days_left"] = cert_days_left(parts.hostname)
    except (OSError, ValueError) as error:
        raport["errors"]["certificate"] = str(error)

    try:
        http_url = url.replace("https://", "http://", 1)
        response = fetch(http_url)
        redirectari = []
        for old_response in response.history:
            redirectari.append({
                "status": old_response.status_code,
                "url": old_response.url,
                "location": old_response.headers.get("Location")
            })
        raport["redirects"] = redirectari
        raport["redirect_final_url"] = response.url
    except requests.RequestException as error:
        raport["errors"]["redirects"] = str(error)

    robots = fetch_robots(url)
    if robots is not None:
        raport["disallowed_paths"] = disallowed_paths(robots)
    else:
        raport["errors"]["robots"] = "robots.txt nu este disponibil"

    with open(output, "w", encoding="utf-8") as file:
        json.dump(raport, file, indent=2, ensure_ascii=False)

    print("Raport pentru:", url)
    print("Cod HTTP:", raport["status"])
    print("URL final:", raport["final_url"])
    print("Titlu:", raport["title"])
    print("IP:", raport["ip"])
    print("Redirectionari:", raport["redirects"])
    print("Scor antete:", raport["security_score"])
    print("Zile certificat:", raport["certificate_days_left"])
    print("Legaturi interne:", raport["internal_links"])
    print("Legaturi externe:", raport["external_links"])
    print("Cai interzise:", raport["disallowed_paths"])
    if raport["errors"] != {}:
        print("Erori:", raport["errors"])
    print("Salvat in", output)
    return raport


if __name__ == "__main__":
    # 46: acest bloc nu ruleaza cand modulul este importat.
    try:
        print("Autotest:", get_status(BASE_URL))
    except requests.RequestException as error:
        print("Nu am putut accesa site-ul:", error)
