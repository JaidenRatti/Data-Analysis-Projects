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
import statistics as stat
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
param = {'per_page': 200, 'page':1}
my_fulldataset = requests.get(activities_link, headers=heading, params=param).json()

all_activities = pandas.json_normalize(my_fulldataset)

def viewdata(data):
    print(data.columns)
    #see 'template'
    print(data.shape)
    #dimensions
    print(data['type'].value_counts())
    #see distribution of bikes --> walks --> hikes

#viewdata(all_activities)

#creating lists of specific activity types
def create_activity_dataset(attribute, full_dataset):
    activity_data = []
    for i in range(0,len(full_dataset))[::-1]:
        #oldest entries at top
        if full_dataset[i]["type"]==attribute:
            activity_data.append(full_dataset[i])
    return activity_data

hike_list = create_activity_dataset("Hike",my_fulldataset)
bike_list = create_activity_dataset("Ride",my_fulldataset)
run_list = create_activity_dataset("Run",my_fulldataset)
walk_list = create_activity_dataset("Walk",my_fulldataset)


#analyzing bike data (for now... since biking is the only activity I do... going to make this to analyze any type later)

def unique_list_attribute(attribute, bike_data):
    list_of_attribute = []
    for data in bike_data:
        raw_data = data[attribute]
        if attribute == "average_speed" or attribute == "max_speed":
            real_data = round(raw_data*3.6,2)
            #convert m/s-->km/h
        if attribute =="distance":
            real_data = round(raw_data/1000,2)
            #convert m-->km
        list_of_attribute.append(real_data)
    return list_of_attribute

bike_distance_list = unique_list_attribute("distance",bike_list)
#creating list of just distances
bike_avg_speed_list = unique_list_attribute("average_speed", bike_list)
#^^
bike_max_speed_list = unique_list_attribute("max_speed",bike_list)
#^^

def country(bike_data):
    stationary_counter = 0
    canada_counter = 0
    country_counter = {}
    for data in bike_data:
        print(data["location_country"])

#Issue with Strava API (displaying all location_country data has only home country and not country the activity actually took place in :( )
#will come back to this

def get_distance_of_instance(list_of_data, distances):
    highest = max(list_of_data)
    index_highest = list_of_data.index(highest)
    instance_highest = (distances[index_highest])
    return highest, instance_highest

max_speed_distance = get_distance_of_instance(bike_max_speed_list, bike_distance_list)
#"How far (km) was the ride where I got max speed?"
max_avg_speed_distance = get_distance_of_instance(bike_avg_speed_list, bike_distance_list)
#"How far (km) was the ride where I got my highest average speed?"
max_distance = get_distance_of_instance(bike_distance_list, bike_distance_list)
#"How far was my furthest ride!"

print("Highest Speed Recorded is " +str(max_speed_distance[0])+ "km/h on a " + str(max_speed_distance[1])+ "km ride")
print("Highest Average Speed Recorded is " +str(max_avg_speed_distance[0])+"km/h on a " + str(max_avg_speed_distance[1])+"km ride")
print("Furthest Distance Recorded is " +str(max_distance[0]) +"km" )
#displaying the variables above

proper = []
for i in range(0,len(bike_list)):
    size = len(bike_list[i]["start_date"])
    proper.append(bike_list[i]["start_date"][:size-10])

dates = date_range(proper[0],proper[-1])
data = bike_distance_list
july.heatmap(dates, data, title='Bike Activity', cmap="github")
july.calendar_plot(dates, data, title = 'Bike Activity',cmap='github')
#play around more with this

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
ani = animation.FuncAnimation(figure1, animate(bike_distance_list))

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
an = animation.FuncAnimation(figure2, animate2(bike_distance_list, bike_avg_speed_list))

figure3 = plt.figure("Figure 3")

def animate3(distances):
    bins = [0,5,10,20,30,40,50,60,70]
    median_distance = stat.median(distances)
    mean_distance = round(stat.mean(distances),2)
    mode_distance = stat.mode(distances)
    color = "#fc4c02"
    color2 = "#fc4c03"
    color3 = "#fc4c04"
    plt.axvline(median_distance, color=color, label='Median Distance (' +str(median_distance)+')')
    plt.axvline(mean_distance, color=color2, label='Mean Distance ('+str(mean_distance)+')')
    plt.axvline(mode_distance, color=color3, label='Mode Distance ('+str(mode_distance)+")")
    plt.hist(distances, bins=bins, edgecolor = 'black')
    plt.legend()
    plt.title('Distance by Count of Rides')
    plt.xlabel('Distance (km)')
    plt.ylabel('Frequency')

a = animation.FuncAnimation(figure3,animate3(bike_distance_list))
plt.show()
