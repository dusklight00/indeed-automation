from wrappers.indeed_wrapper import extract_first_n_page_result, filter_result_by_posted_dates
from wrappers.selenium_wrapper import SeleniumWrapper
from pprint import pprint

driver = SeleniumWrapper()
driver.setup_driver(headless=False)

JOB_TITLE = "apprenticeship"
LOCATION = "London, Greater London"
PAGE_THRESHOLD = 2

filter_dates = [
  "1 day ago",
  "2 days ago",
  "3 days ago",
  "4 days ago"
]

results = extract_first_n_page_result(driver, JOB_TITLE, LOCATION, PAGE_THRESHOLD)
filtered_result = filter_result_by_posted_dates(results, filter_dates)

pprint(filtered_result)