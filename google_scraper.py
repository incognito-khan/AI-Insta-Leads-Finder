import requests
from bs4 import BeautifulSoup
import re
import random
from fake_useragent import UserAgent

# Sample free proxy list (these rotate often)
proxy_list = [
    "http://103.21.163.81:6667",
    "http://190.61.88.147:8080",
    "http://185.217.143.242:8080",
    "http://103.179.109.97:3128",
    "http://138.117.84.161:8080"
]

def get_random_proxy():
    proxy = random.choice(proxy_list)
    return {"http": proxy, "https": proxy}

def search_google_instagram_profiles_with_proxy(keyword, max_results=10):
    headers = {
        "User-Agent": UserAgent().random
    }

    query = f"site:instagram.com {keyword}"
    url = f"https://www.google.com/search?q={requests.utils.quote(query)}"

    for attempt in range(5):
        proxy = get_random_proxy()
        try:
            print(f"🌐 Using proxy: {proxy['http']}")
            response = requests.get(url, headers=headers, proxies=proxy, timeout=10)

            if response.status_code != 200:
                print(f"❌ Status {response.status_code}, retrying...")
                continue

            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a')
            results = []

            for link in links:
                href = link.get('href', '')
                match = re.search(r'instagram\.com/([A-Za-z0-9_.]+)', href)
                if match:
                    username = match.group(1)
                    if username not in [r['username'] for r in results]:
                        results.append({
                            "username": username,
                            "profile_url": f"https://instagram.com/{username}",
                            "title": link.text.strip(),
                            "snippet": "N/A"
                        })
                if len(results) >= max_results:
                    break

            print(f"✅ Found {len(results)} profiles for '{keyword}'")
            return results
        except Exception as e:
            print(f"⚠️ Attempt {attempt + 1} failed: {e}")

    print("❌ All attempts failed.")
    return []
