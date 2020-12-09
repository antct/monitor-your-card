# Monitor-Your-Card

## Pre

> 申请钉钉机器人，参考[钉钉自定义机器人文档](https://ding-doc.dingtalk.com/doc#/serverapi2/qf2nxq)。

> 机器人安全设置为加签方式，提取该密钥secret。

> 申请得到的Webhook地址中提取access_token字段。

## Run

> Fork该项目。选择Setting→Secret→New repository secret，创建以下字段。

```
ECARD_USERNAME=你的校园卡账号
ECARD_PASSWORD=你的校园卡密码
DINGDING_TOKEN=申请的钉钉机器人access_token
DINGDING_SECRET=申请的钉钉机器人secret
```

> 选择Action→Set up a workflow yourself，新建一个Workflow，以下为Action YML示例。

```yml
name: monitor your card
 
on:
  push:
    branches: [ master ]
  schedule:
    - cron:  '0 0 * * *'

jobs:
  monitor:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v2
      
      - uses: actions/setup-python@v2
        with:
          python-version: 3.7

      - name: monitor-hello
        if: ${{ github.event_name == 'push' }}
        env:
          ECARD_USERNAME: ${{ secrets.ECARD_USERNAME }}
          ECARD_PASSWORD: ${{ secrets.ECARD_PASSWORD }}
          DINGDING_TOKEN: ${{ secrets.DINGDING_TOKEN }}
          DINGDING_SECRET: ${{ secrets.DINGDING_SECRET }}
        run: |
          pip install -r requirements.txt
          python main.py hello
        
      - name: monitor-run
        if: ${{ github.event_name == 'schedule' }}
        env:
          ECARD_USERNAME: ${{ secrets.ECARD_USERNAME }}
          ECARD_PASSWORD: ${{ secrets.ECARD_PASSWORD }}
          DINGDING_TOKEN: ${{ secrets.DINGDING_TOKEN }}
          DINGDING_SECRET: ${{ secrets.DINGDING_SECRET }}
        run: |
          pip install -r requirements.txt
          python main.py run
```

> Push trigger触发hello函数，配置成功后钉钉会收到配置成功消息和昨日消费信息。

> Schedule trigger触发run函数，每天早上8点推送昨日消费信息。

## Tree

```
.
├── main.py           # 程序主入口
├── monitor           # 监控端
│   └── api.py        # 监控api，目前实现校园卡
├── notice            # 通知端
│   └── api.py        # 通知api，目前支持钉钉&微信
└── utils             # 工具类
    └── auth.py       # 登录接口
```
