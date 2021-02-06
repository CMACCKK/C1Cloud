from flask import Flask, request
import requests
import datetime
import logging
from src.config import *

app = Flask(__name__)


def push_ftqq(content):
    resp = requests.post("https://sc.ftqq.com/{SOCKEY}.send".format(SOCKEY=ServerJ_Sockey),data={"text": "xray漏洞报告", "desp": content})
    if resp.json()["errno"] != 0:
        raise ValueError("push ftqq failed, %s" % resp.text)
    else:
        print('push content success')

@app.route('/webhook', methods=['POST'])
def xray_webhook():
    vuln = request.json
    # 因为还会收到 https://chaitin.github.io/xray/#/api/statistic 的数据
    if vuln["type"] == "web_statistic":
        return "ok"
    content = """## xray 发现了新漏洞

url: {url}

发现时间: {create_time}

插件: {plugin}

漏洞类型: {vuln_class}

payload: {Payload}
""".format(url=vuln["data"]["target"]["url"], plugin=vuln["data"]["plugin"],
           vuln_class=vuln["type"] or "Default",
           create_time=str(datetime.datetime.fromtimestamp(vuln["data"]["create_time"] / 1000)),
           Payload=vuln["data"]["detail"]["payload"])
    try:
        push_ftqq(content)
    except Exception as e:
        logging.exception(e)
    return 'ok'


if __name__ == '__main__':
    app.run()
