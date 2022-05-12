from locust import HttpUser, tag, task, between,SequentialTaskSet
import random
import copy
from config import *
from tools import get_Authorization, random_mobile

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


class ShopTask(SequentialTaskSet):
    wait_time = between(1, 5)


    @task
    def user_login(self):

        body = {
            "mobile": random_mobile(),
            "checkCode": "47749"
        }
        # print("=======user_login[BODY]:", body, "===========")
        with self.client.post(url=register_api, json=body) as res:
            try:
                code = res.json()['code']
                message = res.json()['message']

                if code == 0:
                    print(f"________{message}")
                else:
                    print(f"Fail!\n==========  code : {code}, msg : {message}")
            except KeyError as k:
                print(f"Fail!\n==========  status_code : {res.status_code}")
                code = 999
        return code

    @tag("shop_detail")
    @task
    def shop_detail_task(self):
        _headers = copy.copy(H)
        _headers['Authorization'] = random.choice(Authorization)

        with self.client.get(url=shop_detail_api, headers=_headers) as res:
            print("======shop_detail_task:", _headers, "===========")
            try:
                code = res.json()['code']
                message = res.json()['message']

                if code == 0:
                    print(f"________{message}")
                else:
                    print(f"Fail!\n==========  code : {code}, msg : {message}")
            except KeyError as k:
                print(f"Fail!\n==========  status_code : {res.status_code}")
                code = 999
        return code

    @tag("shop_product")
    @task
    def shop_product_list_task(self):
        _headers = copy.copy(H)
        _headers['Authorization'] = random.choice(Authorization)
        self.product_id = None
        self.refId = None
        with self.client.get(url=shop_product_list_api, headers=_headers) as res:
            # print("======shop_product_list_task:", _headers, "===========")
            try:
                code = res.json()['code']
                message = res.json()['message']
                res_product_list = res.json()["data"]["items"]
                self.product_id = random.choice(res_product_list)['id']
                self.refId = random.choice(res_product_list)['refId']

                if code == 0:
                    print(f"________{message}")
                else:
                    print(f"Fail!\n==========  code : {code}, msg : {message}")

            except KeyError as k:
                print(f"Fail!\n==========  status_code : {res.status_code}")

    @tag("shop_product")
    @task
    def shop_product_detail_task(self):
        _headers = copy.copy(H)
        _headers['Authorization'] = random.choice(Authorization)
        product_detail_api = shop_product_detail_api.format(self.product_id)
        print("=======product_detail_api==========", product_detail_api)
        with self.client.get(url=product_detail_api, headers=_headers) as res:
            # print("======shop_product_detail_task:", _headers, "===========")
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

    @tag("buy_shop")
    @task
    def buy_shop_product_task(self):
        _headers = copy.copy(H)
        _headers['Authorization'] = random.choice(Authorization)
        data = {"orderType": "DEAL",
                "payAmount": 1,
                "productAmount": 1,
                "productTemplateId": self.refId,
                "client": "H5"}
        with self.client.post(url=buy_shop_product_api, headers=_headers, json=data) as res:
            print("======shop_product_detail_task:", _headers, "===========")
            try:
                code = res.json()['code']
                message = res.json()['message']

                if code == 0:
                    print(f"________{message}")
                else:
                    print(f"Fail!\n==========  code : {code}, msg : {message}")
            except KeyError as k:
                print(f"Fail!\n==========  status_code : {res.status_code}")
                code = 999
            return code


class MyUserGroup(HttpUser):
    """ 定义线程组 """
    tasks = [ShopTask]
    host = "http://testing-mp-api.jiansutech.com"


