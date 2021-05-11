import json
import requests
import time
from pathlib import Path #判断路径文件是否存在

#处理时间格式
def get_sys_date(type = 0):
    if type == 0:
        SystemDate_month = time.strftime("%m",time.localtime())
        SystemDate_day = time.strftime("%d",time.localtime())
        if SystemDate_month[0] == '0':
            SystemDate_month = SystemDate_month[1]
        if SystemDate_day[0] == '0':
            SystemDate_day = SystemDate_day[1]
        return SystemDate_month+SystemDate_day
    else:
        SystemDate_month = time.strftime("%m",time.localtime())
        SystemDate_day = time.strftime("%d",time.localtime())
        return SystemDate_month+SystemDate_day


#PushPlus的推送
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


#读取文件
def read_file(path):
    my_file = Path(path)
    if my_file.is_file():
        # 指定的文件存在
        with open(path, 'r', encoding='utf-8') as f:
            obj = json.load(f)
        f.close()
        return obj
    else:
        print('文件不存在...')
        return -1
        
#生成html文件
def create_html(zhihu_hot=True,zhihu_everyday60s=True,
    zhihu_hot_obj = '',zhihu_everyday60s_obj = ''):

    content_hot = '<h1>知乎热榜</h1>'
    content_everyday60s = '<h1>每天60s读懂世界</h1>'

    if zhihu_hot == True:
        print("生成知乎热门文本...\n")
        for obj in zhihu_hot_obj:
            content_hot = content_hot + "<p><a href={}>({}){}.{}</a><p>{}</p></p>".format(obj["url"],
            obj["hot"],obj["Rank "],obj["title"],obj["detailed "])
        #print(content_hot)

    if zhihu_everyday60s == True:
        print("生成'每天60s读懂世界'文本...\n")
        for obj  in zhihu_everyday60s_obj:
            content_everyday60s = content_everyday60s + "<p>{}</p>".format(obj)
            #content_everyday60s = content_everyday60s+ '<p>' + obj.replace("\"","") + '</p>'
        #print(content_everyday60s)
    

    if zhihu_hot==True or zhihu_everyday60s == True:
        send_html_head = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Title</title></head><body>'
        send_html_body = content_everyday60s + content_hot 
        send_html_foot = '</body></html>'
        send_html = send_html_head + send_html_body + send_html_foot
        return send_html


# 发送信息
def send(pushplus_tokens,zhihu_hot=True,zhihu_everyday60s=True,
    zhihu_file_path_for_hot = r'./res/'+get_sys_date(1)+r'_zhihu_hot.json',
    zhihu_file_path_for_everyday60s= r'./res/'+get_sys_date(1)+r'_zhihu_everyday60s.json'):
    if zhihu_hot == True:
        zhihu_hot_dicts = read_file(zhihu_file_path_for_hot)
        if zhihu_hot_dicts == -1:
            print("知乎热榜文件不存在")
            return -1 #知乎热搜的文件不存在
    if zhihu_everyday60s == True:
        zhihu_everyday60s_dicts = read_file(zhihu_file_path_for_everyday60s)
        if zhihu_everyday60s_dicts == -1:
            print("'每天60s读懂世界'的文件不存在")
            return -2#'每天60s读懂世界'的文件不存在

    send_html = create_html(zhihu_hot,zhihu_everyday60s,zhihu_hot_dicts ,zhihu_everyday60s_dicts)

    for pushplus_token in pushplus_tokens:
        pushplus_post("每日油报",send_html,pushplus_token)

    
    

            

