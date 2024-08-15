# -*- coding: utf-8 -*-

import json
import requests


def do_post(api_url, query_body):
    # headers = {'content-type': 'application/json'}
    response = requests.post(api_url, json=query_body)
    json_res = json.loads(response.text)
    print(json_res)


def do_get(api_url):
    response = requests.get(api_url)
    json_res = json.loads(response.text)
    print(json_res)

api_url = "http://127.0.0.1:8080/york/transit/stop/routes?type=button"
request_body = {
    "question": "9700",
	"channel": "Live Chat",
	"chatId": "f16dde4f-ec6a-4102-badb-09ed7bb5725e",
	"botId": "cdf2da6b-2cc4-4c1d-a3c3-83d5dc8fc7f2",
	"visitorId": "5e6567ae-1e2d-46da-bd68-43139ee9316f",
    "intentId": "5e6567ae-1e2d-46da-bd68-43139ee9316f",
    "getStopTimesIntentId":"5e6567ae-1e2d-46da-bd68-43139ee9316f"
}
#do_post(api_url , request_body)

api_url = "http://127.0.0.1:8080/york/transit/stop/route/times"
request_body = {
    "question": "HIGHWAY 7",
	"channel": "Live Chat",
	"chatId": "f16dde4f-ec6a-4102-badb-09ed7bb5725e",
	"botId": "cdf2da6b-2cc4-4c1d-a3c3-83d5dc8fc7f2",
	"visitorId": "5e6567ae-1e2d-46da-bd68-43139ee9316f",
}
do_post(api_url , request_body)

api_url = "http://127.0.0.1:8080/york/transit/stop/route/times"
request_body = {
    "question": "HIGHWA",
	"channel": "Live Chat",
	"chatId": "f16dde4f-ec6a-4102-badb-09ed7bb5725e",
	"botId": "cdf2da6b-2cc4-4c1d-a3c3-83d5dc8fc7f2",
	"visitorId": "5e6567ae-1e2d-46da-bd68-43139ee9316f",
}
do_post(api_url , request_body)

