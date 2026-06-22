import json
import os
import sys
import pandas as pd
from datetime import datetime
from prompt_builder import build_prompt
from profile_verifier import get_all_companies, worked_for_company
from scraper import LinkedInScraper
from config import OUTPUT_FILE, PROFILE_DIR, PAGE_LOAD_WAIT, SCROLL_WAIT, run_timestamp


os.makedirs("output",exist_ok=True)

if len(sys.argv) < 2:

    print("Usage: python main.py <config_file>")

    exit()

config_file = sys.argv[1]

with open(config_file,"r", encoding="utf-8") as f:

    searches = json.load(f)

print(f"\nLoading Config: "f"{config_file}\n")

scraper = LinkedInScraper()

all_profiles = []

for search in searches:

    prompt = build_prompt(search)

    print("\n====================")

    print(f"Processing: {search['company']}")

    print( "====================")

    profiles = (scraper.scrape_search_url(prompt))

    # =====================================
    # Exact company match for CURRENT searches
    # =====================================

    if search["employment_type"] == "current":

        target_company = (search["company"].strip().lower())
        before_count = len(profiles)

        profiles = [profile for profile in profiles if (profile.get("company", "").strip().lower()== target_company)]

        print(f"Current company filter: {before_count} -> {len(profiles)}")
    
    elif (search["employment_type"]== "past"):

        before_count = len(profiles)
        verified_profiles = []
        for profile in profiles:

            print(
                f"Verifying: "
                f"{profile['name']}"
            )

            companies = get_all_companies(
                scraper.driver,
                profile["profile_url"]
            )

            profile["all_companies"] = companies

            if worked_for_company(companies,search["company"]):

                verified_profiles.append(profile)
                

        profiles = verified_profiles

        print(
            f"Past company filter: "
            f"{before_count} -> "
            f"{len(profiles)}"
        )

    # =====================================
    # Add metadata
    # =====================================

    for profile in profiles:

        profile["source_company"] = (
            search["company"]
        )

        profile["employment_type"] = (
            search["employment_type"]
        )

        profile["search_prompt"] = (
            prompt
        )

    all_profiles.extend(
        profiles
    )

scraper.close()

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        all_profiles,
        f,
        indent=2,
        ensure_ascii=False
    )

print(
    "\n===================="
)

print(
    f"Saved: "
    f"{OUTPUT_FILE}"
)

print(
    "===================="
)

# convert to dataframe using pandas
df = pd.DataFrame(all_profiles)

#deduplication based on profile_url
unique_profiles = {}

for profile in all_profiles:

    unique_profiles[
        profile["profile_url"]
    ] = profile

all_profiles = list(
    unique_profiles.values()
)

print(
    f"\nAfter Deduplication: "
    f"{len(all_profiles)} profiles"
)

# store scrap time as a column
scrape_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
df["scraped_at"] = scrape_time

#to csv
csv_file = (f"output/profiles_{run_timestamp}.csv")

df.to_csv(csv_file, index=False, encoding="utf-8-sig")
print(f"\nSaved: {csv_file}")

#to excel
excel_file = ( f"output/profiles_{run_timestamp}.xlsx")
df.to_excel(excel_file, index=False)
print(f"\nSaved: {excel_file}")

print(
    f"TOTAL PROFILES: "
    f"{len(all_profiles)}"
)
