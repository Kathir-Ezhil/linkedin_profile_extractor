from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.keys import Keys
import time

from config import (
    PROFILE_DIR,
    PAGE_LOAD_WAIT,
    SCROLL_WAIT
)


class LinkedInScraper:

    def __init__(self):

        options = Options()

        options.add_argument(
            f"--user-data-dir={PROFILE_DIR}"
        )

        self.driver = webdriver.Edge(
            options=options
        )

    # ==================================
    # OPEN SEARCH
    # ==================================

    def open_search(self, search_url):

        self.driver.get(search_url)

        print("Opening LinkedIn Recruiter...")

        time.sleep(PAGE_LOAD_WAIT)

    # ==================================
    # EXTRACT VISIBLE PROFILES
    # ==================================

    def extract_visible_profiles(
        self,
        profiles
    ):

        cards = self.driver.find_elements(
            By.CSS_SELECTOR,
            "li[data-test-paginated-profile-list-item-container]"
        )

        print(
            f"Visible cards: {len(cards)}"
        )

        for card in cards:

            try:

                name_elements = card.find_elements(
                    By.CSS_SELECTOR,
                    "[data-test-row-lockup-full-name] a"
                )

                if not name_elements:
                    continue

                name_el = name_elements[0]

                profile_url = (
                    name_el.get_attribute("href")
                )

                if profile_url in profiles:
                    continue

                name = name_el.text.strip()

                title = ""
                location = ""
                company = ""
                open_to_work = False

                # --------------------
                # TITLE
                # --------------------

                try:

                    title = (
                        card.find_element(
                            By.CSS_SELECTOR,
                            "[data-test-row-lockup-headline]"
                        )
                        .text
                        .strip()
                    )

                except:
                    pass

                # --------------------
                # LOCATION
                # --------------------

                try:

                    location = (
                        card.find_element(
                            By.CSS_SELECTOR,
                            "[data-test-row-lockup-location]"
                        )
                        .text
                        .strip()
                    )

                except:
                    pass

                # --------------------
                # COMPANY
                # --------------------

                try:

                    exp_items = (
                        card.find_elements(
                            By.CSS_SELECTOR,
                            "li[data-test-description-description]"
                        )
                    )

                    if exp_items:

                        first_exp = (
                            exp_items[0].text
                        )

                        if " at " in first_exp:

                            company = (
                                first_exp
                                .split(" at ")[1]
                                .split("·")[0]
                                .strip()
                            )

                except:
                    pass

                # --------------------
                # OPEN TO WORK
                # --------------------

                open_to_work = False

                try:

                    otw = card.find_elements(
                        By.CSS_SELECTOR,
                        '[data-live-test-decoration-type="openToOpportunities"]'
                    )

                    open_to_work = len(otw) > 0

                except:
                    pass

                profiles[profile_url] = {

                    "name": name,

                    "title": title,

                    "company": company,

                    "location": location,

                    "open_to_work": open_to_work,

                    "profile_url": profile_url
                }

                print(
                    f"Collected: {name}"
                )

            except Exception:
                pass

    # ==================================
    # SCRAPE PAGE
    # ==================================

    def scrape_current_page(
        self,
        profiles
    ):

        previous_count = -1

        no_change_count = 0

        while True:

            self.extract_visible_profiles(
                profiles
            )

            current_count = len(
                profiles
            )

            print(
                f"Current total: {current_count}"
            )

            if (
                current_count
                == previous_count
            ):

                no_change_count += 1

            else:

                no_change_count = 0

            if no_change_count >= 5:

                print(
                    "Reached end of page."
                )

                break

            previous_count = current_count

            self.driver.execute_script(
                "window.scrollBy(0,1000);"
            )

            time.sleep(
                SCROLL_WAIT
            )

    # ==================================
    # SCRAPE SEARCH URL
    # ==================================

    def scrape_search_url(self,prompt):

        profiles = {}

        self.search_company(prompt)

        # -----------------
        # PAGE 1
        # -----------------

        print(
            "\n===== PAGE 1 ====="
        )

        self.scrape_current_page(
            profiles
        )

        print(
            f"\nPage 1 Complete -> "
            f"{len(profiles)} profiles"
        )

        # -----------------
        # PAGE 2
        # -----------------

        try:

            next_btn = (
                self.driver.find_element(
                    By.CSS_SELECTOR,
                    "[data-test-pagination-next]"
                )
            )

            self.driver.execute_script(
                "arguments[0].click();",
                next_btn
            )

            time.sleep(8)

            self.driver.execute_script(
                "window.scrollTo(0,0);"
            )

            time.sleep(2)

            print(
                "\n===== PAGE 2 ====="
            )

            self.scrape_current_page(
                profiles
            )

        except Exception as e:

            print(
                "No next page"
            )

            print(e)

        return list(
            profiles.values()
        )
    def search_company(self, prompt):

        self.driver.get(
            "https://www.linkedin.com/talent/home"
        )

        time.sleep(8)

        search_box = self.driver.find_element(
            By.CSS_SELECTOR,
            "[data-test-copilot-chat-input]"
        )

        search_box.clear()

        search_box.send_keys(prompt)

        time.sleep(1)

        search_box.send_keys(Keys.ENTER)

        print(
            f"Searching: {prompt}"
        )

        time.sleep(10)

    # ==================================
    # CLOSE DRIVER
    # ==================================


    def close(self):

        self.driver.quit()