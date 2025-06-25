import requests
import re
import pandas as pd
import time

# ✅ Replace these with your real Oxylabs credentials
OXYLABS_USERNAME = "abdullah_Mv080"
OXYLABS_PASSWORD = "Abdullah_123~4"

classifier_keywords = ["founder", "ceo", "owner", "co-founder", "co-owner", "founding partner", "partner", "director", "president", "chief executive officer", "chief operating officer", "chief financial officer", "chief marketing officer", "chief technology officer"]

# API endpoint
OX_API = "https://realtime.oxylabs.io/v1/queries"

def fetch_google_results(query, retries=3):
    search_url = f"https://www.google.com/search?q=site:instagram.com+{query}"
    payload = {
        "source": "google",
        "url": search_url,
        "render": "html"
    }

    for attempt in range(1, retries + 1):
        try:
            response = requests.post(
                OX_API,
                auth=(OXYLABS_USERNAME, OXYLABS_PASSWORD),
                json=payload,
                timeout=60
            )

            if response.status_code == 200:
                return response.text
            else:
                print(f"Error: {response.status_code} - {response.text}")
                time.sleep(5)
        except Exception as e:
            print(f"Request failed on attempt {attempt}: {e}")
            time.sleep(5)

    return None

def extract_instagram_profiles(html, max_results=10):
    matches = re.findall(r"instagram\.com/([A-Za-z0-9_.]+)", html)
    unique_usernames = list(dict.fromkeys(matches))  # Removes duplicates, keeps order
    leads = []
    for username in unique_usernames[:max_results]:
        leads.append({
            "username": username,
            "profile_url": f"https://instagram.com/{username}"
        })
    return leads

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

# Run it
niche = input("Enter a niche (e.g., 'fitness coach', 'business mentor'): ").strip()
niches = [niche]
leads = find_instagram_leads(niches)

# Save to CSV
if leads:
    df = pd.DataFrame(leads)
    df.to_csv("instagram_leads.csv", index=False)
    print("✅ Leads saved to instagram_leads.csv")
else:
    print("❌ No leads found.")
