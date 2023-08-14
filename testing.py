from collections_extended import bag
import timeit
import numpy as np
import requests
import time
import random
import datetime
import json
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
from astropy.time import Time


# starttime = timeit.default_timer()
# old = list(np.arange(1,300,1))
# new = list(np.arange(200,400,1))
#
# old = ["One","Two","Three","Four","Four","Four"]
# new = ["Three","Four","Five","Six","Three"]
# test_a = list(bag(old)-bag(new))
# test_b = list(bag(new)-bag(old))
#
# print("The time difference using bags is:", timeit.default_timer() - starttime)
#
# print(test_a)
# print(test_b)
#
# starttime = timeit.default_timer()
# # old = list(np.arange(1,300,1))
# # new = list(np.arange(200,400,1))
# old = ["One", "Two", "Three", "Four", "Four", "Four"]
# new = ["Three", "Four", "Five", "Six", "Three"]
# new_diff = new.copy()
# old_diff = old.copy()
#
# for i in range(len(old)):
#     if old[i] in new_diff:
#         new_diff.pop(new_diff.index(old[i]))
#
# for i in range(len(new)):
#     if new[i] in old_diff:
#         old_diff.pop(old_diff.index(new[i]))
#
# print("The time difference for old method is:", timeit.default_timer() - starttime)
# print(old_diff)
# print(new_diff)
# #
# a = []
# print(bool(a))
# if bool(a) == False:
#     print("Not empty")
# else:
#     print("Empty")

# counter_1 = 0
# counter_2 = 0
#
# wait_1 = 0.5
# wait_2 = 0.1
# request_amnt = 100
#
# starttime = timeit.default_timer()
# for i in range(request_amnt):
#     time.sleep(wait_1)
#     counter_1 += wait_1
#     request = (requests.get("https://steamcommunity.com/market/priceoverview/?appid=730&currency=3&market_hash_name=UMP-45%20|%20Carbon%20Fiber%20(Minimal%20Wear")).json()
#     if request is None:
#         print("Currently rate limited, please wait.")
#         print("Rate lmiting started at:", counter_2+counter_1, "seconds")
#         while request is None:
#             time.sleep(wait_2)
#             counter_2 += wait_2
#             request = (requests.get(
#                 "https://steamcommunity.com/market/priceoverview/?appid=730&currency=3&market_hash_name=UMP-45%20|%20Carbon%20Fiber%20(Minimal%20Wear")).json()
#
# print("timeit time", timeit.default_timer() - starttime)
# print("Total time taken:", counter_2+counter_1, "seconds")
# print("Rate limited for:",counter_2, "seconds")
# print("Average time per request:",(counter_2+counter_1)/request_amnt,"seconds")
cookie = {'steamLoginSecure': '76561198002365621%7C%7CeyAidHlwIjogIkpXVCIsICJhbGciOiAiRWREU0EiIH0.eyAiaXNzIjogInI6MTQyRV8yMjYxRTIyRF9DMTBFOCIsICJzdWIiOiAiNzY1NjExOTgwMDIzNjU2MjEiLCAiYXVkIjogWyAid2ViIiBdLCAiZXhwIjogMTY4NDg1ODUwOCwgIm5iZiI6IDE2NzYxMzA1NjksICJpYXQiOiAxNjg0NzcwNTY5LCAianRpIjogIjBEMkVfMjI4REE3RUNfODRBQkYiLCAib2F0IjogMTY4MTgyNDgwNSwgInJ0X2V4cCI6IDE2OTk0NzkyNzksICJwZXIiOiAwLCAiaXBfc3ViamVjdCI6ICIzNy4yMjguMjM5LjE2OSIsICJpcF9jb25maXJtZXIiOiAiMzcuMjI4LjIzOS4xNjkiIH0.01Ic5UjzNB_mJ48cOYlaSDQcLLJtaJ5ezRjgvbA2PeV2pS7ZTo1O_SJ1D_F92ysHom0xE-OrIOZkzj2FheRhAQ'}

# wait_interval = 1
# starttime = timeit.default_timer()
# for i in range(1000):
#     # time.sleep(random.uniform(1.5, 4))
#     time.sleep(wait_interval)
#     request = (requests.get("https://steamcommunity.com/market/priceoverview/?appid=730&currency=3&market_hash_name=UMP-45%20|%20Carbon%20Fiber%20(Minimal%20Wear)", cookies=cookie)).json()
#     if request is None:
#         print("Rate limited after", i, "requests. Total time elapsed:",timeit.default_timer()-starttime,"seconds.")
#         break
#     if i % 20 == 0:
#         print("Still testing, currently completed", i, "requests. Total time elapsed:", timeit.default_timer()-starttime, "seconds.")

# today = date.today()
#
# print(today-1)

