import requests
import json
import os
import time
import unicodedata
import numpy

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def openInNewTab(link):
    link = str(link)
    browser.execute_script("window.open(arguments[0]);", link)
def camelCaseIt(text):
    return str(text).title().replace(' ', '').replace("'", "")
def scrollTo(element):
    browser.execute_script("arguments[0].scrollIntoView(true);", element)

def wait_for_ajax(driver):
    wait = WebDriverWait(driver, 15)
    try:
        wait.until(lambda driver: driver.execute_script('return jQuery.active') == 0)
        wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    except Exception as e:
        pass



months = ["Gen", "Feb", "Mar", "Apr", "Mag", "Giu", "Lug", "Ago", "Set", "Ott", "Nov", "Dic"]
months_num = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]

webdriverPath = "./chromedriver"
adBlockPath = "./chromeAdBlock/3.7_0"
if os.name == 'nt':
    webdriverPath += ".exe"

# chrome_options = Options()
# chrome_options.add_argument('load-extension=' + adBlockPath)
# browser = webdriver.Chrome(webdriverPath, chrome_options=chrome_options)
# browser.create_options()
browser = webdriver.Chrome(webdriverPath)
browser.maximize_window()

url = "http://www.calcio.com/storia/ita-serie-a/"
start_time = time.time()


#connect to serie-a archive
browser.get(url)
browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')
wait_for_ajax(browser)



#get list of seasons
seasons = browser.find_elements_by_class_name("data")[1].find_elements_by_tag_name('tr')
# loop through the seasons #2fixed - #nseasons+2    -> range(2, 7) -> 7-2 = 5 seasons
for i in range(2, 3):#len(seasons)
    wait_for_ajax(browser)
    season = {
        "team": []
    }
    seasons = browser.find_elements_by_class_name("data")[1].find_elements_by_tag_name('tr')
    e = seasons[i]
    line = e.find_elements_by_tag_name('td')
    season['winner'] = line[5].text
    season['year'] = line[0].text
    #click on "squadre"
    line[3].find_element_by_tag_name('a').click()
    wait_for_ajax(browser)

    #get list of teams of the season
    teams = browser.find_elements_by_class_name("data")[2].find_elements_by_tag_name('tr')

    # loop through the teams of the season
    for j in range(0, len(teams)):
        print("team\t" + str(j) + "\t" + )
        team = {}
        teams = browser.find_elements_by_class_name("data")[2]
        teams = teams.find_elements_by_tag_name('tr')
        #click on "info"
        teams[j].find_elements_by_tag_name('td')[3].find_element_by_tag_name('a').click()
        wait_for_ajax(browser)
        #get team info
        teamInfos = browser.find_elements_by_class_name("data")[1].find_elements_by_tag_name('tr')
        info = {}
        for inf in teamInfos:
            tds = inf.find_elements_by_tag_name('td')
            key = str(tds[0].text).replace(":", "")
            if key == "Stadio":
                splitted = str(tds[1].text).split("\n")
                info[key] = splitted[0]
                info['Capacity'] = splitted[1]
            else:
                info[camelCaseIt(str(tds[0].text).replace(":", ""))] = str(tds[1].text).replace("\n", " ")

        # download team logo
        # teamPictureUrl = browser.find_element_by_class_name("emblem").find_element_by_tag_name('img').get_attribute('src')
        # img = requests.get(teamPictureUrl).content
        #info['teamLogo'] = img

        ###done with info -> back
        browser.back()
        wait_for_ajax(browser)

        #click on "rosa"
        teams = browser.find_elements_by_class_name("data")[2]
        teams = teams.find_elements_by_tag_name('tr')
        teams[j].find_elements_by_tag_name('td')[5].find_element_by_tag_name('a').click()
        wait_for_ajax(browser)
        roster = {
            "portiere": [],
            "difesa": [],
            "centrocampo": [],
            "attacco": []
        }
        #get team roster (rosa)
        teamRosters = browser.find_elements_by_class_name("data")[2].find_elements_by_tag_name('tr')
        for row in teamRosters:
            player = {}
            #print('-----------'+row.text)
            txt  = str(row.text)
            if(txt == "Portiere" or txt == "Difesa" or txt == "Centrocampo" or txt == "Attacco" or txt == "Allenatore" or txt == "Allenatore in seconda"):
                role = txt.lower()
            else:
                tds = row.find_elements_by_tag_name("td")
                if(role == "allenatore in seconda"):
                    role = "allenatore"

                player['role'] = role
                if(role != "allenatore"):
                    player['number'] = tds[1].text
                player['name'] = tds[2].text
                player['nationality'] = tds[4].text
                birth = str(tds[5].text).split('.')
                if(len(birth) == 3): #birth might be non-present
                    birth = birth[2] + "-" + birth[1] + "-" + birth[0]
                    player['birth'] = birth + "T" + "00:00:00:000+01:00"

                # download player picture
                # playerPictureUrl = tds[0].find_element_by_tag_name('img').get_attribute('src')
                # img = requests.get(playerPictureUrl).content
                # player['picture'] = img
                if(role == "allenatore"):
                    roster[role] = player
                    break
                else:
                    roster[role].append(player)
        browser.back()
        ###done with rosa -> back

        #aggregate info and roster to team
        team['info'] = info
        team['roster'] = roster
        #append team to teams
        season['team'].append(team)
        wait_for_ajax(browser)

    print(json.dumps(season))
    f = open("results/season" + str(season['year']).replace("/", "-") + ".json", "w+")
    f.write(json.dumps(season))
    f.close()
    browser.back()
    wait_for_ajax(browser)

print("------ %s seconds ------" % (time.time() - start_time))
exit(0)