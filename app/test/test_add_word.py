import time
from helper import signup


def test_add_word(URL, driver):
    try:
        username, password = signup(URL, driver) # sign up a new account and automatically log in
        time.sleep(1)

        # enter the word in the text area
        elem = driver.find_element_by_id('selected-words')
        word = 'devour'
        elem.send_keys(word)

        elem = driver.find_element_by_xpath('//form[1]//button[1]') # 找到"把生词加入我的生词库"按钮
        elem.click()

        elem = driver.find_element_by_name('add-btn') # 找到"加入我的生词簿"按钮
        elem.click()

        elems = driver.find_elements_by_xpath("//p[@class='new-word']/a")

        found = 0
        for elem in elems:
            if word in elem.text:
                found = 1
                break

        assert found == 1
    finally:
        driver.quit()
