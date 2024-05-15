import random
import string
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from helper import signup


def has_punctuation(s):
    return any(c in string.punctuation for c in s)


def login(driver, home, uname, password):
    driver.get(home)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, '登录'))).click()
    driver.find_element(By.ID, 'username').send_keys(uname)
    driver.find_element(By.ID, 'password').send_keys(password)
    driver.find_element(By.XPATH, '//button[text()="登录"]').click()
    WebDriverWait(driver, 10).until(EC.title_is(f"EnglishPal Study Room for {uname}"))


def select_valid_word(driver):
    elem = driver.find_element(By.ID, 'text-content')
    essay_content = elem.text
    valid_word = random.choice([word for word in essay_content.split() if len(word) >= 6 and not has_punctuation(
        word) and 'font>' not in word and 'br>' not in word and 'p>' not in word])
    driver.find_element(By.ID, 'selected-words').send_keys(valid_word)
    return valid_word


def test_save_selected_word(driver, URL):
    try:
        username, password = signup(URL, driver)
        word = select_valid_word(driver)
        stored_words = driver.execute_script('return localStorage.getItem("selectedWords");')
        assert word == stored_words, "Selected word not saved to localStorage correctly"
        # 退出并重新登录以检查存储的单词
        driver.find_element(By.LINK_TEXT, '退出').click()
        driver.execute_script("window.open('');window.close();")

        # 等待一会儿，让浏览器有足够的时间关闭标签页
        WebDriverWait(driver, 2)

        # 重新打开一个新的标签页
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])  # 切换到新打开的标签页

        login(driver, URL, username, password)
        textarea_content = driver.find_element(By.ID, 'selected-words').get_attribute('value')
        assert word == textarea_content, "Selected word not preserved after re-login"
    finally:
        driver.quit()
