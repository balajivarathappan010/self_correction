from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def API_Searching():
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service)

    driver.get("https://google.com")

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME,"gLFyf"))
    )

    input_element = driver.find_element(By.CLASS_NAME,"gLFyf")
    input_element.click()
    
    input_element.send_keys("weather api", Keys.ENTER)

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME,"yuRUbf"))
    )

    link = driver.find_element(By.CLASS_NAME, "yuRUbf")
    anchor_tag = link.find_element(By.TAG_NAME,"a")

    anchor_tag.click()

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME,"col-sm-4"))
    )
    api = driver.find_element(By.CLASS_NAME,"col-sm-4")
    anchor = api.find_elements(By.TAG_NAME,"a")

    driver.execute_script("arguments[0].click();", anchor[0])

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME,"api"))
    )

    source = driver.find_elements(By.CLASS_NAME, "api")
    tag = source[1].find_element(By.TAG_NAME, "code")
    text = tag.text
    print(text)

    key = tag.find_element(By.TAG_NAME, "a")
    driver.execute_script("arguments[0].click();", key)
    new_window = driver.window_handles[-1]
    driver.switch_to.window(new_window)
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME,"input-group"))
    )


    get_input = driver.find_elements(By.CLASS_NAME, "input-group")
    print(len(get_input))
    mail = get_input[0].find_element(By.ID,"user_email")
    password = get_input[1].find_element(By.ID, "user_password")
    mail.send_keys("balajivarathappan@gmail.com")
    password.send_keys("Balaji@010")
    btn = driver.find_element(By.NAME, "commit")
    btn.click()

    pr = driver.find_element(By.TAG_NAME, "pre")
    # while True:
    #     if driver.window_handles:
    #         time.sleep(1)
    #     else:
    #         break
    # driver.quit()
    return pr.text
