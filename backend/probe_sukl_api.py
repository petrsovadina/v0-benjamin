import requests
import sys

BASE_URL = "https://testapi.sukl.cz"

POSSIBLE_SWAGGER_PATHS = [
    "/swagger",
    "/swagger/index.html",
    "/swagger-ui.html",
    "/api/docs",
    "/docs",
    "/cis/swagger",
    "/cis/docs"
]

def probe_url(path):
    url = f"{BASE_URL}{path}"
    try:
        response = requests.get(url, timeout=5, verify=False)
        print(f"[{response.status_code}] {url} (Content-Type: {response.headers.get('Content-Type')})")
        if response.status_code == 200:
            return True
    except Exception as e:
        print(f"[ERR] {url}: {e}")
    return False

print(f"Probing {BASE_URL} for API documentation...")
found = False
for path in POSSIBLE_SWAGGER_PATHS:
    if probe_url(path):
        found = True

if not found:
    print("No obvious Swagger/Docs path found.")
    # Try fetching the root page content again to find links
    try:
        r = requests.get(BASE_URL, verify=False)
        print(f"\nRoot page content snippet:\n{r.text[:500]}")
    except Exception as e:
        print(f"Failed to fetch root: {e}")
