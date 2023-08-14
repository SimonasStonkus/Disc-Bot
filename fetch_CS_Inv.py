import json
import requests
import time
import os
import csv
from collections_extended import bag
from collections import Counter
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import datetime
load_dotenv()

cookie = {'steamLoginSecure': os.getenv("STEAM_COOKIE")}

#################
# Unnecessary
item_cols = json.load(open("item_Quality_Colour.json"))


def colored(rgb_Col, text):
    r, g, b = rgb_Col
    return "\033[38;2;{};{};{}m{} \033[39m".format(r, g, b, text)
##################


def fetch_inv(steam_ID):
    new_inv = []

    time.sleep(5)   # Wait in case of rate limiting
    json_data = (requests.get("https://steamcommunity.com/inventory/"+steam_ID+"/730/2?l=english&count=1000", cookies=cookie)).json()
    if json_data is None and os.path.isfile("./Inventories/json/"+steam_ID+".json") is False:      # Check for rate limiting and if there is no fallback inventory
        raise Exception("Error: Rate limited, private inventory or incorrect steamID64")
    elif json_data is None:
        json_data = json.load(open("./Inventories/json/" + steam_ID + ".json", encoding="utf-8"))  # Load fallback inventory
        print("Error: Rate limited, private inventory or incorrect steamID64. Using fallback.")
    with open("./Inventories/json/" + steam_ID + ".json", "w", encoding="utf-8") as outfile:        # Change this to just use the already cut down files, full jsons take up too much space
        outfile.write(json.dumps(json_data))    # Load inventory data into json file

    # json_data = json.load(open("3.json",encoding="utf-8")) ### Testing from local json, remove for publishing

    descriptions = json_data["descriptions"]
    assets = json_data["assets"]

    for i in range(len(assets)):
        class_id = assets[i]["classid"]  # Getting class id of current item in json
        description_index = next((i for i, item in enumerate(descriptions) if item["classid"] == class_id))  # Getting index of description of item depending on the class id from assets
        if descriptions[description_index]["marketable"]:  # Checking to see if item is marketable
            new_inv.append(descriptions[description_index]["market_hash_name"])

    if os.path.isfile("./Inventories/"+steam_ID+".csv"):
        print("Inventory data already exists, checking for changes...")
        old_inv = list(csv.reader(open("./Inventories/"+steam_ID+".csv", "r", encoding="utf-8"), delimiter="`"))[0]
        new_items = list(bag(new_inv) - bag(old_inv))
        removed_items = list(bag(old_inv) - bag(new_inv))

        if bool(new_items):
            print("New items in inventory are:", list(bag(new_inv) - bag(old_inv)))

        if bool(removed_items):
            print("Items removed from the inventory are:", list(bag(old_inv) - bag(new_inv)))

        if not bool(new_items) and not bool(removed_items):
            print("No new items in inventory.")

        with open("./Inventories/"+steam_ID+".csv", "w", encoding="utf-8") as inv:
            inv.write("`".join(new_inv)) # Using "`" instead of "," as delimiter due to "," being in some item names

    else:
        with open("./Inventories/"+steam_ID+".csv", "w", encoding="utf-8") as inv:
            inv.write("`".join(new_inv)) # Using "`" instead of "," as delimiter due to "," being in some item names
            new_items = []
            removed_items = []
        print("New inventory recorded")

    # for i in range(len(descriptions)):
    #     if descriptions[i]["tradable"] == 1:
    #         tags = list(filter(lambda tag: tag['category'] == 'Rarity', descriptions[i]["tags"]))
    #         print(colored(item_cols[tags[0]["localized_tag_name"]], descriptions[i]["market_hash_name"]))
    return descriptions, new_inv, new_items, removed_items  # Descriptions are unnecessary for now, new_items and removed_items are here if I can think of something interesting to do with them


