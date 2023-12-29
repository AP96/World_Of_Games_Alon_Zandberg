import requests
from selenium import webdriver
import sys

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


# To test the score service of a web application.
def test_scores_service(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    # Initialize a Chrome Web Driver
    driver = webdriver.Chrome()
    try:
        driver.get(url)
        score_html_element = driver.find_element(By.ID, "score")
        score = int(score_html_element.text)
        return 1 <= score <= 1000
    except Exception as e:
        print(f"Error produced during test execution: {e}")
        return False
    finally:
        driver.quit()


def main_function():
    application_url = "http://localhost:5000/score"
    if test_scores_service(application_url):
        print("Test Passed Succesfully !")
        sys.exit(0)
    else:
        print("Test Failed !")
        sys.exit(-1)


if __name__ == "__main__":
    main_function()
