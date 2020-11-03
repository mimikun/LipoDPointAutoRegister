# type: ignore
import argparse
import configparser
import os
import time
from datetime import datetime
import urllib3
from selenium.webdriver import Chrome, ChromeOptions
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

CONFIG_FILE = "./config.ini"

parser = argparse.ArgumentParser(description="Awesome lipobitan D point Auto Registration Tool")

group = parser.add_mutually_exclusive_group()
group.add_argument("--version", action="store_true",
                   help="Show version")

args = parser.parse_args()

if os.path.exists(CONFIG_FILE):
    # Read Conf from config.ini
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE, encoding="utf-8")

    login_email = config["LOGIN"]["Email"]
    login_password = config["LOGIN"]["Password"]
else:
    # Read conf from .env.production
    login_email = os.environ["LOGIN_EMAIL"]
    login_password = os.environ["LOGIN_PASSWORD"]

NOW_DT = datetime.now()

try:
    # ChromeDriver Setting(Docker)
    driver = webdriver.Remote(
        "http://selenium-chrome:4444/wd/hub", DesiredCapabilities.CHROME)
    print("Running in Docker...")
except urllib3.exceptions.HTTPError:
    options = ChromeOptions()
    options.add_argument("--headless")
    driver = Chrome(options=options)
    print("Running in Local...")

driver.get("https://m.taisho.co.jp/login/")

assert "リポビタンポイントチャージステーション｜大正製薬" in driver.title

# ログイン情報を挿入
print("Insert login ID and Password...")
email = driver.find_element_by_css_selector(
    "#form1 > div:nth-child(2) > input")
password = driver.find_element_by_css_selector(
    "#form1 > div:nth-child(4) > input")
email.send_keys(login_email)
password.send_keys(login_password)

# ログインボタンを押下
driver.find_element_by_css_selector("#form1 > div.loginModal__btn > input").click()
print("Click Login Button...")

WebDriverWait(driver, 30).until(EC.title_is("リポビタンポイントチャージステーション｜大正製薬"))


driver.get('https://lipovitan-point.com/serial_regist.php')
print('Open Point Registration Page...')


width = driver.execute_script("return document.body.scrollWidth;")
height = driver.execute_script("return document.body.scrollHeight;")
driver.set_window_size(width, height)
driver.save_screenshot("./result.png")

driver.quit()
print("Point Registration done!!!")
