from locust import HttpUser, tag, task, between
import random
import copy
from config import *
from tools import get_Authorization, random_mobile
import requests

H = {
    "Accept": "application/json",
    "Authorization": "",
    "Content-Type": "application/json;charset=UTF-8"
}

with open('./Authorization.txt', 'w+') as f:
    for i in range(10):
        f.writelines(f"{get_Authorization(register_api, user_detail_api)}" + ",")

with open('./Authorization.txt') as f:
    x = f.read()
Authorization = x[:-1].split(',')


class Locust_create(HttpUser):
    wait_time = between(1, 5)
    host = "http://testing-mp-api.jiansutech.com"

    @task(

    )
    @tag("login")
    def user_login(self):

        body = {
            "mobile": random_mobile(),
            "checkCode": "47749"
        }
        token = None
        # print("=======user_login[BODY]:",body,"===========")
        with self.client.post(url=register_api, json=body) as res:
            try:
                code = res.json()['code']
                message = res.json()['message']
                print(f"________{message}")
                # token = res.json()["data"]["access_token"]
                # H["Authorization"] = "Bearer" + token
                # res_detail = requests.get(url=user_detail_api, headers=H)

                if code == 0:
                    print('Success')
                else:
                    print(f"Fail!\n==========  code : {code}, msg : {message}")
            except KeyError as k:
                print(f"Fail!\n==========  status_code : {res.status_code}")
                code = 999
        return code

    @tag("box_list")
    @task()
    def box_list_task(self):
        _headers = copy.copy(H)
        _headers['Authorization'] = random.choice(Authorization)

        with self.client.get(url=box_list_api, headers=_headers) as res:
            # print("======box_list_task:",_headers,"===========")
            try:
                code = res.json()['code']
                message = res.json()['message']
                print(f"________{message}")
                if code == 0:
                    print('Success')
                else:
                    print(f"Fail!\n==========  code : {code}, msg : {message}")
            except KeyError as k:
                print(f"Fail!\n==========  status_code : {res.status_code}")
                code = 999
        return code

    @task()
    @tag("box_detail")
    def box_detail_task(self):
        _headers = copy.copy(H)
        _headers['Authorization'] = random.choice(Authorization)

        with self.client.get(url=box_detail_api, headers=_headers) as res:
            # print("======box_detail_task:", _headers, "===========")
            try:
                code = res.json()['code']
                message = res.json()['message']
                print(f"________{message}")
                if code == 0:
                    print('Success')
                else:
                    print(f"Fail!\n==========  code : {code}, msg : {message}")
            except KeyError as k:
                print(f"Fail!\n==========  status_code : {res.status_code}")
                code = 999
        return code

    @tag("buy_box")
    @task(3)
    def buy_box_task(self):
        _headers = copy.copy(H)
        _headers['Authorization'] = random.choice(Authorization)
        data = {"payAmount": 1, "blindBoxId": box_id, "client": "H5"}
        with self.client.post(url=buy_box_api, headers=_headers, json=data) as res:
            # print("======buy_box_task:", _headers, "===========")
            try:
                code = res.json()['code']
                message = res.json()['message']
                print(f"________{message}")
                if code == 0:
                    print('Success')
                else:
                    print(f"Fail!\n==========  code : {code}, msg : {message}")
            except KeyError as k:
                print(f"Fail!\n==========  status_code : {res.status_code}")
                code = 999
            return code
