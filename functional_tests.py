#coding=utf-8
from selenium import webdriver
import unittest
import os

chrome_driver_path = r"C:\Users\stone\Desktop\chromedriver.exe"

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        chrome_driver = os.path.abspath(chrome_driver_path)
        os.environ["webdriver.chrome.driver"] = chrome_driver
        self.driver = webdriver.Chrome(chrome_driver)
        self.driver.implicitly_wait(3) #3秒等待
    def tearDown(self):
        self.driver.quit()

    def test_process(self):
        #用户打开在线待办事务应用首页
        self.driver.get("http://localhost:8000")
        #以确定打开首页，其标题包含‘To-Do’
        self.assertIn('To-Do' , self.driver.title)
        self.fail('Finish the test.')

        #用户的其他操作...

if __name__ == '__main__':
    unittest.main()