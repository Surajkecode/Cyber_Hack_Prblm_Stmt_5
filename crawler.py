import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import subprocess
import time
import logging
from urllib.parse import urljoin

# ✅ Update with your correct Tor path
TOR_PATH = r"C:/Users/Suraj/OneDrive/Desktop/Tor Browser/Browser/TorBrowser/Tor/tor.exe"

# ✅ Set up logging
logging.basicConfig(filename="crawler.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def start_tor():
    """Starts the Tor process and waits for it to initialize."""
    try:
        tor_process = subprocess.Popen(TOR_PATH, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(10)  # Allow time for Tor to initialize
        logging.info("✅ Tor process started successfully.")
        return tor_process
    except Exception as e:
        logging.error(f"❌ Error starting Tor: {e}")
        return None

def check_tor():
    """Checks if Tor is running by sending a request through the proxy."""
    proxies = {
        "http": "socks5h://127.0.0.1:9150",
        "https": "socks5h://127.0.0.1:9150"
    }
    try:
        print("🔍 Verifying Tor connection...")
        response = requests.get("http://check.torproject.org", proxies=proxies, timeout=10)
        if "Congratulations" in response.text:
            print("✅ Tor is working!")
            logging.info("✅ Tor is verified and working.")
            return True
        else:
            print("❌ Tor connection failed.")
            logging.error("❌ Tor connection failed.")
            return False
    except requests.exceptions.RequestException:
        print("❌ Could not connect to Tor. Is it running?")
        logging.error("❌ Could not connect to Tor.")
        return False

def crawl_website(url, max_retries=3):
    """Crawls a given .onion website using Tor."""
    tor_process = start_tor()
    if not tor_process:
        print("🛑 Exiting. Could not start Tor.")
        return

    if not check_tor():
        tor_process.terminate()
        return

    proxies = {
        "http": "socks5h://127.0.0.1:9150",
        "https": "socks5h://127.0.0.1:9150"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

    for attempt in range(max_retries):
        try:
            print(f"🔍 Attempt {attempt + 1}: Accessing {url} via Tor...")
            response = requests.get(url, headers=headers, proxies=proxies, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "html.parser")
            title = soup.title.string if soup.title else "No Title"
            links = [urljoin(url, link.get("href")) for link in soup.find_all("a", href=True)]
            text = soup.get_text()
            emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+/.[a-zA-Z]{2,}", text)
            phone_numbers = re.findall(r"/+?/d{10,15}", text)

            print(f"🌍 Website Title: {title}")
            print("🔗 Links Found:", links[:5])  # Show first 5 links
            print("📧 Emails Found:", emails[:5])  # Show first 5 emails
            print("📞 Phone Numbers Found:", phone_numbers[:5])  # Show first 5 phone numbers

            # Save extracted data
            df = pd.DataFrame({"Website": [title], "Links": [", ".join(links)], 
                               "Emails": [", ".join(emails)], "Phone Numbers": [", ".join(phone_numbers)]})
            df.to_excel("onion_data.xlsx", index=False)
            print("✅ Data saved to onion_data.xlsx")

            # Save HTML page content
            with open("onion_page.html", "w", encoding="utf-8") as file:
                file.write(response.text)
            print("📄 Page content saved as onion_page.html")

            # Run metadata extraction
            print("🚀 Running metadata.py on onion_page.html...")
            subprocess.run(["python", "metadata.py", "onion_page.html"])

            break  # Exit loop if successful

        except requests.exceptions.RequestException as e:
            print(f"❌ Error accessing {url}: {e}")
            logging.error(f"❌ Request failed: {e}")
            if attempt < max_retries - 1:
                print("🔄 Retrying in 5 seconds...")
                time.sleep(5)
            else:
                print("🛑 Max retries reached. Moving to next site.")

    tor_process.terminate()
    print("🛑 Tor process stopped.")
    logging.info("🛑 Tor process stopped.")

# ✅ Allow user to input a site or use default
default_site = "http://3g2upl4pq6kufc4m.onion"  # DuckDuckGo Onion
target_site = input(f"Enter an .onion site to crawl (or press Enter for default [{default_site}]): ") or default_site

crawl_website(target_site)