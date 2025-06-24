# bing_scraper.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
import time

def search_bing_instagram_profiles(keyword, max_results=10):
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # No GUI
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--window-size=1920,1080")

    # Optional: Set path to chromedriver if not in PATH
    service = Service("chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    query = f"site:instagram.com {keyword}"
    url = f"https://www.bing.com/search?q={query}"

    try:
        driver.get(url)
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "li.b_algo h2 a"))
            )
        except Exception as e:
            print("❌ Page didn't load results properly:", e)
            driver.save_screenshot("error.png")  # See what the page looked like
            print(driver.page_source[:2000])

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        results = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if "instagram.com" in href:
                match = re.search(r"instagram\.com/([A-Za-z0-9_.]+)", href)
                if match:
                    username = match.group(1)
                    results.append({
                        "username": username,
                        "profile_url": f"https://instagram.com/{username}",
                        "title": a.text.strip(),
                        "snippet": a.find_next('p').text.strip() if a.find_next('p') else ""
                    })
            if len(results) >= max_results:
                break

        return results

    except Exception as e:
        print(f"❌ Error while scraping Bing: {e}")
        return []

    finally:
        driver.save_screenshot("last_bing_page.png")
        driver.quit()
