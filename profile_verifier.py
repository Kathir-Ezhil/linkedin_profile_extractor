from selenium.webdriver.common.by import By
import time
import json

with open(
    "company_aliases.json",
    "r",
    encoding="utf-8"
) as f:

    COMPANY_ALIASES = json.load(f)


def get_all_companies(driver, profile_url):

    current_url = driver.current_url

    driver.get(profile_url)

    time.sleep(5)

    company_elements = driver.find_elements(
        By.CSS_SELECTOR,
        """
        [data-test-position-entity-company-name],
        [data-test-grouped-position-entity-company-name]
        """
    )

    companies = []

    for element in company_elements:

        company = element.text.strip()

        company = (
            company
            .replace(
                "Related to search terms in your query",
                ""
            )
            .strip()
        )

        company = company.split("·")[0].strip()

        company = company.split("\n")[0].strip()

        if (
            company
            and company not in companies
        ):
            companies.append(company)

    driver.get(current_url)

    return companies

def normalize_company(name):

    name = name.lower()

    name = name.replace(".", "")

    name = name.replace(
        "private limited",
        "pvt ltd"
    )

    name = " ".join(
        name.split()
    )

    return name


def worked_for_company(companies,target_company):

    aliases = COMPANY_ALIASES.get(
        target_company,
        [target_company]
    )


    target = (
        target_company
        .strip()
        .lower()
    )
    aliases = [

        normalize_company(alias)

        for alias in aliases
    ]


    print("\nTARGET =", repr(target))

    for company in companies:

        company_norm = normalize_company(company)

        print(
            "COMPARE:",
            repr(company_norm)
        )

        if company_norm in aliases:

            print("MATCH FOUND")

            return True

    return False