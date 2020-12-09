import datetime

from utils.auth import zju_auth

def ecard(username: str, password: str, delta=60000):
    res = {}
    try:
        sess, _ = zju_auth.login(
            username=username,
            password=password
        )
        resp = sess.get(url='http://mapp.zju.edu.cn/lightapp/lightapp/getCardDetail').json()
        card = resp['data']['query_card']['card'][0]
        account = card['account']
        name = card['name']
        params = { 'account': '{}'.format(account) }
        resp = sess.get(url='http://mapp.zju.edu.cn/lightapp/lightapp/getCardBalance', params=params).json()
        balance = int(resp['data']['query_accinfo']['accinfo'][0]['balance']) / 100.0
        time = datetime.date.today().strftime("%Y%m%d")
        params = {
            'curpage': '1',
            'pagesize': '10',
            'account': '{}'.format(account),
            'queryStart': time,
            'queryEnd': time
        }
        resp = sess.get(url='http://mapp.zju.edu.cn/lightapp/lightapp/getHistoryConsumption', params=params).json()
        items = resp['data']['query_his_total']['total']
        total_cost = sum([int(item['sign_tranamt']) / 100 for item in items])
        current_time = datetime.datetime.now()
        res['date'] = time
        res['balance'] = balance
        res['query_time'] = current_time.strftime("%Y%m%d%H%M%S")
        res['total_cost'] = total_cost
        res['recent_cost'] = []
        res['name'] = name
        for i in range(len(items)):
            item = items[i]
            occtime = item['occtime']
            time_delta = current_time - datetime.datetime.strptime(occtime, '%Y%m%d%H%M%S')
            if time_delta.seconds <= delta:
                res['recent_cost'].append(item)
            else:
                break
    except Exception:
        pass 
    finally:
        return res