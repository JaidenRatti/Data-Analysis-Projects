import time
import requests
import urllib3
import json
import pandas
import csv
import calplot
import calmap
import numpy as np
import math
import pandas as pd
from pandas.io.json import json_normalize
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from datetime import datetime
import july
from july.utils import date_range
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


f = open('test.json')
data = json.load(f)
clientid = data["client_id"]
clientsecret = data["client_secret"]
refreshtoken = data["refresh_token"]
#data & tokens from hidden json
auth_link = "https://www.strava.com/oauth/token"
activities_link = "https://www.strava.com/api/v3/athlete/activities"

payload = {
    'client_id': clientid,
    'client_secret': clientsecret,
    'refresh_token': refreshtoken,
    'grant_type': "refresh_token",
    'f': 'json'
    }

res = requests.post(auth_link, data=payload, verify=False)
access_token = res.json()['access_token']
#use refresh token to get new access token

heading = {'Authorization': 'Bearer ' + access_token}
param = {'per_page': 150, 'page':1}
my_fulldataset = requests.get(activities_link, headers=heading, params=param).json()

all_activities = pandas.json_normalize(my_fulldataset)





def viewdata(data):
    print(data.columns)
    print(data.shape)
    print(data['type'].value_counts())
    #see distribution of bikes --> walks --> hikes

#viewdata(all_activities)

bike_data = []
run_data = []
hike_data = []
walk_data = []

def create_bike_dataset(full):
    for i in range(0,len(full))[::-1]:
    #oldest entries appear at top
        if(full[i]["type"]=="Ride"):
            bike_data.append(full[i])
    return bike_data

def create_run_dataset(full):
    for i in range(0,len(full))[::-1]:
        if(full[i]["type"]=="Run"):
            run_data.append(full[i])
    return run_data

def create_hike_dataset(full):
    for i in range(0,len(full))[::-1]:
        if(full[i]["type"]=="Hike"):
            hike_data.append(full[i])
    return hike_data

def create_walk_dataset(full):
    for i in range(0,len(full))[::-1]:
        if(full[i]["type"]=="Walk"):
            walk_data.append(full[i])
    return walk_data

#currently not optimized...ignore

hike_list = create_hike_dataset(my_fulldataset)
bike_list = create_bike_dataset(my_fulldataset)
run_list = create_run_dataset(my_fulldataset)
walk_list = create_walk_dataset(my_fulldataset)

#analyzing bike data (for now.. going to make this to analyze any type later)

def distances(bike_data):
    bike_distances= []
    for data in bike_data:
        raw_distance = data["distance"]
        real_distance = round(raw_distance/1000,2)
        #convert from m-->km
        bike_distances.append(real_distance)
    return bike_distances

def avg_speed(bike_data):
    avg_bike_speeds = []
    for data in bike_data:
        raw_avg_bike_speed = data["average_speed"]
        real_avg_bike_speed = round(raw_avg_bike_speed*3.6,2)
        #convert from m/s to km/h
        avg_bike_speeds.append(real_avg_bike_speed)
    return avg_bike_speeds


dates = date_range("2020-01-01","2020-12-31")
data = np.random.randint(0,14,len(dates))
july.heatmap(dates, data, title='Bike Activity', cmap="github")

bike_distance_list = distances(bike_list)
bike_avg_speed_list = avg_speed(bike_list)
#print(bike_avg_speed_list)

style.use('fast')
figure1 = plt.figure("Figure 1")
ax1 = figure1.add_subplot(1,1,1)

def animate(data):
    #print(data)
    listx = []
    listy = []
    for i in range(0,len(data)):
        listx.append(i)
        listy.append(data[i])
    ax1.clear()
    ax1.plot(listx,listy, color="#fc4c02")
    ax1.set_xlabel('xth bike ride')
    ax1.set_ylabel('distance in km')
    ax1.set_title('Bike Rides & Distances')
ani = animation.FuncAnimation(figure1, animate(bike_distance_list), interval=1000)

figure2 = plt.figure("Figure 2")

def animate2(distances,avgspeed):
    listx=[]
    listy=[]
    for i in range(0,len(data)):
        listx.append(distances)
        listy.append(avgspeed)
    plt.scatter(listx,listy, s=50,c="#fc4c02",)
    plt.title('Avg Speed (km/h) vs Distance (km)')
    plt.xlabel('Distance (km)')
    plt.ylabel('Average Speed (km/h)')
an = animation.FuncAnimation(figure2, animate2(bike_distance_list, bike_avg_speed_list), interval=1000)

plt.show()
