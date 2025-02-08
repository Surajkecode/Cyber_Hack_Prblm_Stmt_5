import requests

proxies = {
    "http": "socks5h://127.0.0.1:9050",
    "https": "socks5h://127.0.0.1:9050",
}

try:
    response = requests.get("http://check.torproject.org", proxies=proxies)
    print(response.text)
except requests.exceptions.RequestException as e:
    print(f"❌ Tor connection failed: {e}")
