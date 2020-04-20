import json
import os
import time
import random
import unidecode
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

def time_wait():
    x = random.uniform(0.4, 0.6)
    time.sleep(x)


def wait_for_ajax(driver):
    wait = WebDriverWait(driver, 15)
    try:
        wait.until(lambda driver: driver.execute_script('return jQuery.active') == 0)
        wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    except Exception as e:
        pass

files = ["ita-serie-a", "ger-bundesliga", "eng-premier-league", "fra-ligue-1", "esp-primera-division"]
links = ["https://www.sofascore.com/it/torneo/calcio/italy/serie-a/23", "https://www.sofascore.com/it/torneo/calcio/germany/bundesliga/35", "https://www.sofascore.com/it/torneo/calcio/england/premier-league/17", "https://www.sofascore.com/it/torneo/calcio/france/ligue-1/34", "https://www.sofascore.com/it/torneo/calcio/spain/laliga/8"]
months = ["Gen", "Feb", "Mar", "Apr", "Mag", "Giu", "Lug", "Ago", "Set", "Ott", "Nov", "Dic"]
months_num = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
STARTING_YEAR = 15  #2015
ACTUAL_YEAR = 19    #2019


linkIndex = 1
url = links[linkIndex]          #pick links[i] to choose the season
filename = files[linkIndex]     #json filename

webdriverPath = "./chromedriver"
if os.name == 'nt':
    webdriverPath += ".exe"
browser = webdriver.Chrome(webdriverPath)
browser.maximize_window()
start_time = time.time()
browser.get(url)

# get on the desired season
wait_for_ajax(browser)
dropdown = browser.find_element_by_class_name("styles__MenuWrapper-cdd802-1")
ul = dropdown.find_element_by_class_name("styles__Menu-cdd802-5")
li = ul.find_elements_by_tag_name("li")
dropdown.click()
#loop through the seasons
li_text = []
for l in li:
    li_text.append(l.text)
    print(l.text)

index = li_text.index(str(STARTING_YEAR) + "/" + str(STARTING_YEAR + 1))

