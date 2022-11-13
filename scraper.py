from wrappers.indeed_wrapper import extract_first_n_page_result, filter_result_by_posted_dates
from wrappers.selenium_wrapper import SeleniumWrapper
from utils import save_dict_as_csv

driver = SeleniumWrapper()
driver.setup_driver(headless=False)

JOB_TITLE = "Credit Control"
LOCATION = ""
PAGE_THRESHOLD = "full"
SAVE_FILE_NAME = "result.csv"

filter_dates = [
  "Just posted"
]

results = extract_first_n_page_result(driver, JOB_TITLE, LOCATION, PAGE_THRESHOLD)
filtered_result = filter_result_by_posted_dates(results, filter_dates)

save_dict_as_csv(
  file_name = SAVE_FILE_NAME,
  dictionary = filtered_result
)

