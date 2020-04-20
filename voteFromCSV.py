import re
import json
import os
import time
import random
#####PARAMETERS
LEAGUE = "Serie A"
TOTAL_ROUND = 38
season_list = ["15-16", "16-17", "17-18", "18-19"]

#####JSON PATH
json_filename = "ita-serie-a_filledV2"
json_toOpen = "data/csv/json/"+json_filename + ".json"
json_toSave = "data/csv/json_updated/"+json_filename + "_withVotes" + ".json"
f = open(json_toOpen, "r")
json_championship = json.load(f)
f.close();

for s in season_list:
    season = season_list.index(s)
    for r in range(0, TOTAL_ROUND):
        filename = "Voti_Fantacalcio_Stagione_20" + s + "_Giornata_" + str(r+1)
        filepath = 'data/csv/' + LEAGUE + " " + s + " csv/" + filename + '.csv'
        print("Season " + s + "| round " + str(r+1) + "| " )
        with open(filepath) as f:
           line = f.readline()
           cnt = 1
           while line:
               splitted = str(line.strip()).split(";")
               if splitted[1] == "":
                   if "Voti Fantacalcio" in str(splitted[0]) or "Solo su" in str(splitted[0]) or "QUESTO FILE" in str(splitted[0]) or "E' DA " in str(splitted[0]):
                       break
                   team = splitted[0]
                   #serie A exception
                   if team == "VERONA":
                       team = "HELLAS"
                   # print("Team name ---- " + team)
                   #new team detected
                   matchArray = json_championship["season"][season]["round"][r]["match"]
                   for m in matchArray:
                       if re.search(team, m["homeTeam"], re.IGNORECASE):
                           # print(team + "    ---? " + m["homeTeam"])
                           lineup = m["homeLineup"]["player"]
                           break

                       elif re.search(team, m["awayTeam"], re.IGNORECASE):
                           # print(team + "    ---? " + m["awayTeam"])
                           lineup = m["awayLineup"]["player"]
                           break

                    #now you have the target lineup to insert the votes

                   line = f.readline()      #read the header line (worthless)
                   c=0  #DEBUG
                   cc=0 #DEBUG
                   while line:
                       line = f.readline()
                       player = str(line.strip()).split(";")
                       if player[1] == "ALL":
                           #RANDOM VOTE FOR THE UNLUCKY GUYS
                           for l in lineup:
                               if "starter" in l:
                                   if l["starter"] is True:
                                       if "vote" not in l:
                                           randomVote = random.randrange(55, 70, 5)/10
                                           # print("Random vote inserted! " + l["name"] + " randomly assigned with " + str(randomVote))
                                           l["vote"] = randomVote
                           break
                       vote = player[3].replace("*", "")
                       #to remove abbreviated name like A in GOMEZ A
                       name = player[2].rstrip("\'")
                       name = re.sub(r"\s.$", "", name)


                       for l in lineup:
                            if re.search(name, l["name"], re.IGNORECASE):
                                l["vote"] = float(vote)
                                c += 1      #DEBUG
                                break
                       cc +=1   #DEBUG
                   # print(team + " HIT RATE " +str(c)+"/"+str(cc))   #DEBUG
               line = f.readline()
               cnt += 1

f = open(json_toSave, "w+")
json_data = json.dumps(json_championship)
f.write(json_data)
f.close()
print("CSV import done")


