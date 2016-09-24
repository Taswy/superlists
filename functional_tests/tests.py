#coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
import unittest
import os

chrome_driver_path = r"C:\Users\stone\Desktop\chromedriver.exe"

class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        chrome_driver = os.path.abspath(chrome_driver_path)
        os.environ["webdriver.chrome.driver"] = chrome_driver
        self.driver = webdriver.Chrome(chrome_driver)
        self.driver.implicitly_wait(3) #3秒等待
    def tearDown(self):
        self.driver.quit()

    def check_for_row_in_list_table(self,row_text):
        table =self.driver.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text,[row.text for row in  rows])

    def test_process(self):
        #用户打开在线待办事务应用首页
        self.driver.get(self.live_server_url)
        #以确定打开首页，其标题和头部包含‘To-Do’
        self.assertIn('To-Do' , self.driver.title)
        header_text = self.driver.find_element_by_tag_name('h1').text
        self.assertIn('To-Do',header_text)
        #应用邀请他输入一个待办事项
        inputbox = self.driver.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')
        #他在文本框中输入离“Buy peacock feather”
        inputbox.send_keys('Buy peacock feather')

        #他按回车键后，页面更新
        inputbox.send_keys(Keys.ENTER)
        self.check_for_row_in_list_table('1: Buy peacock feather')

        #页面更新，显示一条代办事务“Buy peacock feather”

        #页面又显示一个文本框，可以输入其他的待办事项]
        #他有输入“Use peacock feathers to make a fly ”
        inputbox = self.driver.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        #页面再次更新 显示两条
        table =self.driver.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.check_for_row_in_list_table('1: Buy peacock feather')
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')
        self.fail('Finish the test.')
        #用户的其他操作...

if __name__ == '__main__':
    unittest.main()