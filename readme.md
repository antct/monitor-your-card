# Monitor-Your-Card

## Pre

> 申请钉钉机器人，参考https://ding-doc.dingtalk.com/doc#/serverapi2/qf2nxq。安全设置为加签方式，记该密钥为secret。申请得到的Webhook地址里提取access_token字段，记为token。

## Run

> Fork该项目。选择Setting→Secret→New repository secret。分别创建以下字段。

```
ECARD_USERNAME=你的校园卡账号
ECARD_PASSWORD=你的校园卡密码
DINGDING_TOKEN=申请的钉钉机器人access_token
DINGDING_SECRET=申请的钉钉机器人secret
```

> 选择Action→Set up a workflow yourself。以下提供一个Action Example。

```yml
name: Monitor Your Card

on:
  schedule:
    # run every 10 minutes
    - cron:  '*/10 * * * *'

jobs:
  monitor-your-card:
    name: monitor your card
    runs-on: ubuntu-latest
    steps:
      - name: checkout actions
      - uses: actions/checkout@v1

      - name: Set up Python 3.7
      - uses: actions/setup-python@v1
        with:
          python-version: 3.7

      - uses: your_github_username/@master
        env:
          ECARD_USERNAME: ${{ secrets.ECARD_USERNAME }}
          ECARD_PASSWORD: ${{ secrets.ECARD_PASSWORD }}
          DINGDING_USERNAME: ${{ secrets.DINGDING_USERNAME }}
          DINGDING_PASSWORD: ${{ secrets.DINGDING_PASSWORD }}
        if: ${{ github.event_name == 'push' }}
        run: |
        pip install -r requirements
        python main.py hello
        run: |
        pip install -r requirements
        python main.py
```

