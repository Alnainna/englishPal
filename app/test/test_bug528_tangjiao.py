import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


# 测试登录页面输入密码包含空格的情况
def test_login_password_with_space(driver, URL):
    try:
        driver.get(URL+"/login")

        # 输入用户名
        username_elem = driver.find_element_by_id('username')
        username_elem.send_keys("test_user")

        # 输入包含空格的密码
        password_elem = driver.find_element_by_id('password')
        password_elem.send_keys("password with space")

        # 提交登录表单
        elem = driver.find_element_by_class_name('btn')  # 找到提交按钮
        elem.click()

        # 显式等待直到警告框出现
        WebDriverWait(driver, 10).until(EC.alert_is_present())

        # 检查是否弹出警告框
        alert = driver.switch_to.alert
        assert "输入不能包含空格!" in alert.text
    except (NoSuchElementException, TimeoutException) as e:
        pytest.fail("页面元素未找到或超时: {}".format(e))


# 测试注册页面输入密码包含空格的情况

def test_signup_password_with_space(driver, URL):
    try:
        driver.get(URL+"/signup")

        # 输入用户名
        username_elem = driver.find_element_by_id('username')
        username_elem.send_keys("new_user")

        # 输入包含空格的密码
        password_elem = driver.find_element_by_id('password')
        password_elem.send_keys("password with space")

        # 再次输入密码
        password2_elem = driver.find_element_by_id('password2')
        password2_elem.send_keys("password with space")

        # 提交注册表单
        elem = driver.find_element_by_class_name('btn')  # 找到提交按钮
        elem.click()

        # 显式等待直到警告框出现
        WebDriverWait(driver, 10).until(EC.alert_is_present())

        # 检查是否弹出警告框
        alert = driver.switch_to.alert
        assert "输入不能包含空格!" in alert.text
    except (NoSuchElementException, TimeoutException) as e:
        pytest.fail("页面元素未找到或超时: {}".format(e))



# 测试重设密码页面输入新密码包含空格的情况

def test_reset_password_with_space(driver, URL):
    try:
        driver.get(URL+"/reset")

        # 输入用户名
        username_elem = driver.find_element_by_id('username')
        username_elem.send_keys("test_user")

        # 输入包含空格的密码
        password_elem = driver.find_element_by_id('password')
        password_elem.send_keys("password with space")

        # 提交重设密码表单
        elem = driver.find_element_by_class_name('btn')  # 找到提交按钮
        elem.click()

        # 显式等待直到警告框出现
        WebDriverWait(driver, 10).until(EC.alert_is_present())

        # 检查是否弹出警告框
        alert = driver.switch_to.alert
        assert "输入不能包含空格!" in alert.text
    except (NoSuchElementException, TimeoutException) as e:
        pytest.fail("页面元素未找到或超时: {}".format(e))
