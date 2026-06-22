from scraper import LinkedInScraper
from profile_verifier import get_all_companies

scraper = LinkedInScraper()

profile_url = "https://www.linkedin.com/talent/profile/AEMAABTSimEB9iYKflRLae1OGy1oT0Z14spmNtc?searchHistoryId=21183512676&highlightedPatternSource=%255CbSSG%2520Consulting%2520Pvt%2520Ltd%255Cb&trk=SEARCH_GLOBAL"

companies = get_all_companies(
    scraper.driver,
    profile_url
)

print("\nCOMPANIES:\n")

for company in companies:
    print(company)

scraper.close()