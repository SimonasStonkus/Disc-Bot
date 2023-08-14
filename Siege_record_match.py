import pandas as pd
import numpy as np

siege_Maps = []
with open("siege_Maps.csv") as x:
    siege_Maps.append(x.readline().split(", "))
siege_Maps = siege_Maps[0]

match_Data_List = pd.read_csv("Match_records.csv", header=None).values.tolist()

map_Data = match_Data_List[0]
win_Data = list(np.array(match_Data_List[1], dtype=int))
loss_Data = list(np.array(match_Data_List[2], dtype=int))


def record_Match(Map, Outcome):
    if Map in map_Data:
        if Outcome == "Win":
            win_Data[map_Data.index(Map)] += 1
        else:
            loss_Data[map_Data.index(Map)] += 1
    else:
        map_Data.append(Map)
        if Outcome == "Win":
            win_Data.append(1)
            loss_Data.append(0)
        else:
            win_Data.append(0)
            loss_Data.append(1)
    np.savetxt("Match_records.csv", [map_Data, win_Data, loss_Data], delimiter=",", fmt='% s')
