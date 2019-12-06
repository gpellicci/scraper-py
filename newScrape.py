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


# url = "https://www.diretta.it/serie-a/archivio/"
# start_time = time.time()
#
# #connect to serie-a archive
# browser.get(url)
# wait_for_ajax(browser)
#
# #find list of seasons
# seasons = browser.find_element_by_id("tournament-page-archiv").find_elements_by_class_name("leagueTable__season")
# seasons.pop(0)
# seasons.pop(0)
# leagueName = browser.find_element_by_class_name("teamHeader__name").text
# # leagueYear = browser.find_element_by_class_name("teamHeader__text").text
# print(leagueName + " has " + str(len(seasons)) + " seasons available")
# for s in seasons:
#     print(s.find_element_by_tag_name('a').text)
#
# #for each season (from past year to the first recorded)
# for i in range(0, len(seasons)):
#     #open the season panel
#     seasons.pop(0).find_element_by_tag_name('a').click()
#
# exit(0)



url = "https://www.diretta.it/serie-a-2018-2019/risultati/"
start_time = time.time()

#connect to serie-a archive
browser.get(url)
wait_for_ajax(browser)

#
browser.find_element_by_class_name("event__more event__more--static")


#find list of seasons
seasons = browser.find_element_by_id("tournament-page-archiv").find_elements_by_class_name("leagueTable__season")
seasons.pop(0)
seasons.pop(0)
leagueName = browser.find_element_by_class_name("teamHeader__name").text
# leagueYear = browser.find_element_by_class_name("teamHeader__text").text
print(leagueName + " has " + str(len(seasons)) + " seasons available")
for s in seasons:
    print(s.find_element_by_tag_name('a').text)

#for each season (from past year to the first recorded)
for i in range(0, len(seasons)):
    #open the season panel
    seasons.pop(0).find_element_by_tag_name('a').click()
