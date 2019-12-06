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

#select per-turn view
wait_for_ajax(browser)
radioButton = browser.find_element_by_class_name("js-tournament-page-events-select-round")
browser.execute_script("arguments[0].scrollIntoView(true);", radioButton)
radioButton.click()

#select turn 1
wait_for_ajax(browser)
dropdown = browser.find_elements_by_css_selector("div.dropdown.dropdown-select")
dropdown = dropdown[2]
ul = dropdown.find_element_by_tag_name("ul")
li = ul.find_elements_by_tag_name("li")
browser.execute_script("arguments[0].scrollIntoView(true);", dropdown)
browser.find_element_by_class_name("widget-close-button").click()
print("Composed of " + str(len(li)) + " weeks")

#loop through the turns of the season
for j in range(0, len(li)):
    dropdown.click()
    li[j].find_element_by_tag_name("a").click()
    # loop through the matches to scrape data
    wait_for_ajax(browser)
    matches = browser.find_elements_by_class_name("js-event-list-tournament-events")
    for m in matches:
        if (m.is_displayed()):
            matches_click = m
            break
    matches_click = matches_click.find_elements_by_tag_name("a")
    #loop through the matches of that week
    for i in range(0, len(matches_click)):
        matchStatus = str(matches_click[i].find_element_by_css_selector("div.cell__section.status").text).replace("\n", " ")
        #if match is not over (delayed, not yet played and so on)
        if "FIN" not in matchStatus:
            continue

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
        data = {
            "event" : [],
            "eventHome" : [],
            "eventAway" : []
        }
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
        div = browser.find_element_by_class_name("incidents-container")
        events = div.find_elements_by_class_name("cell--incident")
        for i, event in enumerate(events):
            browser.execute_script("arguments[0].scrollIntoView(true);", events[i])
            divClass = event.get_attribute("class")
            txt = str(event.text).replace('\n', ' ').replace(" +", "+")

            if len(txt) == 0:
                pass
            elif "cell--right" in divClass:
                data['eventAway'].append(txt)
            elif "cell--center" in divClass:
                data['event'].append(txt)
            else:
                data['eventHome'].append(txt)
        #get match info like stadium and location
        matchInfo = browser.find_element_by_class_name("js-event-page-info-container")
        browser.execute_script("arguments[0].scrollIntoView(true);", matchInfo)
        matchInfo = matchInfo.find_elements_by_tag_name("tr")
        for m in matchInfo:
            td = m.find_elements_by_tag_name("td")
            td[0] = str(td[0].text).replace("\n", " ").title().replace(' ', '').replace("'", "")
            td[1] = str(td[1].text).replace("\n", " ")
            if "DataDiInizio" != td[0] and "CartelliniPerPartita" != td[0]:
                data['info' + td[0]] = td[1]


        #scroll back to top of window
        browser.execute_script("arguments[0].scrollIntoView(true);", browser.find_element_by_css_selector("a.h-interactive.js-event-link"))
        # click statistics tab
        browser.find_element_by_xpath("//*[@id='pjax-container-main']/div/div[2]/div/div/div/div[1]/div[3]/div[3]/div/div[2]/div/div/div[1]/div[3]/ul/li[2]").click()
        wait_for_ajax(browser)
        # get statistics
        stats = browser.find_element_by_id("statistics-period-ALL").find_elements_by_class_name("stat-group-event")
        for s in stats:
            browser.execute_script("arguments[0].scrollIntoView(true);", s)
            for i, e in enumerate(str(s.text).split('\n')):
                if i % 3 == 0:
                    tmp = e
                elif i % 3 == 1:
                    statName = e.title().replace(' ', '').replace("'", "")  # CamelCase it
                    data['home' + statName] = tmp
                else:
                    data['away' + statName] = e

        #scroll back to top of window
        browser.execute_script("arguments[0].scrollIntoView(true);", browser.find_element_by_css_selector("a.h-interactive.js-event-link"))
        json_data = json.dumps(data)
        print(json_data)
        f.write(json_data + '\n')
        #click X and close stats panel
        browser.find_element_by_class_name("widget-close-button").click()


f.close()
print("------ %s seconds ------" % (time.time() - start_time))
# browser.close()




exit(0)
