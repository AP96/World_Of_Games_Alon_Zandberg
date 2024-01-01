import traceback
import sys
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_scores_service(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Remote(
        command_executor='http://selenium-standalone-chrome:4444/wd/hub',
        options=chrome_options
    )

    try:
        driver.get(url)
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
    application_url = "http://wog_web_app:5000/score"
    if test_scores_service(application_url):
        print("Test Passed Successfully!")
        sys.exit(0)
    else:
        print("Test Failed!")
        sys.exit(-1)


if __name__ == "__main__":
    main_function()
