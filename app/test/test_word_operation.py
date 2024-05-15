from time import sleep
from selenium import webdriver

# 获取浏览器驱动，并且打开响应的网址
driver = webdriver.Chrome(executable_path="C:\Program Files (x86)\Google\ChromeDriver\chromedriver.exe")

HOME_PAGE = "http://127.0.0.1:5000/"


def test_word_operation():
    try:
        login()
        unfamiliar()
        familiar()
        delete()
    finally:
        driver.quit()


def login():
    driver.get(HOME_PAGE)

    assert 'English Pal -' in driver.page_source

    # login
    elem = driver.find_element_by_link_text('登录')
    elem.click()
    sleep(2)
    uname = 'peter'
    password = 'peter'

    elem = driver.find_element_by_name('username')
    elem.send_keys(uname)

    elem = driver.find_element_by_name('password')
    elem.send_keys(password)

    # find the login button
    elem = driver.find_element_by_xpath('/html/body/form/p[3]/input')
    elem.click()

    assert 'EnglishPal Study Room for ' + uname in driver.title


def familiar():
    sleep(5)

    elem = driver.find_element_by_xpath('//*[@id="p_0"]/a[3]')

    count = int(elem.find_element_by_xpath('//*[@id="freq_0"]').text)

    loop = 3

    for i in range(loop):
        elem.click()
        sleep(1)

    new_count = int(driver.find_element_by_xpath('//*[@id="freq_0"]').text)

    assert count - loop == new_count


def unfamiliar():
    sleep(5)

    elem = driver.find_element_by_xpath('//*[@id="p_0"]/a[4]')

    count = int(elem.find_element_by_xpath('//*[@id="freq_0"]').text)

    loop = 2

    for i in range(loop):
        elem.click()
        sleep(1)

    new_count = int(driver.find_element_by_xpath('//*[@id="freq_0"]').text)

    assert count + loop == new_count


def delete():
    sleep(3)
    word = driver.find_element_by_xpath('//*[@id="word_0"]').text
    elem = driver.find_element_by_xpath('//*[@id="p_0"]/a[5]')
    elem.click()
    sleep(5)
    driver.refresh()
    driver.refresh()
    driver.refresh()
    find_word = word in driver.page_source
    assert find_word is False
