from bs4 import BeautifulSoup
from tqdm import tqdm

BASE_URL = "https://uk.indeed.com"

def get_result_code(driver):
  JOB_RESULTS_XPATH = "/html/body/main/div/div[1]/div/div/div[5]/div[1]/div[5]/div/ul"
  driver.load_wait(JOB_RESULTS_XPATH)
  result_elem = driver.load_element(JOB_RESULTS_XPATH)
  result_html_code = result_elem.get_attribute("innerHTML")
  
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
      "Job Ttile": job_title,
      "Rating": rating,
      "Company Name": company_name,
      "Day Posted": day_posted,
      "Salary": salary,
      "Job Link": job_link
    }

    jobs.append(job_info)
  
  return jobs

def get_nth_result_page_code(driver, job_title, location, page_no):
  driver.get(BASE_URL + "/jobs?q=" + job_title + "&l=" + location + "&start=" + str(page_no * 10))
  result_code = get_result_code(driver)
  return result_code

def get_nth_page_result(driver, job_title, location, page_no):
  result_page_code = get_nth_result_page_code(driver, job_title, location, page_no)
  extracted_result = extract_result(result_page_code)
  return extracted_result

def extract_first_n_page_result(driver, job_title, location, n_pages):
  print(f"[*] Extracting {n_pages} results ...")
  final_result = []
  for page in tqdm(range(n_pages)):
    result = get_nth_page_result(driver, job_title, location, page)
    final_result = final_result + result
  return final_result


def filter_result_by_posted_dates(results, filter_dates):
  filtered_result = []
  for result in results: 
    if result["Day Posted"] in filter_dates:
      filtered_result.append(result)
  return filtered_result

# def extract_page_result_until_day_posted(driver, job_title, location, day_posted):
#   final_result = []

#   is_day_posted_found = False
#   page = 0
#   while True:
#     results = get_nth_page_result(driver, job_title, location, page)

    # if not is_day_posted_found and (results[-1]["day_posted"] == day_posted):
    #   is_day_posted_found = True

    # if is_day_posted_found and (results[-1]["day_posted"] != day_posted):
    #   is_day_posted_local_found = False
    #   for result in results:
    #     final_result = final_result + result
    #     if not is_day_posted_local_found and (result["day_posted"] == day_posted):
    #       is_day_posted_local_found = True
    #     if is_day_posted_local_found and (result["day_posted"] != day_posted):
    #       break
    #   break

    # final_result = final_result + results
    # page += 1