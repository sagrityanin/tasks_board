from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import os
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from dotenv import load_dotenv

urls = ["https://task.info66.ru:4443/tasks/all/",
        "https://task.info66.ru:4443/usertasks/"]
url_login = "https://task.info66.ru:4443/login/"

load_dotenv()




def login(browser) -> None:
    browser.get(url_login)
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable(
        (By.ID, "id_username"))).send_keys(os.getenv("TASK_USER"))
    browser.find_element(By.ID, "id_password").send_keys(os.getenv("TASK_PASSWORD"))
    browser.find_element(By.TAG_NAME, "button").click()
    sleep(1)


def main(count: int) -> None:
    with webdriver.Chrome() as browser:
        login(browser)
        for url in urls:
            browser.get(url)
            for i in range(count):
                browser.find_element(By.XPATH, "//*[contains(text(), 'next')]").click()
                sleep(2)
            for i in range(count):
                browser.find_element(By.XPATH, "//*[contains(text(), 'previous')]").click()
                sleep(2)


if __name__ == "__main__":
    main(2)
    print("Pagination correct")
