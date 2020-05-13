import json
import os
import re
import time

filename = "ger-bundesliga_filledV2.json"
toOpen = "data/toNormalize/"+filename
ranking_file = "data/toNormalize/done/RANKING_"+filename
season_file = "data/toNormalize/done/SEASON_"+filename
team_file = "data/toNormalize/done/TEAM_"+filename


f = open(toOpen, "r")
json_championship = json.load(f)
f.close()

json_season = []
json_ranking = []
json_team = []

# remove rankings from main document
for i in range(0, len(json_championship["season"])):
    rank = {
        "league":json_championship["name"],
        "year":json_championship["season"][i]["year"],
        "ranking":json_championship["season"][i]["ranking"]
    }

    json_ranking.append(rank)
    del json_championship["season"][i]["ranking"]

    # Team normalization
    for j in range(0, 2):#len(json_championship["season"][i]["team"])):
        tmp = json_championship["season"][i]["team"][j]
        player_array = {
            "league":json_championship["name"],
            "year":json_championship["season"][i]["year"],
            "team":tmp["info"][0]["squadra"],
            "player":tmp["roster"][0]["player"],
            "info":tmp["info"][0]
        }
        json_team.append(player_array)

    del json_championship["season"][i]["team"]

    season = json_championship["season"][i]
    season["league"] = json_championship["name"]
    json_season.append(season)



f = open(ranking_file, "w+")
f.write(json.dumps(json_ranking))
f.close()

f = open(team_file, "w+")
f.write(json.dumps(json_team))
f.close()

f = open(season_file, "w+")
f.write(json.dumps(json_season))
f.close()

print("NORMALIZATION completed")
