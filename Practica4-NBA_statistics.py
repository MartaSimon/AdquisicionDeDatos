import json
import numpy as np
def load_json(path):
    """
    Loads JSON file in given path into a dictionary that will
    be returned.
    Params
    -------
    path : str
    The path to the target JSON file.
    Return
    -------
    d : dic
    The dictionary with the JSON content loaded.
    """
    with open(path, "r") as input_file:
        d = json.load(input_file)
        return d
d = load_json("../kobe.json")

headers_needed = ["SEASON_ID","PLAYER_AGE","GP","REB","PTS","AST"]
header_index = np.where(np.isin(d["resultSets"]["name" == "SeasonTotalsRegularSeason"]["headers"],headers_needed))
regular_season_stats = []

for item_dict in d["resultSets"]:
    if(item_dict["name"] == "SeasonTotalsRegularSeason"):
        regular_season_stats.append(headers_needed)
        #print((item_dict["headers"] == "SEASON_ID")).index()
        for item_list in item_dict["rowSet"]:
            np_item_list = np.array(item_list)
            aux_list = list(np_item_list[header_index])
            #print(aux_list)
            regular_season_stats.append(aux_list)
        break
            
print(regular_season_stats)