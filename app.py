"""
YORK transit search service.
"""
import os
import pandas as pd
from flask import Flask, request, render_template
import uuid
from datetime import datetime, timezone
import pytz

# pylint: disable=C0103
cache = {}
data_stoptimes = pd.read_csv("./york_transit/stop_times.txt")
data_trips = pd.read_csv("./york_transit/trips.txt")
data_routes = pd.read_csv("./york_transit/routes.txt")
app = Flask(__name__)

class PostBodyFromComm100():
    chatId: str
    botId: str
    channel: str
    question: str
    originalQuestion: str
    visitorId: str

@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    message = "It's running!"

    """Get Cloud Run environment variables."""
    service = os.environ.get('K_SERVICE', 'Unknown service')
    revision = os.environ.get('K_REVISION', 'Unknown revision')

    return render_template('index.html',
        message=message,
        Service=service,
        Revision=revision)

@app.route('/york/transit/stop/routes', methods=['POST'])
def findRoutes():
    request_data = request.get_json()
    args = request.args
    messageType = args.get("type", default="", type=str)
    if messageType != "button":
        messageType = "quickreply"
    result = []
    messages = []
    stoptimes = []
    chatId = None
    question = None
    originalQuestion = None
    stop_id = 0
    intentId = None
    getStopTimesIntentId = "00000000-0000-0000-0000-000000000000"
    if request_data:
        if 'chatId' in request_data:
            chatId = request_data['chatId']

        if 'question' in request_data:
            question = request_data['question']

        if 'originalQuestion' in request_data:
            originalQuestion = request_data['originalQuestion']
        
        if 'intentId' in request_data:
            intentId = request_data['intentId']
        
        if 'getStopTimesIntentId' in request_data:
            getStopTimesIntentId = request_data['getStopTimesIntentId']

    if question is not None:
        stop_id = question
    elif originalQuestion is not None:
        stop_id = originalQuestion
    try:
        stopid = int(stop_id)
    except:
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
                    result.append({"type": "goToIntent", "text": row2.route_long_name,"routeId":row1.route_id, "intentId": getStopTimesIntentId })
    #print(stoptimes)
    if chatId is not None:
        cache[chatId] = {"stopId": stopid, "stoptimes": stoptimes}
    if len(result):
        #return quickreply message

        messages.append({
            "type": messageType,
            "content": {
                "message": "please choose Route:",
                "items": result
            },
            "disableChatInputArea": True
        })
    else:
        #no route found
        messages.append({
            "type": "quickreply",
            "content": {
                "message": "no routes found",
                "items": [
                    {
                        "type": "goToIntent",
                        "text": "input another stop id",
                        "intentId": intentId
                    },
                    {
                        "type": "contactAgent",
                        "text": "click to contact agent"
                    }
                ]
            }
        })

    return messages

@app.route('/york/transit/stop/route/times', methods=['POST'])
def findRouteTimes():
    request_data = request.get_json()
    chatId = None
    question = None
    originalQuestion = None
    routeName = ""
    if request_data:
        if 'chatId' in request_data:
            chatId = request_data['chatId']

        if 'question' in request_data:
            question = request_data['question']

        if 'originalQuestion' in request_data:
            originalQuestion = request_data['originalQuestion']

    if question is not None:
        routeName = question
    elif originalQuestion is not None:
        routeName = originalQuestion

    if chatId is None or routeName == "" or cache[chatId] is None:
        """Return no data found."""
        print("no data found")        
        return {"code": 0 , "data": ""}
    data = cache[chatId]
    lastTimes = getLast3Times(routeName, data["stoptimes"])
    if len(lastTimes):
        return {"code": 1 , "data": ','.join(lastTimes) }
    return {"code": 0 , "data": ""}

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

if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=server_port, host='0.0.0.0')
