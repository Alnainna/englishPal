import uuid
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException, NoAlertPresentException

def signup(URL, driver):
    username = 'TestUser' + str(uuid.uuid1()).split('-')[0].title()
    password = '[Abc+123]'

    driver.get(URL)
        
    elem = driver.find_element_by_link_text('注册')
    elem.click()
    
    elem = driver.find_element_by_id('username')
    elem.send_keys(username)
    
    elem = driver.find_element_by_id('password')
    elem.send_keys(password)

    elem = driver.find_element_by_id('password2')
    elem.send_keys(password)    
    
    elem = driver.find_element_by_class_name('btn') # 找到"注册"按钮
    elem.click()

    try:
        WebDriverWait(driver, 1).until(EC.alert_is_present())
        driver.switch_to.alert.accept()
    except (UnexpectedAlertPresentException, NoAlertPresentException):
        pass
    
    return username, password
