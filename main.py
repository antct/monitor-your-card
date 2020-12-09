from monitor.api import ecard
from notice.api import dingding

import os
import sys


class task():
    @staticmethod
    def hello(ecard_username: str, ecard_password: str, dingding_token: str, dingding_secret: str):
        dingding(
            title='Hello World!',
            text='Hello {}, GitHub Action OK!'.format(ecard_username),
            token=dingding_token,
            secret=dingding_secret
        )
        task.run(
            ecard_username=ecard_username,
            ecard_password=ecard_password,
            dingding_token=dingding_token,
            dingding_secret=dingding_secret
        )

    @staticmethod
    def run(ecard_username: str, ecard_password: str, dingding_token: str, dingding_secret: str):
        data = ecard(
            username=ecard_username,
            password=ecard_password
        )
        text = '***\n\n'
        text += '{} 消费 {:.2f} 元 余额 {:.2f} 元'.format(data['date'], -1 * data['total_cost'], data['balance'])
        for item in data['items'][::-1]:
            occtime = item['occtime']
            mercname = item['mercname']
            tranname = item['tranname']
            sign_tranamt = int(item['sign_tranamt']) / 100
            text += '\n\n***\n\n'
            text += "{}-{}-{} {}:{}:{}\n\n{} {} 消费 {:.2f} 元".format(
                occtime[0:4], occtime[4:6], occtime[6:8],
                occtime[8:10], occtime[10:12], occtime[12:14], mercname, tranname,
                -1*sign_tranamt
            )
        text += '\n\n***'
        dingding(
            title="昨日校园卡消费信息~",
            text=text,
            token=dingding_token,
            secret=dingding_secret
        )


if __name__ == "__main__":
    if sys.argv[1] == 'hello':
        task.hello(
            ecard_username=os.getenv('ECARD_USERNAME'),
            ecard_password=os.getenv('ECARD_PASSWORD'),
            dingding_token=os.getenv('DINGDING_TOKEN'),
            dingding_secret=os.getenv('DINGDING_SECRET')
        )
    elif sys.argv[1] == 'run':
        task.run(
            ecard_username=os.getenv('ECARD_USERNAME'),
            ecard_password=os.getenv('ECARD_PASSWORD'),
            dingding_token=os.getenv('DINGDING_TOKEN'),
            dingding_secret=os.getenv('DINGDING_SECRET')
        )
    else:
        pass
