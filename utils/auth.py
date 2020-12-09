import re
import requests

class zju_auth():
    @staticmethod
    def _rsa_encrypt(password_str: str, e_str: str, M_str: str):
        password_bytes = bytes(password_str, 'ascii')
        password_int = int.from_bytes(password_bytes, 'big')
        e_int = int(e_str, 16)
        M_int = int(M_str, 16)
        result_int = pow(password_int, e_int, M_int)
        return hex(result_int)[2:].rjust(128, '0')

    @staticmethod
    def login(username: str, password: str):
        _headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Access-Control-Allow-Origin': '*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
        }
        _session = requests.Session()

        resp = _session.get(url='https://zjuam.zju.edu.cn/cas/login')
        execution = re.search('name="execution" value="(.*?)"', resp.text).group(1)
        resp = _session.get(url='https://zjuam.zju.edu.cn/cas/v2/getPubKey').json()
        n, e = resp['modulus'], resp['exponent']
        encrypt_password = zju_auth._rsa_encrypt(password, e, n)
        data = {
            'username': username,
            'password': encrypt_password,
            'execution': execution,
            '_eventId': 'submit'
        }
        resp = _session.post(url='https://zjuam.zju.edu.cn/cas/login', data=data)
        msg = None
        if not re.search('class="login-page"', resp.text):
            if re.search('id="time-box"', resp.text):
                msg = 'account lock'
            else:
                msg = 'login ok'
        else:
            msg = 'wrong password'
        return _session, msg