# a = datetime.date(2022, 11, 28).isoformat()
# print(a)
# a1 = datetime.date.fromisoformat(a)
# print(a1)
#
# b = datetime.date.today().isoformat()
# b1 = datetime.date.fromisoformat(b)
# print(b)
#
# print(b1-a1)
#
# delta_T = datetime.timedelta(days = 5)
#
# if b1-a1 > delta_T:
#     print("yep")
#

# str = "Dreams & Nightmares Case"
# print(str)
# if "&" in str:
#     str = str.replace("&", "%26")
#     print("yep")
# print(str)
#
# print(datetime.datetime.now())

# history = json.load(open("./Inventories/76561198002365621_history.json", encoding="utf8"))
#
# dates = list(history.keys())
# items = []
# values = []
# tick_labels = []
# for date in dates:
#     iso_date = datetime.datetime.fromisoformat(date)
#     dates[dates.index(date)] = iso_date
#     tick_labels.append(iso_date.strftime("%d/%m/%y"))
#     items.append(history[date]["items"])
#     values.append(history[date]["value"])
#
# tick_labels = [*set(tick_labels)]
# tick_locations = []
# for i in range(len(tick_labels)):
#     tick_locations.append(datetime.datetime.strptime(tick_labels[i]+"-12:00:00", "%d/%m/%y-%H:%M:%S"))
#     tick_labels[i] = tick_labels[i][0:5]

#
#
# for date in dates:
#     dates[dates.index(date)] = Time(date.isoformat(), format="isot").mjd
# #dates = Time(datetime.datetime.isoformat(dates), format="isot").mjd
# x_y_spline = make_interp_spline(dates,values)
# print(dates)
# dates_ = np.linspace(min(dates), max(dates),500)
# values_ = x_y_spline(dates_)
#
# plt.plot(dates, values)
# #plt.ylim(0, 1350)
# plt.ylabel("Inventory value (€)")
# plt.xticks(tick_locations, tick_labels)
# plt.show()

#history = json.load(open("./Inventories/76561198082782188_history.json", encoding="utf8"))

# history = json.load(open("./Inventories/76561198002365621_history.json", encoding="utf8"))
#
# dates = list(history.keys())
# items = []
# values = []
# tick_labels = []
# for date in dates:
#     iso_date = datetime.datetime.fromisoformat(date)
#     dates[dates.index(date)] = iso_date
#     tick_labels.append(iso_date.strftime("%d/%m/%y"))
#     items.append(history[date]["items"])
#     values.append(history[date]["value"])
# tick_labels = [*set(tick_labels)]
# tick_locations = []
# for i in range(len(tick_labels)):
#     tick_locations.append(datetime.datetime.strptime(tick_labels[i]+"-12:00:00", "%d/%m/%y-%H:%M:%S"))
#     tick_labels[i] = tick_labels[i][0:5]

#
#
# for date in dates:
#     dates[dates.index(date)] = Time(date.isoformat(), format="isot").mjd
# #dates = Time(datetime.datetime.isoformat(dates), format="isot").mjd
# x_y_spline = make_interp_spline(dates,values)
# print(dates)
# dates_ = np.linspace(min(dates), max(dates),500)
# values_ = x_y_spline(dates_)
# fig, ax = plt.subplots()
#
#
# ax.plot(dates, values,color = "green")
# ax.set_ylabel("Inventory value (€)")
# ax.fill_between(dates, min(values)-min(values)*0.001, values, alpha=.3, color = "green")
# ax.annotate(f"{values[-1]:.2f}€", (dates[-1], values[-1]), horizontalalignment='center', verticalalignment='bottom')
# ax.scatter(dates[-1],values[-1],color = "green")
# ax.grid()
# ax.set_xticks(tick_locations, tick_labels)
# if dates[-1]-dates[0] >= datetime.timedelta(days=10):
#     ax.set_xlim(dates[-1]-datetime.timedelta(days=10),dates[-1])
# else:
#     ax.set_xlim(dates[-1] - datetime.timedelta(days=7), dates[-1])

# ax2 = ax.twinx()
# ax2.tick_params(axis='y')
# ax2.set_ylabel("Items")
# ax2.annotate(items[-1], (dates[-1], items[-1]), horizontalalignment='center', verticalalignment='bottom')
# ax2.plot(dates, items)
# ax2.scatter(dates[-1],items[-1])
#plt.ylim(0, 1350)
# plt.show()

test = {}
#test2= {"test1": {"test2": 1, "test3":2}

history = json.load(open("./Inventories/76561198082782188_history.json", encoding="utf8"))
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
    ax.set_xlim(dates[5], dates[-1])
else:
    ax.set_xlim(dates[-1] - datetime.timedelta(days=7), dates[-1])
plt.show()
