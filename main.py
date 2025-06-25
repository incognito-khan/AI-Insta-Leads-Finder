import requests
import pandas as pd
import re
from bs4 import BeautifulSoup
import time
import instaloader

# ========== CONFIG ==========
OXYLABS_USERNAME = "abdullah_Mv080"
OXYLABS_PASSWORD = "Abdullah_123~4"
MAX_RESULTS = 10
COOLDOWN_SECONDS = 5
# ============================

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json"
}

loader = instaloader.Instaloader()

def fetch_google_results(niche):
    query = f"site:instagram.com {niche}"
    payload = {
        "source": "google",
        "url": f"https://www.google.com/search?q={query}",
        "render": "html"
    }

    response = requests.post(
        "https://realtime.oxylabs.io/v1/queries",
        auth=(OXYLABS_USERNAME, OXYLABS_PASSWORD),
        json=payload
    )

    if response.status_code == 200:
        return response.text
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def extract_instagram_profiles(html, max_results=10):
    matches = re.findall(r'instagram\.com/([A-Za-z0-9_.]+)', html)
    unique_usernames = list(dict.fromkeys(matches))
    leads = []

    for username in unique_usernames:
        if username.lower() in ["reel", "tv", "p", "explore", "stories"]:
            continue

        profile_url = f"https://instagram.com/{username}"
        email, website, phone = get_contact_info_from_bio(username)
        time.sleep(COOLDOWN_SECONDS)

        leads.append({
            "username": username,
            "profile_url": profile_url,
            "email": email,
            "website": website,
            "phone": phone
        })

        if len(leads) >= max_results:
            break

        time.sleep(1.5)

    return leads


def get_contact_info_from_bio(username):
    try:
        profile = instaloader.Profile.from_username(loader.context, username)
        bio = profile.biography

        # Extract email
        email_match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", bio)
        email = email_match.group(0) if email_match else ""

        # Extract website
        url_match = re.search(
            r'(?<!@)\b(?:https?://|www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:\.[a-zA-Z]{2,})?(?:/[^\s]*)?',
            bio
        )
        website = url_match.group(0).rstrip(".,") if url_match else ""

        # Extract phone number from wa.me or tel: or plain number
        phone_match = re.search(r'(?:wa\.me/|tel:)?(\+?\d[\d\s\-()]{7,})', bio)
        phone = phone_match.group(1).strip() if phone_match else ""

        return email, website, phone

    except Exception as e:
        print(f"Error fetching {username}: {e}")
        return "", "", ""


def find_instagram_leads(niches, max_results=10):
    all_leads = []
    for niche in niches:
        print(f"\nSearching for: {niche}")
        html = fetch_google_results(niche)
        if html:
            leads = extract_instagram_profiles(html, max_results)
            print(f"Found {len(leads)} profiles for '{niche}'")
            for lead in leads:
                lead["niche"] = niche
            all_leads.extend(leads)
        else:
            print(f"No results for '{niche}'")
    return all_leads

# ========= MAIN ==========
niche_input = input("Enter a single niche to search (e.g., 'fitness coach'): ").strip()

if not niche_input or "," in niche_input:
    print("Please enter only one niche (no commas).")
    exit()

niches = [niche_input]

leads = find_instagram_leads(niches)

if leads:
    df = pd.DataFrame(leads)
    df.to_csv("instagram_leads.csv", index=False)
    print("Leads saved to instagram_leads.csv")
else:
    print("No leads found.")
