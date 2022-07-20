from tkinter import Y
import requests
import urllib3
import json
import pandas
import calplot
import numpy as np
import pandas as pd
from pandas.io.json import json_normalize
import matplotlib.pyplot as plt
from matplotlib import style
 
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
activity_df = pandas.json_normalize(my_fulldataset)

cols = ['name', 'type', 'distance', 'moving_time', 'elapsed_time', 'average_speed', 'max_speed', 'start_date_local','location_city','location_country','achievement_count','kudos_count','start_latlng','end_latlng','map.summary_polyline']
#specifying data (creating table with only the useful information)

activity_df = activity_df[cols]

def viewdata(data):
    #easy insight into data in any table
    print(data.columns)
    #see 'template'
    print(data.shape)
    #dimensions
    print(data['type'].value_counts())
    #see distribution of activities

activity_df["start_date_local"] = pd.to_datetime(activity_df['start_date_local'])
activity_df = activity_df.set_index('start_date_local')
#converting to datetime and setting as the index
activity_df['distance'] = round(activity_df['distance']/1000,2) 
#conversion from m to km
activity_df['average_speed'] = round(activity_df['average_speed'] * 3.6,2)
activity_df['max_speed'] = round(activity_df['max_speed'] * 3.6,2)
#conversion from m/s to km/h

#creating tables of activities
bike_activities_df = activity_df.loc[activity_df['type'] == 'Ride']
walk_activities_df = activity_df.loc[activity_df['type']=='Walk']

total_distance = bike_activities_df["distance"].sum()
total_moving_time = bike_activities_df["moving_time"].sum()
total_elapsed_time = bike_activities_df["elapsed_time"].sum()
total_achievements = bike_activities_df["achievement_count"].sum()
total_kudos = bike_activities_df["kudos_count"].sum()
num_bikes = len(bike_activities_df)
#just curious

style.use('fast')

heatmap = calplot.calplot(data = bike_activities_df['distance'],how='sum',cmap="YlGn",suptitle="Distance Heatmap",dayticks=False,figsize=(10,8))

avgspeed_distance = pd.DataFrame(bike_activities_df, columns=['average_speed', 'distance'])
avgspeed_distance.plot(x = 'distance', y = 'average_speed', kind = 'scatter')
plt.title("Average Speed vs Distance")
plt.xlabel("Distance (KM)")
plt.ylabel("Average Speed (KM/H)")

achievement_distance = pd.DataFrame(bike_activities_df, columns=['kudos_count','distance'])
achievement_distance.plot(x='distance',y='kudos_count',kind='scatter')
plt.title("Kudos Count vs Distance")
plt.xlabel("Distance (KM)")
plt.ylabel("Kudos Count")

def cumulative(bike_activities):
    plt.figure("Cumulative Distance")
    listx = []
    for i in range(0,len(bike_activities)):
        listx.append(i)
    cumulative_distance = bike_activities_df['distance'].cumsum(axis=0)
    plt.plot(listx,cumulative_distance)
    plt.title("Cumulative Distance")
    plt.xlabel("Activity #")
    plt.ylabel("Distance (KM)")

cumulative(bike_activities_df)
#cumulative distance

""" def bikehisto(distances):
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
    plt.ylabel('Frequency') """

# figure3 = plt.figure("Figure 3")
# fig3 = bikehisto(bike_distance_list)
plt.show()