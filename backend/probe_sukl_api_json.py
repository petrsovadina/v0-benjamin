import requests

BASE_URL = "https://testapi.sukl.cz"

POSSIBLE_JSON_PATHS = [
    "/swagger/v1/swagger.json",
    "/v1/swagger.json",
    "/api-docs",
    "/docs/swagger.json",
    "/swagger.json",
    "/cis/swagger/v1/swagger.json",
    "/lek13/swagger/v1/swagger.json"
]

def probe_url(path):
    url = f"{BASE_URL}{path}"
    try:
        response = requests.get(url, timeout=5, verify=False)
        ct = response.headers.get('Content-Type', '')
        print(f"[{response.status_code}] {url} (Content-Type: {ct})")
        if response.status_code == 200 and ('json' in ct):
            return True
            print(f"FOUND JSON: {response.text[:100]}...")
    except Exception as e:
        print(f"[ERR] {url}: {e}")
    return False

print(f"Probing JSON specs on {BASE_URL}...")
for path in POSSIBLE_JSON_PATHS:
    if probe_url(path):
        break
