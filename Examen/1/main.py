from checker import SITES, build_url, is_https, show_response
from checker import check_site, scan_sites, check_headers, retry_check


print("Partea 1")
gazda = SITES[0].replace("https://", "")
print("URL fara /:", build_url(gazda, "login"))
print("URL cu /:", build_url(gazda, "/login"))
print("HTTPS:", is_https(SITES[0]))
print("HTTP:", is_https(SITES[9]))

print("\nPartea 2")
show_response(SITES[0])
print("site inexistent")
show_response(SITES[9])

print("\nPartea 3")
for url in SITES:
    print(url, "->", check_site(url))

print("\nPartea 4")
scan_sites()

print("\nPartea 5")
print("Antete:", check_headers(SITES[10]))
print("Eroare:", check_headers(SITES[9]))

print("\nPartea 6")
print("Status 200:", retry_check(SITES[3]))
print("Status 404:", retry_check(SITES[6]))
print("Status 500:", retry_check(SITES[7], 2))
print("Site inexistent:", retry_check(SITES[9]))
