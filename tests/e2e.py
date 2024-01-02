import traceback
import sys
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_scores_service(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Remote(
        command_executor='http://localhost:4444/wd/hub',
        options=chrome_options
    )

    try:
        logging.info(f"Opening URL: {url}")
        driver.get(url)
        logging.info("Waiting for the score element to be present on the page.")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "score"))
        )
        score_html_element = driver.find_element(By.ID, "score")
        score = int(score_html_element.text)
        logging.info(f"Score found: {score}")
        return 1 <= score <= 1000
    except Exception as e:
        logging.error("Error produced during test execution", exc_info=True)
        return False
    finally:
        logging.info("Quitting the driver.")
        driver.quit()


def main_function():
    application_url = "http://localhost:5001/score"
    logging.info("Starting the test.")
    if test_scores_service(application_url):
        logging.info("Test Passed Successfully!")
        sys.exit(0)
    else:
        logging.error("Test Failed!")
        sys.exit(-1)


if __name__ == "__main__":
    main_function()
