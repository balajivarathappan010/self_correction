from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def PlayingIPL():
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service)

    driver.get("https://google.com")

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME,"gLFyf"))
    )

    input_element = driver.find_element(By.CLASS_NAME,"gLFyf")
    input_element.click()
    input_element.send_keys("jiocinema", Keys.ENTER)

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME,"yuRUbf"))
    )

    link = driver.find_element(By.CLASS_NAME, "yuRUbf")
    anchor_tag = link.find_element(By.TAG_NAME,"a")

    anchor_tag.click()

    clickable = driver.find_element(By.ID, "rail_jio_voot-common_my-voot_0_editorial_1656321054")
    clickable.click()
    while True:
        if driver.window_handles:
            time.sleep(1)
        else:
            break

    driver.quit()