for p in range(0, index):
    k = index - p       #4-0 = 4  ----> 4-3 = 1
    print("season " + li_text[k])

    # get on the desired season
    time_wait()
    browser.get(url)
    wait_for_ajax(browser)
    dropdown = browser.find_element_by_class_name("styles__MenuWrapper-cdd802-1")
    browser.execute_script("arguments[0].scrollIntoView(true);", dropdown)
    ul = dropdown.find_element_by_class_name("styles__Menu-cdd802-5")
    li = ul.find_elements_by_tag_name("li")

    dropdown.click()
    ##
    #li[i] which season?
    li[k].click()
    print("Clicked on season " + dropdown.text)

    #select per-turn view
    wait_for_ajax(browser)
    time_wait()
    radioButton = browser.find_elements_by_class_name("Tabs__Header-vifb7j-0")[1].find_elements_by_class_name("Label-sc-19k9vkh-0")[1]
    browser.execute_script("arguments[0].scrollIntoView(true);", radioButton)
    time_wait()
    radioButton.click()
    wait_for_ajax(browser)

    #select turn 1
    time_wait()
    resultDiv = browser.find_element_by_class_name("u-mV12")
    browser.execute_script("arguments[0].scrollIntoView(true);", resultDiv)
    wait_for_ajax(browser)
    roundButton = resultDiv.find_element_by_class_name("styles__MenuWrapper-cdd802-1")
    roundButton.click()
    wait_for_ajax(browser)
    time_wait()
    round_li = roundButton.find_elements_by_tag_name("li")
    round_li[0].click()
    time_wait()
    print("Composed of " + str(len(round_li)) + " rounds")
    season = {
        "round" : []
    }
    #loop through the rounds of the season
    for i in range(0, len(round_li)):
        wait_for_ajax(browser)
        f = open("data/" + filename + "_filled.txt", "r")
        json_championship = json.load(f)
        f.close()
        round = {
            "match" : []
        }

        resultDiv = browser.find_element_by_class_name("u-mV12")
        roundButton = resultDiv.find_element_by_class_name("styles__MenuWrapper-cdd802-1")
        roundButton.click()
        wait_for_ajax(browser)
        browser.execute_script("arguments[0].scrollIntoView(true);", resultDiv)
        wait_for_ajax(browser)
        round_li = roundButton.find_elements_by_tag_name("li")
        browser.execute_script("arguments[0].scrollIntoView(true);", round_li[i])
        round_li[i].click()
        wait_for_ajax(browser)
        time_wait()
        browser.execute_script("arguments[0].scrollIntoView(true);", resultDiv)     ##
        # loop through the matches to scrape data
        matchDiv = resultDiv.find_element_by_class_name("styles__EventListContent-b3g57w-2")
        match_li = matchDiv.find_elements_by_class_name("EventCellstyles__Link-sc-1m83enb-0")
        print("This round is composed of " + str(len(match_li)) + " matches")

        #loop through the matches of that week
        match_count = 0
        for j in range(0, len(match_li)):
            time_wait()
            # if j > 0:
            #     time.sleep(3)
            print("---MATCH #"+ str(j))
            matchStatus = match_li[j].find_element_by_class_name("Cell-decync-0").find_element_by_class_name("Section-sc-1a7xrsb-0").get_attribute("title")

            #if match is not over (delayed, not yet played and so on)
            if "FIN" not in matchStatus:
                continue

            match_li[j].click()
            time_wait()
            wait_for_ajax(browser)
            homeTeamChecked = unidecode.unidecode(str(match_li[j].find_element_by_class_name("EventCellstyles__WinIndicator-ni00fg-3").text))

            ##specific conversion if BUNDESLIGA

            if homeTeamChecked == "Hamburger SV":
                homeTeamChecked = "Amburgo"
            elif homeTeamChecked == "Bayer 04 Leverkusen":
                homeTeamChecked = "Bayer Leverkusen"
            elif homeTeamChecked == "Bayern Munchen":
                homeTeamChecked = "Bayern Monaco"
            elif homeTeamChecked == "Borussia M'gladbach":
                homeTeamChecked = "Bor. Monchengladbach"
            elif homeTeamChecked == "1. FC Koln":
                homeTeamChecked = "Colonia"
            elif homeTeamChecked == "Eintracht Frankfurt":
                homeTeamChecked = "Eintracht Francoforte"
            elif homeTeamChecked == "Ingolstadt":
                homeTeamChecked = "FC Ingolstadt 04"
            elif homeTeamChecked == "Hertha BSC":
                homeTeamChecked = "Hertha Berlino"
            elif homeTeamChecked == "1899 Hoffenheim":
                homeTeamChecked = "Hoffenheim"
            elif homeTeamChecked == "1. FSV Mainz 05":
                homeTeamChecked = "Mainz 05"
            elif homeTeamChecked == "FC Schalke 04":
                homeTeamChecked = "Schalke 04"
            elif homeTeamChecked == "VfB Stuttgart":
                homeTeamChecked = "Stoccarda"
            elif homeTeamChecked == "Darmstadt 98":
                homeTeamChecked = "SV Darmstadt 98"
            elif homeTeamChecked == "Freiburg":
                homeTeamChecked = "Friburgo"

            ###################################

            match_array = json_championship["season"][p]["round"][i]["match"]
            match_index = -1
            for index_match, m in enumerate(match_array):
                if(m["homeTeam"] in homeTeamChecked):
                    match_index = index_match
                    break
            if(match_index == -1):
                print("-----rip****************************************")
                continue

            matchInfo = {
                "statisticHome" : [],
                "statisticAway": []
            }

            wait_for_ajax(browser)
            time_wait()
            time_wait()
            tmp = browser.find_element_by_class_name("u-mV12").find_elements_by_class_name("Label-sc-19k9vkh-0")
            # print(str(len(tmp)))
            for t in tmp:
                if t.text == "STATISTICHE":
                    browser.execute_script("arguments[0].scrollIntoView(true);", t)
                    t.click()
                    continue
            time_wait()
            wait_for_ajax(browser)
            statDiv = browser.find_element_by_xpath("/html/body/div[1]/main/div/div[2]/div/div[1]/div[4]/div/div[2]/div/div/div/div[2]/div/div[1]/div/div[2]/div[2]/div[2]/div/div[2]/div/div")
            statss = statDiv.find_elements_by_class_name("Cell-decync-0")
            for s in statss:
                browser.execute_script("arguments[0].scrollIntoView(true);", s)
                portions = s.find_elements_by_class_name("Section-sc-1a7xrsb-0")
                # [0] home stat
                # [1] stat name
                # [2] away stat
                statName = portions[1].text
                homeStat = str(portions[0].text)
                stat = {
                    statName: homeStat
                }
                matchInfo['statisticHome'].append(stat)
                awayStat = str(portions[2].text)
                stat = {
                    statName: awayStat
                }
                matchInfo['statisticAway'].append(stat)

            browser.execute_script("arguments[0].scrollIntoView(true);", resultDiv)

            #add the match statistics to the json
            print("season "+str(p)+" round "+str(i)+" match "+str(match_count))
            json_championship["season"][p]["round"][i]["match"][index_match]["statisticHome"] = matchInfo["statisticHome"]
            json_championship["season"][p]["round"][i]["match"][index_match]["statisticAway"] = matchInfo["statisticAway"]

            time_wait()
            #scroll back to top of window
            browser.execute_script("arguments[0].scrollIntoView(true);", resultDiv)

            match_count = match_count + 1



        json_data = json.dumps(json_championship)
        f = open("data/" + filename + "_filled.txt", "w+")
        f.write(json_data)
        f.close()

print("------ %s seconds ------" % (time.time() - start_time))
exit(0)