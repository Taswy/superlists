#coding=utf-8

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
import unittest
import os

chrome_driver_path = r"/local/chromedriver"

class NewVisitorTest(LiveServerTestCase):
    def start_a_chrome(self):
        chrome_driver = os.path.abspath(chrome_driver_path)
        os.environ["webdriver.chrome.driver"] = chrome_driver
        return webdriver.Chrome(chrome_driver)
    def setUp(self):
        self.driver = self.start_a_chrome()
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

        #他按回车键后，被带到一个新的URL
        inputbox.send_keys(Keys.ENTER)
        #这个页面显示一条代办事务“Buy peacock feather”
        edith_list_url = self.driver.current_url
        self.assertRegexpMatches(edith_list_url, '/lists/.+')
        print edith_list_url
        self.check_for_row_in_list_table('1: Buy peacock feather')
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
        #用户的其他操作...

        #另外一个用户2（新用户）访问了网站
        ##使用一个新的浏览器会话
        ## 确保用户1的信息不会从cookie中泄露出来
        self.driver.quit()
        self.driver = self.start_a_chrome()

        # 用户2访问首页
        # 页面中看不到用户1的清单
        self.driver.get(self.live_server_url)
        page_text = self.driver.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feather', page_text)
        self.assertNotIn('Use peacock feathers to make a fly', page_text)

        #用户2输入一个新的待办事务，新建一个清单
        # 他不像用户1的风格
        inputbox = self.driver.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        # 用户1获得了它的唯一url
        francis_list_url = self.driver.current_url
        self.assertRegexpMatches(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        #刷新之后的页面还是没有edith的清单
        page_text = self.driver.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feather', page_text)
        self.assertIn('Buy milk', page_text)

        #两个人很满意，都去睡觉了

        self.fail('Finish the test.')

if __name__ == '__main__':
    unittest.main()