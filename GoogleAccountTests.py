import time
import unittest
import logging
from logging.handlers import RotatingFileHandler
from pwgen import pwgen

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

import config
import secrets

class AutoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(config.webdriver_binary_path)
        cls.wait = WebDriverWait(cls.driver, 10)
        cls.driver.implicitly_wait(20)
        cls.actions = ActionChains(cls.driver)
        cls.driver.maximize_window()

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()
        cls.driver.quit()

    
class Account(AutoTests):
    @classmethod
    def setUpClass(cls):
        super(Account, cls).setUpClass()

    def setUp(self):
        self.driver.get('https://google.com')

    def click_next(self):
        next_btn = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//span[contains(text(), "Далее")]')
            )
        )
        next_btn.click()

    def test_register(self):
        self.driver.get('https://accounts.google.com')
        username = pwgen(15)
        passwd = pwgen(15)

        create_acc_btn = self.driver.find_element_by_xpath(
            '//span[contains(text(), "Создать аккаунт")]'
        )
        create_acc_btn.click()
        
        firstname_input = self.driver.find_element_by_xpath(
            '//input[@name="firstName"]'
        )
        firstname_input.send_keys('selenium')

        lastname_input = self.driver.find_element_by_xpath(
            '//input[@name="lastName"]'
        )
        lastname_input.send_keys('test')
        
        username_input = self.driver.find_element_by_xpath(
            '//input[@name="Username"]'
        )
        username_input.send_keys(username)

        passwd_input = self.driver.find_element_by_xpath(
            '//input[@name="Passwd"]'
        )
        passwd_input.send_keys(passwd)
        
        confirmpasswd_input = self.driver.find_element_by_xpath(
            '//input[@name="ConfirmPasswd"]'
                            
        )
        confirmpasswd_input.send_keys(passwd)

        next_btn = self.driver.find_element_by_xpath(
            '//span[contains(text(), "Далее")]'
        )
        next_btn.click()

        self.assertTrue(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    '//h1[contains(text(), "Подтвердите номер телефона")]'
                    )
            ),
            msg="переход на страницу с подтвержденеим телефона"
        )

    @unittest.skip('ассертить иконку слишком сложно')
    def test_auth(self):
        self.driver.get('https://google.com')
        username,password = secrets.login_credentials.split(':')
        login_btn = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//a[contains(text(), "Войти")]')
            )
        )
        login_btn.click()
        
        #login_input = self.driver.find_element_by_xpath(
        #    '//a[@name="identifier"]'
        #) по имени почему-то не работает
        login_input = self.wait.until(
            EC.element_to_be_clickable(
                (By.ID, 'identifierId')
            )
        )
        login_input.send_keys(username)
        
        self.click_next()

        passwd_input = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//input[@name="password"]')
            )
        )
        passwd_input.send_keys(password)

        self.click_next()
        user_logo = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//a[@title]')
            )
        )
        time.sleep(5)
        # имеет смысл сравнивать скриншоты
        self.assertRegex(user_logo.get_attribute('title'), username)

