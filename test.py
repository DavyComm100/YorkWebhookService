# -*- coding: utf-8 -*-
import pandas as pd
from datetime import datetime, timezone
import pytz

data_stoptimes = pd.read_csv("./york_transit/stop_times.txt")
data_trips = pd.read_csv("./york_transit/trips.txt")
data_routes = pd.read_csv("./york_transit/routes.txt")
    
def findRoutes(stop_id):
    result = []
    stoptimes=[]
    try:
        stopid = int(stop_id)
    except ValueError:
        stopid = 0
    for row in data_stoptimes[data_stoptimes["stop_id"] == stopid].itertuples():
        for row1 in data_trips[data_trips["trip_id"] == row.trip_id].itertuples():
            for row2 in data_routes[data_routes["route_id"] == row1.route_id].itertuples():                
                stoptimes.append({"route_id":row1.route_id, "route_name":row2.route_long_name, "arrival_time": row.arrival_time })
                exist = False
                for item in result:
                    if item["routeId"] == row2.route_id:
                        exist = True

                if exist == False:
                    result.append({"routeId": row2.route_id, "name": row2.route_long_name })
    print(stoptimes)
    return getLast3Times("HIGHWAY 7", stoptimes)

def getLast3Times(routeName: str, stoptimes: []):
    result = []
    utc = pytz.timezone('UTC')
    now = utc.localize(datetime.utcnow())
    la = pytz.timezone('America/New_York')
    local_date = now.astimezone(la)
    local_time = local_date.strftime('%X')

    for r in stoptimes:
        if r["route_name"] == routeName:
            tocompare_time = r["arrival_time"].replace(" ", "0")
            if tocompare_time >= local_time:
                result.append(tocompare_time)
    
    result.sort()
    return result[:3]

print(findRoutes("9700"))