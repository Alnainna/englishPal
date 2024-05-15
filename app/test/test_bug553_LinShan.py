from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import logging
import time
import pytest

@pytest.mark.parametrize("test_input,expected",
                         [("‘test1’", "test1"),
                          ("'test2'", "test2"),
                          ("“test3”", "test3"),
                          ("it's", "it's"),
                          ("hello,I'm linshan", ["hello","i'm","linshan"]),
                          ("Happy New Year！？", ["happy","new","year"]),
                          ("My favorite book is 《Harry Potter》。", ["potter","harry","my","favorite","book","is"])])
def test_bug553_LinShan(test_input,expected, driver, URL):
    try:
        # 打开对应地址的网页
        driver.get(URL)

        # 浏览器最大窗口化
        driver.maximize_window()

        # 判断网页源代码中是否有English Pal -文字
        assert 'English Pal -' in driver.page_source

        # 将测试的数据输入到主页的textarea里
        driver.find_element_by_xpath("//textarea[@name='content']").send_keys(Keys.CONTROL, "a")
        driver.find_element_by_xpath("//textarea[@name='content']").send_keys(test_input)
        time.sleep(1)

        # 点击按钮获取单词
        driver.find_element_by_xpath("//input[@value='get文章中的词频']").click()
        time.sleep(1)

        # 获取筛选后的单词
        words = driver.find_elements_by_xpath("//p/a")

        # 遍历获取到的单词，并判断单词与预期的相同
        for word in words:
            # 判断单词是否在预期结果中
            assert word.text in expected
            
        # 返回上一页网页
        driver.find_element_by_xpath("//input[@value='确定并返回']").click()
        time.sleep(0.1)

    except Exception as e:
        # 输出异常信息
        logging.error(e)
        # 关闭浏览器
        driver.quit()
    finally:
        driver.quit()
