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
    print("为 {} 发送推送...\n".format(token))
    url = 'http://pushplus.hxtrip.com/send'
    data = {
    "token":token,
    "title":title,
    "content":content,
    "template" : template #模版类型，默认html，此外还有json
    }
    body=json.dumps(data).encode(encoding='utf-8')
    headers = {'Content-Type':'application/json'}
    r = requests.post(url,data=body,headers=headers)
    print(r.text)

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
        print('文件不存在...\n')
        return -1

#写入文件        
def write_html(html,path = r'./temporary/'+get_sys_date(1)+r'.html'):
    with open(path,'w',encoding='utf-8') as file_object:
            file_object.write(json.dumps(html,indent = 4, ensure_ascii=False))
    file_object.close()


#生成html文件
def create_html(zhihu_hot=True,zhihu_everyday60s=True,xiaoheihe_most_popular=True,xiaoheihe_discount = True,
    zhihu_hot_obj = '',zhihu_everyday60s_obj = '',xiaoheihe_most_popular_obj = '',xiaoheihe_discount_obj = ''):

    content_hot = '<h1>知乎热榜</h1>'
    content_everyday60s = '<h1>每天60s读懂世界</h1>'
    content_xiaoheihe_most_popular = '<h1>小黑盒流行游戏</h1>'
    content_xiaoheihe_discount = '<h1>小黑盒打折促销</h1>'

    if zhihu_everyday60s == True :
        print("生成'每天60s读懂世界'文本...\n")
        for obj  in zhihu_everyday60s_obj:
            content_everyday60s = content_everyday60s + "<p>{}</p>".format(obj)
            #content_everyday60s = content_everyday60s+ '<p>' + obj.replace("\"","") + '</p>'
        #print(content_everyday60s)

    if zhihu_hot == True :
        print("生成知乎热门文本...\n")
        count = 1 #计数器，超过一定数之后就停止生成
        for obj in zhihu_hot_obj:
            if count == 11:
                break
            content_hot = content_hot + "<p><a href={}>({}){}.{}</a><p>{}</p></p>".format(obj["url"],
            obj["hot"],obj["Rank"],obj["title"],obj["detailed"])
            count = count + 1
        #print(content_hot)

    if xiaoheihe_most_popular == True:
        print("生成小黑盒流行游戏文本...\n")
        for obj in xiaoheihe_most_popular_obj:
            content_xiaoheihe_most_popular = content_xiaoheihe_most_popular + "<p>{}.{}(评分{}/{})</p>".format(obj["Rank"],
                                                                                            obj["game_name"],obj["game_score"],obj["game_price"])

    if xiaoheihe_discount == True:
        print("生成小黑盒游戏打折促销文本...\n")
        for obj in xiaoheihe_discount_obj:
            content_xiaoheihe_discount = content_xiaoheihe_discount + "<p>{}.{}(评分{}/{})</p>".format(obj["Rank"],
                                                                                            obj["game_name"],obj["game_score"],obj["game_price"])
    
    if zhihu_hot==True or zhihu_everyday60s == True:
        send_html_head = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>每日油报</title></head><body>'
        send_html_body = content_xiaoheihe_most_popular + content_xiaoheihe_discount + content_everyday60s + content_hot
        send_html_foot = '</body></html>'
        send_html = send_html_head + send_html_body + send_html_foot
        write_html(send_html)#写入临时文件
        return send_html


# 发送信息
def send(pushplus_tokens,zhihu_hot=True,zhihu_everyday60s=True,xiaoheihe_most_popular=True,xiaoheihe_discount = True,
    zhihu_file_path_for_hot = r'./res/'+get_sys_date(1)+r'_zhihu_hot.json',
    zhihu_file_path_for_everyday60s= r'./res/'+get_sys_date(1)+r'_zhihu_everyday60s.json',
    file_path_for_xiaoheihe_most_popular = r'./res/'+get_sys_date(1)+r'_xiaoheihe_most_popular.json',
    file_path_for_xiaoheihe_discount = r'./res/'+get_sys_date(1)+r'_xiaoheihe_discount.json'):

    #读取json文件的时候为了防止读取成字符形式
    if zhihu_hot == 'True':
        zhihu_hot = True
    if zhihu_everyday60s == 'True':
        zhihu_everyday60s = True
    if xiaoheihe_most_popular == 'True':
        xiaoheihe_most_popular = True
    if xiaoheihe_discount == 'True':
        xiaoheihe_discount = True

    zhihu_hot_dicts = ""
    zhihu_everyday60s_dicts = ""
    xiaoheihe_most_popular_dicts = ""
    xiaoheihe_discount_dicts = ""

    if zhihu_hot == True :
        zhihu_hot_dicts = read_file(zhihu_file_path_for_hot)
        if zhihu_hot_dicts == -1:
            print("知乎热榜文件不存在\n")
            return -1 #知乎热搜的文件不存在
    if zhihu_everyday60s == True:
        zhihu_everyday60s_dicts = read_file(zhihu_file_path_for_everyday60s)
        if zhihu_everyday60s_dicts == -1:
            print("'每天60s读懂世界'的文件不存在\n")
            return -2#'每天60s读懂世界'的文件不存在
            
    if xiaoheihe_most_popular == True:
        xiaoheihe_most_popular_dicts = read_file(file_path_for_xiaoheihe_most_popular)
        if xiaoheihe_most_popular_dicts == -1:
            print("小黑盒流行游戏的文件不存在\n")
            return -3

    if xiaoheihe_discount == True:
        xiaoheihe_discount_dicts = read_file(file_path_for_xiaoheihe_discount)
        if xiaoheihe_discount_dicts == -1:
            print("小黑盒游戏促销的文件不存在\n")
            return -4

    send_html = create_html(zhihu_hot,zhihu_everyday60s,xiaoheihe_most_popular,xiaoheihe_discount,
        zhihu_hot_dicts,zhihu_everyday60s_dicts,xiaoheihe_most_popular_dicts,xiaoheihe_discount_dicts)

    for pushplus_token in pushplus_tokens:
        pushplus_post("每日油报",send_html,pushplus_token)

    
    

            

