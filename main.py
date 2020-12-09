from monitor.api import ecard
from notice.api import dingding

import os
import sys


class task():
    def __init__(self):
        pass

    def hello(self, ecard_username: str, ecard_password: str, dingding_token: str, dingding_secret: str, delta=600):
        data = ecard(
            username=ecard_username,
            password=ecard_password,
            delta=delta
        )
        name = data['name']
        dingding(
            title='Hello World!',
            text='Hello {}, GitHub Action OK!'.format(name),
            token=dingding_token,
            secret=dingding_secret
        )

    def run(self, ecard_username: str, ecard_password: str, dingding_token: str, dingding_secret: str, delta=600):
        data = ecard(
            username=ecard_username,
            password=ecard_password,
            delta=delta
        )
        balance = data['balance']
        total_cost = data['total_cost']
        for item in data['recent_cost']:
            occtime = item['occtime']
            mercname = item['mercname']
            tranname = item['tranname']
            sign_tranamt = int(item['sign_tranamt']) / 100
            text = "ecard monitor\n\n{}-{}-{} {}:{}:{}\n\n{} {}\n\n消费 {:.2f} 元 剩余 {:.2f} 元 累计 {:.2f} 元".format(
                occtime[0:4], occtime[4:6], occtime[6:8],
                occtime[8:10], occtime[10:12], occtime[12:14], mercname, tranname,
                -1*sign_tranamt, balance, -1*total_cost
            )
            dingding(
                title="新的校园卡消费信息~",
                text=text,
                token=dingding_token,
                secret=dingding_secret
            )

if __name__ == "__main__":
    obj = task()
    if sys.argv[1] == 'hello':
        obj.hello(
            ecard_username=os.getenv('ECARD_USERNAME'),
            ecard_password=os.getenv('ECARD_PASSWORD'),
            dingding_token=os.getenv('DINGDING_TOKEN'),
            dingding_secret=os.getenv('DINGDING_SECRET')
        )
    else:
        obj.run(
            ecard_username=os.getenv('ECARD_USERNAME'),
            ecard_password=os.getenv('ECARD_PASSWORD'),
            dingding_token=os.getenv('DINGDING_TOKEN'),
            dingding_secret=os.getenv('DINGDING_SECRET')
        )
