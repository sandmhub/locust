import requests
from faker import Faker

from config import Host


def my_faker(func: str):
    f = Faker(locale='zh_CN')
    return getattr(f, func)()


def random_mobile():
    return my_faker('phone_number')


def get_Authorization(url,url_2):
    """
    :param url:  Host + "/mp/auth/appRegister"
    :param url_2: Host + "/blockbzz/product/user/detail"
    :return:
    """

    body = {
        "mobile": random_mobile(),
        "checkCode": "47749"
    }
    req = requests.post(url=url, json=body)
    try:
        Authorization = req.json()['data']['access_token']

        requests.get(url=url_2, headers={'Authorization': "Bearer " + Authorization})
        return "Bearer " + Authorization
    except KeyError as k:
        print(f"get_Authorization 返回 {req.json()}")
        return


import csv


with open("mobile.csv", "w+", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["mobile"])
    for i in range(10):
        m = random_mobile()
        writer.writerow([m])


