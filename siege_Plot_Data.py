import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

match_Data_List = pd.read_csv("Match_records.csv", header=None).values.tolist()

map_Data = np.array(match_Data_List[0])
win_Data = np.array(match_Data_List[1], dtype=int)
loss_Data = np.array(match_Data_List[2], dtype=int)
matches_Played = np.add(win_Data, loss_Data)
winrate_Data = np.divide(win_Data*100, matches_Played)
playrate_Data = np.divide(matches_Played*100, np.sum(matches_Played))


def plot_Data():
    fig, ax = plt.subplots(dpi=180)
    img = plt.imread("ezll.jpg")
    ax.imshow(img, extent=[0, max(playrate_Data) + 0.1*100, 0, 1.1*100],aspect = "auto")
    ax.set_ylim(-0.1*100, 1.1*100)
    ax.set_xticks(ticks=np.arange(0.1*100, 1.1*100, 0.1*100))
    ax.set_xlim(0, max(playrate_Data) + 0.1*100)
    ax.spines['bottom'].set_position('center')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.grid(True, alpha=0.8, which="both")
    ax.set_ylabel("Win %")
    ax.set_xlabel("Playrate %")
    ax.scatter(playrate_Data, winrate_Data)

    for i, txt in enumerate(map_Data):
        ax.annotate(txt, (playrate_Data[i], winrate_Data[i]))
    plt.show()


plot_Data()
