import json
import os
import pandas as pd
from datetime import datetime
from prompt_builder import build_prompt

from scraper import (
    LinkedInScraper
)

from config import (
    OUTPUT_FILE
)

os.makedirs(
    "output",
    exist_ok=True
)

with open(
    "searches.json",
    "r",
    encoding="utf-8"
) as f:

    searches = json.load(f)


scraper = LinkedInScraper()

all_profiles = []

for search in searches:

    prompt = build_prompt(search)

    print(
        "\n===================="
    )

    print(
        f"Processing: "
        f"{search['company']}"
    )

    print(
        "===================="
    )
    prompt = build_prompt(search)
    profiles = (scraper.scrape_search_url(prompt))

    for profile in profiles:

        profile[
            "source_company"
        ] = search["company"]

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

# store scrap time as a column
scrape_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
df["scraped_at"] = scrape_time

#to csv
df.to_csv("output/profiles.csv", index=False, encoding="utf-8-sig")
print("\nSaved: output/profiles.csv")

#to excel
df.to_excel("output/profiles.xlsx", index=False)
print("\nSaved: output/profiles.xlsx")

print(
    f"TOTAL PROFILES: "
    f"{len(all_profiles)}"
)
