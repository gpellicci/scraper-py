import json
import os
import time
import unidecode

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

files = ["ita-serie-a", "bundesliga", "eng-premier-league", "fra-ligue-1", "esp-primera-division"]
links = ["https://www.sofascore.com/it/torneo/calcio/italy/serie-a/23", "https://www.sofascore.com/it/torneo/calcio/germany/bundesliga/35", "https://www.sofascore.com/it/torneo/calcio/england/premier-league/17", "https://www.sofascore.com/it/torneo/calcio/france/ligue-1/34", "https://www.sofascore.com/it/torneo/calcio/spain/laliga/8"]
months = ["Gen", "Feb", "Mar", "Apr", "Mag", "Giu", "Lug", "Ago", "Set", "Ott", "Nov", "Dic"]
months_num = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
STARTING_YEAR = 15  #2015
ACTUAL_YEAR = 19    #2019


linkIndex = 3
url = links[linkIndex]          #pick links[i] to choose the season
filename = files[linkIndex]     #json filename

# with open("data/" + filename + ".txt") as file:
#     json_championship = json.load(file)
# f = open("data/" + filename + "_filled.txt", "w+")
webdriverPath = "./chromedriver"
if os.name == 'nt':
    webdriverPath += ".exe"
browser = webdriver.Chrome(webdriverPath)
browser.maximize_window()
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

#loop through the seasons
li_text = []
for l in li:
    li_text.append(l.find_element_by_tag_name("a").text)
