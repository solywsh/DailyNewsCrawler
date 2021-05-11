import json
import requests
from pathlib import Path #判断路径文件是否存在
PushPlus_token = "a6265a189e994e74bf6ab24587bb8891"

def pushplus_post(title,content,token,template="html"):
    url = 'http://pushplus.hxtrip.com/send'
    data = {
    "token":token,
    "title":title,
    "content":content,
    "template" : template #模版类型，默认html，此外还有json
    }
    body=json.dumps(data).encode(encoding='utf-8')
    headers = {'Content-Type':'application/json'}
    requests.post(url,data=body,headers=headers)


def read_html(path):
    my_file = Path(path)
    if my_file.is_file():
        # 指定的文件存在
        with open(path, 'r', encoding='utf-8') as f:
            obj = f.read()
        f.close()
        return obj
    else:
        print('文件不存在...')
        return -1

if __name__ == "__main__":
    path = r'F:\GithubWarehouse\study\python\每日热点\test\test.html'
    html_file = read_html(path)
    if html_file != -1:
        pushplus_post('测试',str(html_file),PushPlus_token)