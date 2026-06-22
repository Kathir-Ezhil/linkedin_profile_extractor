from datetime import datetime
run_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")


PROFILE_DIR = PROFILE_DIR = r"D:\linkedin_automation\edge_profile_test"

OUTPUT_FILE = f"output/profiles_{run_timestamp}.json"

PAGE_LOAD_WAIT = 10

SCROLL_WAIT = 2

HEADLESS = False