index = li_text.index(str(STARTING_YEAR) + "/" + str(STARTING_YEAR + 1))
for p in range(0, 1):#index):
    k = index - p       #4-0 = 4  ----> 4-3 = 1
    print("season " + li_text[k])

    # get on the desired season
    browser.get(url)
    wait_for_ajax(browser)
    dropdown = browser.find_elements_by_css_selector("div.dropdown.dropdown-select")[0]
    browser.execute_script("arguments[0].scrollIntoView(true);", dropdown)
    li = browser.find_element_by_xpath("//*[@id='pjax-container-main']/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[3]/div/div/ul").find_elements_by_tag_name("li")
    dropdown.click()
    ##
    #li[i] which season?
    li[k].find_element_by_tag_name("a").click()
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
    season = {
        "round" : []
    }
    #loop through the rounds of the season
    for i in range(0, 12):#len(li)):
        f = open("data/" + filename + "_filled.txt", "r")
        json_championship = json.load(f)
        f.close()
        round = {
            "match" : []
        }
        dropdown.click()
        browser.execute_script("arguments[0].scrollIntoView(true);", li[i])
        li[i+1].find_element_by_tag_name("a").click()
        # loop through the matches to scrape data
        wait_for_ajax(browser)
        matches = browser.find_elements_by_class_name("js-event-list-tournament-events")
        for m in matches:
            if (m.is_displayed()):
                matches_click = m
                break
        matches_click = matches_click.find_elements_by_tag_name("a")

        #loop through the matches of that week
        match_count = 0
        for j in range(0, len(matches_click)):
            matchStatus = str(matches_click[j].find_element_by_css_selector("div.cell__section.status").text).replace("\n", " ")
            #if match is not over (delayed, not yet played and so on)
            if "FIN" not in matchStatus:
                continue

            matches_click[j].click()
            homeTeamChecked = matches_click[j].find_elements_by_class_name("event-team")[0].text
            match_array = json_championship["season"][p]["round"][i]["match"]
            match_index = -1
            for index_match, m in enumerate(match_array):
                if(homeTeamChecked in m["homeTeam"]):
                    match_index = index_match
                    break
            if(match_index == -1):
                continue
            try:
                element = WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "js-details-widget-container"))
                )
            except:
                pass
            wait_for_ajax(browser)

            matchInfo = {
                "statisticHome" : [],
                "statisticAway": []
            }
            #scroll back to top of window
            browser.execute_script("arguments[0].scrollIntoView(true);", browser.find_element_by_css_selector("a.h-interactive.js-event-link"))
            # click statistics tab
            browser.find_element_by_xpath("//*[@id='pjax-container-main']/div/div[2]/div/div/div/div[1]/div[3]/div[3]/div/div[2]/div/div/div[1]/div[3]/ul/li[2]").click()

            wait_for_ajax(browser)
            # get statistics
            stats = browser.find_element_by_id("statistics-period-ALL").find_elements_by_class_name("stat-group-event")
            for s in stats:
                browser.execute_script("arguments[0].scrollIntoView(true);", s)
                stat = {}
                statName = ""
                for idx, e in enumerate(str(s.text).split('\n')):
                    if idx % 3 == 0:
                        tmp = e
                    elif idx % 3 == 1:
                        statName = e.title().replace(' ', '').replace("'", "")  # CamelCase it
                        stat = {
                            statName : tmp
                        }
                        matchInfo['statisticHome'].append(stat)
                    else:
                        stat = {
                            statName : e
                        }
                        matchInfo['statisticAway'].append(stat)
            #add the match statistics to the json
            print("season "+str(p)+" round "+str(i)+" match "+str(match_count))
            json_championship["season"][p]["round"][i]["match"][index_match]["statisticHome"] = matchInfo["statisticHome"]
            json_championship["season"][p]["round"][i]["match"][index_match]["statisticAway"] = matchInfo["statisticAway"]

            #scroll back to top of window
            browser.execute_script("arguments[0].scrollIntoView(true);", browser.find_element_by_css_selector("a.h-interactive.js-event-link"))

            #get votes
            mainWindow = browser.window_handles[0];
            browser.find_element_by_xpath("//*[@id='pjax-container-main']/div/div[2]/div/div/div/div[1]/div[3]/div[3]/div/div[2]/div/div/div[1]/div[3]/ul/li[3]").click()
            wait_for_ajax(browser)
            #open extended match info page in new tab
            browser.find_element_by_xpath("//*[@id='tab-event-widget-lineups']/a").click()
            wait_for_ajax(browser)
            handles = browser.window_handles
            for h in handles:
                if(h.title() != mainWindow.title()):
                    newWindow = h
            browser.switch_to.window(newWindow)
            #you are now on the extended match info page
            #get players votes
            #click statistics
            browser.find_element_by_xpath("//*[@id='pjax-container-main']/div/div[2]/div/div[2]/ul/li[2]").click()
            wait_for_ajax(browser)
            #click on home team tab
            #home=visible, away=hidden
            # teamButtons = browser.find_elements_by_class_name("item-row item-row--fancy")[0].find_elements_by_tag_name("span")
            # teamButtons[1].click()
            rows = browser.find_element_by_xpath("//*[@id='player-statistics-tab-summary']/table/tbody").find_elements_by_tag_name("tr")
            for row in rows:
                if("hidden" in row.get_attribute("class")):
                    continue
                tds = row.find_elements_by_tag_name("td")
                # vote = {}
                # vote['player'] = tds[1].text
                playerName = tds[1].text
                playerNumber =  tds[0].find_element_by_tag_name("span").get_attribute("textContent")
                # vote['vote'] = tds[11].text
                value = tds[11].text

                if("home" in row.get_attribute("class")):
                    # homeTeam["player"].append(vote)
                    tmp = json_championship["season"][p]["round"][i]["match"][index_match]["homeLineup"]["player"]
                    playerIndex = -1
                    #print("HOME checking for "+playerName)
                    for count, t in enumerate(tmp):
                        if (t["number"] == playerNumber):
                            playerIndex = count
                            break
                    if(playerIndex != -1):
                        json_championship["season"][p]["round"][i]["match"][index_match]["homeLineup"]["player"][playerIndex]["vote"] = value
                else:
                    # awayTeam["player"].append(vote)
                    tmp = json_championship["season"][p]["round"][i]["match"][index_match]["awayLineup"]["player"]
                    playerIndex = -1
                    #print("AWAY checking for "+playerName)
                    for count, t in enumerate(tmp):
                        if (t["number"] == playerNumber):
                            playerIndex = count
                            break
                    if(playerIndex != -1):
                        json_championship["season"][p]["round"][i]["match"][index_match]["awayLineup"]["player"][playerIndex]["vote"] = value

            # matchInfo["homeTeamVote"] = homeTeam
            # matchInfo["awayTeamVote"] = awayTeam

            #players votes obtained
            #done with the extended match info page -> close and switch back to main window
            browser.close()
            browser.switch_to.window(mainWindow)

            #click X and close stats panel
            browser.find_element_by_class_name("widget-close-button").click()
            match_count = match_count + 1


        json_data = json.dumps(json_championship)
        f = open("data/" + filename + "_filled.txt", "w+")
        f.write(json_data)
        f.close()

print("------ %s seconds ------" % (time.time() - start_time))
exit(0)
# #save json to file
# json_data = json.dumps(json_championship)
# print(json_data)
# f.write(json_data + '\n')
# f.close()
# print("------ %s seconds ------" % (time.time() - start_time))
# exit(0)