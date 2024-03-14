from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import os
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from dotenv import load_dotenv

url_login = "https://task.info66.ru:4443/login/"

load_dotenv()


def change_status(browser) -> None:
    browser.find_element(By.ID, "id_status").find_elements(By.TAG_NAME, "option")[1].click()
    sleep(1)
    browser.find_element(By.XPATH, "//*[contains(text(), 'Сохранить')]").click()


def login(browser):
    browser.get(url_login)
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable(
        (By.ID, "id_username"))).send_keys(os.getenv("TASK_USER"))
    browser.find_element(By.ID, "id_password").send_keys(os.getenv("TASK_PASSWORD"))
    browser.find_element(By.TAG_NAME, "button").click()
    sleep(2)


def main(count: int) -> None:
    with webdriver.Chrome() as browser:
        login(browser)
        for i in range(count):
            browser.get("https://task.info66.ru:4443/task-list")
            sleep(1)
            browser.find_element(By.ID, "id_executor").find_element(By.XPATH, "//*[contains(text(), 'andrey')]").click()

            sleep(3)
            list_tasks = browser.find_elements(By.XPATH, "//*[contains(text(), 'Детали задачи')]")
            if len(list_tasks) > 0:
                list_tasks[0].click()
                print(f"Меняем статус задачи {i}")
                change_status(browser)
            else:
                print("Все задачи обработаны")
                break


if __name__ == "__main__":
    main(int(os.getenv("COUNT")))
