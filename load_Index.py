import pandas
from numpy import random
def load_paint():
    #loads the paint names and indices as a dict
    paint_dict = pandas.read_csv("paint_index_sorted.csv", names=["Paint index", "Paint name"], engine="python",
                                  index_col=False, usecols=["Paint name", "Paint index"]).set_index(
        "Paint name").to_dict()
    return paint_dict

def load_weapon():
    #Loads the weapon names and indices as a dict
    weapon_dict = pandas.read_csv("Weapon_index_sorted.csv", names=["Weapon index", "Weapon name"], index_col=False,
                                   usecols=["Weapon name", "Weapon index"]).set_index("Weapon name").to_dict()
    return weapon_dict
