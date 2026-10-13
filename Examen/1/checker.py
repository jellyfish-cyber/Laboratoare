import requests

SITES = [
    # Pagini obișnuite (Părțile 2, 3 și 4)
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    # Pagini care eșuează
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    # Anteturi de securitate (Partea 5)
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    # Răspunde aleatoriu cu 200 sau 500 (Partea 6)
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]


def build_url(host, path):
    """Returnează o adresă completă, de exemplu https://example.com/login."""
    if not path.startswith("/"):
        path = "/" + path
    return "https://" + host + path


def is_https(url):
    """Returnează True dacă adresa începe cu https://, altfel False."""
    return url.startswith("https://")


def show_response(url):
    """Trimite un GET la url și afișează statusul și Content-Type."""
    try:
        raspuns = requests.get(url, timeout=5)
        print("status:", raspuns.status_code)
        print("Content-Type:", raspuns.headers.get("Content-Type", "unknown"))
    except requests.RequestException:
        print("site-ul nu poate fi accesat.")


def check_site(url):
    """Returnează un dicționar cu: status, content_type, length, server."""
    try:
        raspuns = requests.get(url, timeout=5)
        return {
            "status": raspuns.status_code,
            "content_type": raspuns.headers.get("Content-Type", "unknown"),
            "length": len(raspuns.content),
            "server": raspuns.headers.get("Server", "unknown"),
        }
    except requests.RequestException:
        return {"status": None, "error": "site-ul este inaccesibil"}


def scan_sites():
    """Verifică toate site-urile din SITES, afișează-le pe cele care merg și un rezumat."""
    rezultate = []
    for url in SITES:
        rezultat = check_site(url)
        rezultat["url"] = url
        rezultate.append(rezultat)

    reusite = []
    for rezultat in rezultate:
        if rezultat["status"] == 200:
            reusite.append((rezultat["length"], rezultat["url"]))
    reusite.sort(reverse=True)
    for lungime, url in reusite:
        print(url, "-> 200,", lungime, "octeti")

    esuate = len(rezultate) - len(reusite)
    print("reusite:", len(reusite), "| esuate:", esuate)


def check_headers(url):
    """Returnează un dicționar cu: present, missing, score."""
    try:
        raspuns = requests.get(url, timeout=5)
        prezente = []
        lipsa = []

        for antet in SECURITY_HEADERS:
            if antet in raspuns.headers:
                prezente.append(antet)
            else:
                lipsa.append(antet)

        scor = len(prezente) * 25
        return {"present": prezente, "missing": lipsa, "score": scor}
    except requests.RequestException:
        return {"status": None, "error": "site inaccesibil"}


def retry_check(url, attempts=3):
    """Încearcă de cel mult `attempts` ori; returnează un dicționar cu: status, attempts."""
    rezultat = {"status": None, "attempts": 0}
    for incercare in range(1, attempts + 1):
        verificare = check_site(url)
        rezultat = {"status": verificare["status"], "attempts": incercare}
        if verificare["status"] is None:
            rezultat["error"] = verificare["error"]
            return rezultat

        if verificare["status"] < 500:
            break

    return rezultat
