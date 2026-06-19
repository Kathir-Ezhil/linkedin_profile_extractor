from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options
import time

PROFILE_DIR = r"D:\linkedin_automation\edge_profile"

options = Options()
options.add_argument(
    f"--user-data-dir={PROFILE_DIR}"
)

driver = webdriver.Edge(options=options)

driver.get(
    "https://www.linkedin.com/talent/home"
)

time.sleep(10)

search_box = driver.find_element(
    By.CSS_SELECTOR,
    '[data-test-copilot-chat-input]'
)

search_box.clear()

prompt = (
    "Current employees of Zoho who are open to work"
)

search_box.send_keys(prompt)

time.sleep(2)

search_box.send_keys(Keys.ENTER)

print("Prompt submitted")

input("Press Enter...")