def get_inventory_value(items):
    total = 0
    today_date = datetime.datetime.now()  # For checking time difference
    print("Calculating inventory value...")
    price_dict = json.load(open("item_prices.json", encoding="utf-8"))  # Loading cached price data

    for market_hash_name in items:
        if market_hash_name not in price_dict or today_date - datetime.datetime.fromisoformat(price_dict[market_hash_name]["date_updated"]) > datetime.timedelta(hours=12):  # Run this if there is no cached price data or if it is older than 5 days
            market_hash_name_cleaned = market_hash_name.replace("&", "%26")  # Hard-coded solution for items such as "Dreams & Nightmares Case" causing weird issues with the market api
            time.sleep(3)
            print(market_hash_name)
            price_data = (requests.get("https://steamcommunity.com/market/priceoverview/?appid=730&currency=3&market_hash_name="+market_hash_name_cleaned, cookies=cookie)).json()
            print(price_data)
            if price_data is None and market_hash_name in price_dict:  # If rate limited, use available data even if out of date
                total += float(price_dict[market_hash_name]["price"])
                print(market_hash_name)
                continue
            elif price_data is None and market_hash_name not in price_dict:
                continue

            if "median_price" in price_data:  # Checks for low volume items that may not have median price or lowest price
                total += float(price_data["median_price"][0:-1].replace(",", ".").replace("-", "0").replace(" ", ""))
                price_dict[market_hash_name] = {"price": price_data["median_price"][0:-1].replace(",", ".").replace("-", "0").replace(" ", ""), "date_updated": today_date.isoformat()}  # Cache new price
            elif "lowest_price" in price_data:
                total += float(price_data["lowest_price"][0:-1].replace(",", ".").replace("-", "0").replace(" ", ""))
                price_dict[market_hash_name] = {"price": price_data["lowest_price"][0:-1].replace(",", ".").replace("-", "0").replace(" ", ""), "date_updated": today_date.isoformat()}  # Cache new price
            else:
                continue
        else:
            print(market_hash_name)
            total += float(price_dict[market_hash_name]["price"])

    with open("item_prices.json", "w+", encoding="utf8") as file:  # Save new prices to json
        json.dump(price_dict, file)

    return float(f"{total:.2f}")


# Get item value, store in json for history, implement this into get_inventory_value
def get_item_value(market_hash_name):
    today_date = datetime.datetime.now()
    if os.path.isfile("item_prices_new.json"):
        price_dict = json.load(open("item_prices_new.json", encoding="utf-8"))
    else:
        price_dict = {}

    market_hash_name_cleaned = market_hash_name.replace("&", "%26")  # Hard-coded solution for items such as "Dreams & Nightmares Case" causing weird issues with the market api
    price_data = (requests.get("https://steamcommunity.com/market/priceoverview/?appid=730&currency=3&market_hash_name=" + market_hash_name_cleaned, cookies=cookie)).json()
    if market_hash_name not in price_dict:
        price_dict[market_hash_name] = {}  # Create key so that it is accessible with the date

    price_dict[market_hash_name][today_date.isoformat()] = price_data["lowest_price"][0:-1].replace(",", ".").replace("-", "0").replace(" ", "")

    with open("item_prices_new.json", "w+", encoding="utf8") as file:  # Save new prices to json
        json.dump(price_dict, file)


#get_item_value("StatTrak\u2122 SSG 08 | Parallax (Field-Tested)")


def get_plot(STEAM_ID):  # Code copied from testing file, needs work but its fine for now
    history = json.load(open("./Inventories/"+STEAM_ID+"_history.json", encoding="utf8"))
    dates = list(history.keys())

    items = []
    values = []
    tick_labels = []
    for date in dates:
        iso_date = datetime.datetime.fromisoformat(date)
        dates[dates.index(date)] = iso_date
        tick_labels.append(iso_date.strftime("%d/%m/%y"))
        items.append(history[date]["items"])
        values.append(history[date]["value"])
    tick_labels = [*set(tick_labels)]
    tick_locations = []
    for i in range(len(tick_labels)):
        tick_locations.append(datetime.datetime.strptime(tick_labels[i] + "-12:00:00", "%d/%m/%y-%H:%M:%S"))
        tick_labels[i] = tick_labels[i][0:5]

    fig, ax = plt.subplots()
    ax.plot(dates, values, color="green")
    ax.set_ylabel("Inventory value (€)")
    ax.fill_between(dates, min(values) - min(values) * 0.001, values, alpha=.3, color="green")
    ax.annotate(f"{values[-1]:.2f}€", (dates[-1], values[-1]), horizontalalignment='center', verticalalignment='bottom')
    ax.scatter(dates[-1], values[-1], color="green")
    ax.grid()
    ax.set_xticks(tick_locations, tick_labels)

    if dates[-1] - dates[0] >= datetime.timedelta(days=10):
        ax.set_xlim(dates[-1] - datetime.timedelta(days=10), dates[-1])
    else:
        ax.set_xlim(dates[-1] - datetime.timedelta(days=7), dates[-1])

    plt.savefig("value_plot.png")
    plt.close()

