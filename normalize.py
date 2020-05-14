import json
import os
import re
import time

filename = "eng.json"
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
        "ranking":json_championship["season"][i]["ranking"]["team"]
    }

    json_ranking.append(rank)
    del json_championship["season"][i]["ranking"]

    # Team normalization
    for j in range(0, len(json_championship["season"][i]["team"])):
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
    for j in range(0, len(season["round"])):
        for k in range(0, len(season["round"][j]["match"])):
            match = season["round"][j]["match"][k]
            # Home lineup
            for y in range(0, len(match["homeLineup"]["player"])):
                player = match["homeLineup"]["player"][y]
                if "enterTime" in season["round"][j]["match"][k]["homeLineup"]["player"][y]:
                    if isinstance(season["round"][j]["match"][k]["homeLineup"]["player"][y]["enterTime"], str):
                        t = season["round"][j]["match"][k]["homeLineup"]["player"][y]["enterTime"]
                        time = t.split(" ")
                        #print(time)
                        season["round"][j]["match"][k]["homeLineup"]["player"][y]["enterTime"] = int(time[0])
                        season["round"][j]["match"][k]["homeLineup"]["player"][y]["leaveTime"] = int(time[1])

            # Away lineup
            for y in range(0, len(match["awayLineup"]["player"])):
                player = match["awayLineup"]["player"][y]
                if "enterTime" in season["round"][j]["match"][k]["awayLineup"]["player"][y]:
                    if isinstance(season["round"][j]["match"][k]["awayLineup"]["player"][y]["enterTime"], str):
                        t = season["round"][j]["match"][k]["awayLineup"]["player"][y]["enterTime"]
                        time = t.split(" ")
                        season["round"][j]["match"][k]["awayLineup"]["player"][y]["enterTime"] = int(time[0])
                        season["round"][j]["match"][k]["awayLineup"]["player"][y]["leaveTime"] = int(time[1])

            if "statisticHome" in match:
                for y in range(0, len(match["statisticHome"])):
                    stat = match["statisticHome"][y]
                    if "Prec. passaggi" in stat:
                        season["round"][j]["match"][k]["statisticHome"][y]["PrecPassaggi"] = stat["Prec. passaggi"]
                        del season["round"][j]["match"][k]["statisticHome"][y]["Prec. passaggi"]

            if "statisticAway" in match:
                for y in range(0, len(match["statisticAway"])):
                    stat = match["statisticAway"][y]
                    if "Prec. passaggi" in stat:
                        season["round"][j]["match"][k]["statisticAway"][y]["PrecPassaggi"] = stat["Prec. passaggi"]
                        del season["round"][j]["match"][k]["statisticAway"][y]["Prec. passaggi"]

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
