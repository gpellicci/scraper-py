import json
import os
import re
import time

#json_data = json.dumps(json_championship)
filename = "ger-bundesliga_filledV2.json"
toOpen = "data/V2/"+filename
toSave = "data/V2/CHANGEDTYPE-"+filename

f = open(toOpen, "r")
json_championship = json.load(f)
f.close();


####ROUND
for i in range(0, len(json_championship["season"])):
    for j in range(0, len(json_championship["season"][i]["round"])):
        for k in range(0, len(json_championship["season"][i]["round"][j]["match"])):
            match = json_championship["season"][i]["round"][j]["match"][k]
            match["homeResult"] = int(match["homeResult"])
            match["awayResult"] = int(match["awayResult"])
            if match["attendance"] != "a porte chiuse":
                match["attendance"] = int(match["attendance"])

            ##GOAL
            if "goal" in match:
                for y in range(0, len(match["goal"])):
                    goal = match["goal"][y]
                    goal["homePartial"] = int(goal["homePartial"])
                    goal["awayPartial"] = int(goal["awayPartial"])
                    goal["minute"] = int(goal["minute"])

            ##HOME LINEUP
            for y in range(0, len(match["homeLineup"]["player"])):
                player = match["homeLineup"]["player"][y]
                if "number" in player and player["number"] != '':
                    player["number"] = int(player["number"])
                if "leaveTime" in player and " " not in player["leaveTime"]:
                    player["leaveTime"] = int(player["leaveTime"])
                if "enterTime" in player and " " not in player["enterTime"]:
                    player["enterTime"] = int(player["enterTime"])

            ##AWAY LINEUP
            for y in range(0, len(match["awayLineup"]["player"])):
                player = match["awayLineup"]["player"][y]
                if "number" in player and player["number"] != '':
                    player["number"] = int(player["number"])
                if "leaveTime" in player and " " not in player["leaveTime"]:
                    player["leaveTime"] = int(player["leaveTime"])
                if "enterTime" in player and " " not in player["enterTime"]:
                    player["enterTime"] = int(player["enterTime"])



            ####STATISTIC HOME
            if "statisticHome" in match:
                for y in range(0, len(match["statisticHome"])):
                    stat = match["statisticHome"][y]
                    if "Possesso palla" in stat:
                        stat["PossessoPalla"] = int(str(stat["Possesso palla"]).replace("%", ""))
                        del stat["Possesso palla"]
                    if "Tiri totali" in stat:
                        stat["TiriTotali"] = int(stat["Tiri totali"])
                        del stat["Tiri totali"]
                    if "Tiri in porta" in stat:
                        stat["TiriInPorta"] = int(stat["Tiri in porta"])
                        del stat["Tiri in porta"]
                    if "Tiri fuori" in stat:
                        stat["TiriFuori"] = int(stat["Tiri fuori"])
                        del stat["Tiri fuori"]
                    if "Tiri bloccati" in stat:
                        stat["TiriBloccati"] = int(stat["Tiri bloccati"])
                        del stat["Tiri bloccati"]
                    if "Calci d'angolo" in stat:
                        stat["CalciDAngolo"] = int(stat["Calci d'angolo"])
                        del stat["Calci d'angolo"]
                    if "Fuorigioco" in stat:
                        stat["Fuorigioco"] = int(stat["Fuorigioco"])
                    if "Cartellini gialli" in stat:
                        stat["CartelliniGialli"] = int(stat["Cartellini gialli"])
                        del stat["Cartellini gialli"]
                    if "Cartellini rossi" in stat:
                        stat["CartelliniRossi"] = int(stat["Cartellini rossi"])
                        del stat["Cartellini rossi"]
                    if "Tiri in area" in stat:
                        stat["TiriInArea"] = int(stat["Tiri in area"])
                        del stat["Tiri in area"]
                    if "Tiri da fuori area" in stat:
                        stat["TiriDaFuoriArea"] = int(stat["Tiri da fuori area"])
                        del stat["Tiri da fuori area"]
                    if "Salvataggi del portiere" in stat:
                        stat["SalvataggiDelPortiere"] = int(stat["Salvataggi del portiere"])
                        del stat["Salvataggi del portiere"]
                    if "Passaggi" in stat:
                        stat["Passaggi"] = int(stat["Passaggi"])
                    if "Precisione passaggi" in stat:
                        stat["PrecisionePassaggi"] = int(re.sub(r' (.*)', '', str(stat["Precisione passaggi"])))
                        del stat["Precisione passaggi"]
                    if "Falli" in stat:
                        stat["Falli"] = int(stat["Falli"])
                    if "Parate" in stat:
                        stat["Parate"] = int(stat["Parate"])
                    if "Contrasti vinti" in stat:
                        stat["ContrastiVinti"] = int(stat["Contrasti vinti"])
                        del stat["Contrasti vinti"]
                    if "Contrasti aerei vinti" in stat:
                        stat["ContrastiAereiVinti"] = int(stat["Contrasti aerei vinti"])
                        del stat["Contrasti aerei vinti"]


            ####STATISTIC AWAY
            if "statisticAway" in match:
                for y in range(0, len(match["statisticAway"])):
                    stat = match["statisticAway"][y]
                    if "Possesso palla" in stat:
                        stat["PossessoPalla"] = int(str(stat["Possesso palla"]).replace("%", ""))
                        del stat["Possesso palla"]
                    if "Tiri totali" in stat:
                        stat["TiriTotali"] = int(stat["Tiri totali"])
                        del stat["Tiri totali"]
                    if "Tiri in porta" in stat:
                        stat["TiriInPorta"] = int(stat["Tiri in porta"])
                        del stat["Tiri in porta"]
                    if "Tiri fuori" in stat:
                        stat["TiriFuori"] = int(stat["Tiri fuori"])
                        del stat["Tiri fuori"]
                    if "Tiri bloccati" in stat:
                        stat["TiriBloccati"] = int(stat["Tiri bloccati"])
                        del stat["Tiri bloccati"]
                    if "Calci d'angolo" in stat:
                        stat["CalciDAngolo"] = int(stat["Calci d'angolo"])
                        del stat["Calci d'angolo"]
                    if "Fuorigioco" in stat:
                        stat["Fuorigioco"] = int(stat["Fuorigioco"])
                    if "Cartellini gialli" in stat:
                        stat["CartelliniGialli"] = int(stat["Cartellini gialli"])
                        del stat["Cartellini gialli"]
                    if "Cartellini rossi" in stat:
                        stat["CartelliniRossi"] = int(stat["Cartellini rossi"])
                        del stat["Cartellini rossi"]
                    if "Tiri in area" in stat:
                        stat["TiriInArea"] = int(stat["Tiri in area"])
                        del stat["Tiri in area"]
                    if "Tiri da fuori area" in stat:
                        stat["TiriDaFuoriArea"] = int(stat["Tiri da fuori area"])
                        del stat["Tiri da fuori area"]
                    if "Salvataggi del portiere" in stat:
                        stat["SalvataggiDelPortiere"] = int(stat["Salvataggi del portiere"])
                        del stat["Salvataggi del portiere"]
                    if "Passaggi" in stat:
                        stat["Passaggi"] = int(stat["Passaggi"])
                    if "Precisione passaggi" in stat:
                        stat["PrecisionePassaggi"] = int(re.sub(r' (.*)', '', str(stat["Precisione passaggi"])))
                        del stat["Precisione passaggi"]
                    if "Falli" in stat:
                        stat["Falli"] = int(stat["Falli"])
                    if "Parate" in stat:
                        stat["Parate"] = int(stat["Parate"])
                    if "Contrasti vinti" in stat:
                        stat["ContrastiVinti"] = int(stat["Contrasti vinti"])
                        del stat["Contrasti vinti"]
                    if "Contrasti aerei vinti" in stat:
                        stat["ContrastiAereiVinti"] = int(stat["Contrasti aerei vinti"])
                        del stat["Contrasti aerei vinti"]










####RANKING
for i in range(0, len(json_championship["season"])):
    for j in range(0, len(json_championship["season"][i]["ranking"]["team"])):
        tmp = json_championship["season"][i]["ranking"]["team"][j]
        tmp["goalScored"] = int(tmp["goalScored"])
        tmp["loss"] = int(tmp["loss"])
        tmp["won"] = int(tmp["won"])
        tmp["goalAllowed"] = int(tmp["goalAllowed"])
        tmp["goalScored"] = int(tmp["goalScored"])
        tmp["draw"] = int(tmp["draw"])
        tmp["played"] = int(tmp["played"])
        tmp["points"] = int(tmp["points"])

####TEAM
for i in range(0, len(json_championship["season"])):
    for j in range(0, len(json_championship["season"][i]["team"])):
        ##ROSTER
        roster = json_championship["season"][i]["team"][j]["roster"][0]["player"]
        for k in range(0, len(roster)):
            player = roster[k]
            if "number" in player:
                player["number"] = int(player["number"])

        #INFO Niente da fare
        #info = json_championship["season"][i]["team"][j]["info"]





f = open(toSave, "w+")
json_data = json.dumps(json_championship)
f.write(json_data)
f.close()
print("clown done")