def get_value_and_save(STEAM_ID):   # This is a bad way to do this, think of something better, probably need to refactor the entire code
    today_date = datetime.datetime.now().isoformat()
    descriptions, inventory, new, removed = fetch_inv(STEAM_ID)
    value = get_inventory_value(inventory)

    if os.path.isfile("./Inventories/" + STEAM_ID + "_history.json"):
        history = json.load(open("./Inventories/" + STEAM_ID + "_history.json", encoding="utf8"))
        if today_date not in history or history[today_date]["items"] != len(inventory):  # Given that im using a full iso date (hours minutes seconds included) these checks are completely useless
            history[today_date] = {"value": value, "items": len(inventory)}

    else:
        history = {today_date: {"value": value, "items": len(inventory)}}

    with open("./Inventories/" + STEAM_ID + "_history.json", "w+", encoding="utf8") as file:
        json.dump(history, file)

    get_plot(STEAM_ID)
    return value


def force_price_update():
    price_list = json.load(open("item_prices.json", encoding="utf-8"))
    items = list(price_list.keys())
    today_date = datetime.datetime.now()

    for market_hash_name in items:
        if today_date - datetime.datetime.fromisoformat(price_list[market_hash_name]["date_updated"]) > datetime.timedelta(hours=8):
            market_hash_name_cleaned = market_hash_name.replace("&", "%26")  # Hard-coded solution for items such as "Dreams & Nightmares Case" causing weird issues with the market api
            time.sleep(4)
            print(market_hash_name)
            price_data = (requests.get("https://steamcommunity.com/market/priceoverview/?appid=730&currency=3&market_hash_name="+market_hash_name_cleaned, cookies=cookie)).json()
            print(price_data)
            if price_data is None:  # If rate limited, use available data even if out of date
                continue

            if "median_price" in price_data:  # Checks for low volume items that may not have median price or lowest price
                price_list[market_hash_name] = {"price": price_data["median_price"][0:-1].replace(",", ".").replace("-", "0").replace(" ", ""), "date_updated": today_date.isoformat()}  # Cache new price
            elif "lowest_price" in price_data:
                price_list[market_hash_name] = {"price": price_data["lowest_price"][0:-1].replace(",", ".").replace("-", "0").replace(" ", ""), "date_updated": today_date.isoformat()}  # Cache new price
            else:
                continue

    with open("item_prices.json", "w+", encoding="utf8") as file:  # Save new prices to json
        json.dump(price_list, file)


##############
# Unnecessary
def return_inv(descriptions):
    inv_string = ""
    for i in range(len(descriptions)):
        if descriptions[i]["marketable"] == 1:
            tags = list(filter(lambda tag: tag['category'] == 'Rarity', descriptions[i]["tags"]))
            inv_string += colored(item_cols[tags[0]["localized_tag_name"]], descriptions[i]["market_hash_name"])
            inv_string += "\n"
    return inv_string
##############


# descriptions, inventory, new, removed = fetch_inv("76561198002365621") ## 76561198082782188
# print()
# Returned_string = return_inv(descriptions)
# print(Returned_string)
# force_price_update()
#
# total_value = get_value_and_save("76561198082782188")
# print("The total value of the inventory is: ", total_value, "€")

# total_value = get_value_and_save("76561198002365621")
# print("The total value of the inventory is: ", total_value, "€")



