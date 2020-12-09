import datetime

from utils.auth import zju_auth

def ecard(username: str, password: str):
    res = {}
    try:
        # zju auth session
        sess, _ = zju_auth.login(
            username=username,
            password=password
        )

        # ecard basic info
        resp = sess.get(url='http://mapp.zju.edu.cn/lightapp/lightapp/getCardDetail').json()
        card = resp['data']['query_card']['card'][0]
        account = card['account']

        # today cost
        params = { 'account': '{}'.format(account) }
        resp = sess.get(url='http://mapp.zju.edu.cn/lightapp/lightapp/getCardBalance', params=params).json()
        balance = int(resp['data']['query_accinfo']['accinfo'][0]['balance']) / 100.0
        today = datetime.date.today()
        oneday = datetime.timedelta(days=1) 
        yesterday = today - oneday
        yesterday = yesterday.strftime("%Y%m%d")
        params = {
            'curpage': '1',
            'pagesize': '10',
            'account': '{}'.format(account),
            'queryStart': yesterday,
            'queryEnd': yesterday
        }
        resp = sess.get(url='http://mapp.zju.edu.cn/lightapp/lightapp/getHistoryConsumption', params=params).json()
        items = resp['data']['query_his_total']['total']
        total_cost = sum([int(item['sign_tranamt']) / 100 for item in items])
        current_time = datetime.datetime.now()
        res['date'] = yesterday
        res['balance'] = balance
        res['query_time'] = current_time.strftime("%Y%m%d%H%M%S")
        res['total_cost'] = total_cost
        res['items'] = items
    except Exception:
        pass 
    finally:
        return res