from wrappers.selenium_wrapper import SeleniumWrapper
from bs4 import BeautifulSoup
from pprint import pprint

BASE_URL = "https://uk.indeed.com"

def get_result_code(driver):
  JOB_RESULTS_XPATH = "/html/body/main/div/div[1]/div/div/div[5]/div[1]/div[5]/div/ul"
  driver.load_wait(JOB_RESULTS_XPATH)
  result_elem = driver.load_element(JOB_RESULTS_XPATH)
  result_html_code = result_elem.get_attribute("innerHTML")
  print(result_html_code)
  return result_html_code

def extract_result(result_code):
  soup = BeautifulSoup(result_code, "html.parser")
  results = soup.find_all("li")
  filtered_results = []
  for result in results:
    num_escapes = len(result.get_text().split("\n"))
    if num_escapes > 2:
      filtered_results.append(result)

  jobs = []
  for result in filtered_results:
    job_title = result.find("span").get_text() if result.find("span") != None else None
    rating = result.find("span", {"class": "ratingNumber"}).find("span").get_text() if result.find("span", {"class": "ratingNumber"}) != None else None
    company_name = result.find("span", {"class": "companyName"}).get_text() if result.find("span", {"class": "companyName"}) != None else None
    day_posted = result.find("span", {"class": "date"}).get_text().replace("PostedPosted ", "", 1) if result.find("span", {"class": "date"}) != None else None
    salary = result.find("div", {"class": "attribute_snippet"}).get_text().replace(" a year", "") if result.find("div", {"class": "attribute_snippet"}) != None else None
    job_link = BASE_URL + filtered_results[0].find("a", {"class": "jcs-JobTitle"}, href=True)["href"]

    job_info = {
      "job_title": job_title,
      "rating": rating,
      "company_name": company_name,
      "day_posted": day_posted,
      "salary": salary,
      "job_link": job_link
    }

    jobs.append(job_info)
  
  return jobs

def get_nth_result_page_code(driver, job_title, location, page_no):
  driver.get(BASE_URL + "/jobs?q=" + job_title + "&l=" + location + "&start=" + str(page_no * 10))
  result_code = get_result_code(driver)
  result = extract_result(result_code)
  return result


driver = SeleniumWrapper()
driver.setup_driver(headless=False)
result_code = get_nth_result_page_code(driver, "apprenticeship", "London, Greater London", 2)
result = extract_result(result_code)


pprint(result)

while True:
  pass