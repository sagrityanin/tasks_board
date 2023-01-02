from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import os
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from dotenv import load_dotenv

count = 100
url = "https://task.info66.ru:4443"
url_login = "https://task.info66.ru:4443/login/"

load_dotenv()


def make_task(browser, i: int) -> None:
    browser.find_element(By.ID, "id_title").send_keys(f"Тестовая задача {i}")
    browser.find_element(By.ID, "id_executor").find_elements(By.TAG_NAME, "option")[1].click()
    sleep(1)
    browser.find_element(By.XPATH, '//button[@type="submit"]').click()
    sleep(1)


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
        for i in range(count):
            browser.find_element(By.XPATH, "//*[contains(text(), 'Добавить задачу')]").click()
            print(f"Создание задачи {i}")
            sleep(1)
            make_task(browser, i)


if __name__ == "__main__":
    main(int(os.getenv("COUNT")))
