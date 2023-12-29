
import traceback
from selenium import webdriver
import sys

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# To test the score service of a web application.
def test_scores_service(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    # Initialize a Chrome Web Driver
    driver = webdriver.Chrome()
    try:
        driver.get(url)
        # Wait until the score element is present in the DOM
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "score"))
        )
        score_html_element = driver.find_element(By.ID, "score")
        score = int(score_html_element.text)
        return 1 <= score <= 1000
    except Exception as e:
        print(f"Error produced during test execution: {e}")
        traceback.print_exc()
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
