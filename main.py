# main.py

import pandas as pd
from google_scraper import search_google_instagram_profiles_with_proxy as search_instagram_profiles

def classify_lead(snippet, title, keywords):
    text = (snippet + " " + title).lower()
    return any(kw.lower() in text for kw in keywords)

def find_instagram_leads(niches, classifier_keywords, max_results=10):
    all_leads = []
    for niche in niches:
        print(f"🔍 Searching for niche: {niche}")
        profiles = search_instagram_profiles(niche, max_results=max_results)
        print(f"✅ Found {len(profiles)} profiles for '{niche}'")
        for profile in profiles:
            if classify_lead(profile["snippet"], profile["title"], classifier_keywords):
                all_leads.append(profile)
    return all_leads

if __name__ == "__main__":
    niches = ["fitness coach", "yoga instructor", "vegan chef"]
    classifier_keywords = ["coach", "instructor", "entrepreneur", "chef", "vegan", "plant-based", "nutrition", "recipes"]

    leads = find_instagram_leads(niches, classifier_keywords, max_results=10)

    df = pd.DataFrame(leads)
    df.to_csv("instagram_leads.csv", index=False)
    print("✅ Leads saved to instagram_leads.csv")
