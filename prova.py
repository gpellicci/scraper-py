


import json
import os
import time
import unicodedata
import numpy

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def wait_for_ajax(driver):
    wait = WebDriverWait(driver, 15)
    try:
        wait.until(lambda driver: driver.execute_script('return jQuery.active') == 0)
        wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    except Exception as e:
        pass


months = ["Gen", "Feb", "Mar", "Apr", "Mag", "Giu", "Lug", "Ago", "Set", "Ott", "Nov", "Dic"]
months_num = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]

f = open("16-17.txt", "w+")
webdriverPath = "./chromedriver"
if os.name == 'nt':
    webdriverPath += ".exe"
browser = webdriver.Chrome(webdriverPath)
browser.maximize_window()

url = "http://www.calcio.com/cronaca_partita/serie-a-2016-2017-as-roma-udinese-calcio/"
start_time = time.time()

#connect to serie-a archive
browser.get(url)
wait_for_ajax(browser)

bb = browser.find_elements_by_css_selector("td")
for i in range(0, 30):
    bb.pop(0)
for b in bb:
    t = str(b.text)
    print(b.text)
    f.write(t)
