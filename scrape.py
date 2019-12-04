import json
import os
import time
import datetime

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

f = open("test.txt", "w+")
webdriverPath = "./chromedriver"
if os.name == 'nt':
    webdriverPath += ".exe"
browser = webdriver.Chrome(webdriverPath)
browser.maximize_window()
url = "https://www.sofascore.com/it/torneo/calcio/italy/serie-a/23"
start_time = time.time()
browser.get(url)

# get on the desired season
wait_for_ajax(browser)
dropdown = browser.find_elements_by_css_selector("div.dropdown.dropdown-select")
dropdown = dropdown[0]
ul = browser.find_element_by_xpath(
    "//*[@id='pjax-container-main']/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[3]/div/div/ul")
li = ul.find_elements_by_tag_name("li")
dropdown.click()
li[3].find_element_by_tag_name("a").click()
print("Clicked on season " + dropdown.text)

# set week 1
wait_for_ajax(browser)
dropdown = browser.find_elements_by_css_selector("div.dropdown.dropdown-select")
dropdown = dropdown[1]
ul = dropdown.find_element_by_tag_name("ul")
li = ul.find_elements_by_tag_name("li")
browser.execute_script("arguments[0].scrollIntoView(true);", dropdown)
dropdown.click()
li[0].find_element_by_tag_name("a").click()

# loop through the matches to scrape data
wait_for_ajax(browser)
matches = browser.find_elements_by_class_name("js-event-list-tournament-events")[1].find_elements_by_tag_name("a")
print(len(matches))
browser.find_element_by_xpath(
    "//*[@id='pjax-container-main']/div/div[2]/div/div/div/div[1]/div[3]/div[3]/div/div[2]/div/div/button").click()
for i in range(0, len(matches)):
    matches_click = browser.find_elements_by_class_name("js-event-list-tournament-events")[1].find_elements_by_tag_name(
        "a")
    matches_click[i].click()
    try:
        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "js-details-widget-container"))
        )
    except:
        pass
    wait_for_ajax(browser)
    # get team names
    teams = str(browser.find_element_by_css_selector("a.h-interactive.js-event-link").text).split(" - ")
    data = {}
    data['homeTeam'] = teams[0]
    data['awayTeam'] = teams[1]
    # get match date
    date = browser.find_element_by_class_name("js-details-component-startTime-container").find_elements_by_class_name(
        "cell__content")[0]
    d = str(date.text).replace(".", "").replace(",", "")
    d = d.split()
    isodate = d[2] + "-" + months_num[months.index(d[1])] + "-" + d[0] + "T" + d[3] + ":00:000+01:00"
    data['date'] = isodate
    #get match events (tabellino)
    #div = browser.find_element_by_class_name("incidents-container")
    ##############
    #events = div.find_elements_by_class_name("cell")
    #print("Events#"+len(events))
    ############### prendere cell (center, right, left) e scriverci away o home
    # click statistics
    browser.find_element_by_xpath("//*[@id='pjax-container-main']/div/div[2]/div/div/div/div[1]/div[3]/div[3]/div/div[2]/div/div/div[1]/div[3]/ul/li[2]").click()
    wait_for_ajax(browser)
    # get stats
    stats = browser.find_element_by_id("statistics-period-ALL").find_elements_by_class_name("stat-group-event")
    for s in stats:
        for i, e in enumerate(str(s.text).split('\n')):
            if i % 3 == 0:
                tmp = e
            elif i % 3 == 1:
                statName = e.title().replace(' ', '').replace("'", "")  # CamelCase it
                data['home' + statName] = tmp
            else:
                data['away' + statName] = e

    json_data = json.dumps(data)
    print(json_data)
    #click X and close stats panel
    browser.find_element_by_xpath(
        "//*[@id='pjax-container-main']/div/div[2]/div/div/div/div[1]/div[3]/div[3]/div/div[2]/div/div/button").click()

f.close()
print("------ %s seconds ------" % (time.time() - start_time))
# browser.close()
