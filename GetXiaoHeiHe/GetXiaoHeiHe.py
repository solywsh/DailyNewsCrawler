import time
from bs4.builder import HTML
import requests
#import pprint
import json
from bs4 import BeautifulSoup

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

def get_xiaoheihe_html(url):
    headers={
	    'Host':'www.xiaoheihe.cn',
	    'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
	    'Connection':'keep-alive',
	    'Upgrade-Insecure-Requests':'1',
	    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.56'
    }
    
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status() #如果不是返回状态码200，则产生异常
        r.encoding = 'utf-8'
        return r.text
    except:
        #返回-1，表示get失败，此时即使cookie失效也会生成网页只是会叫你登陆，所以需要在下面的函数解析网页
        return 404


def get_zhihu_hot_dict(html,xiaoheihe_most_popular = True,xiaoheihe_discount = True,
                file_path_for_xiaoheihe_most_popular = r'./res/'+get_sys_date(1)+r'_xiaoheihe_most_popular.json',
                file_path_for_xiaoheihe_discount = r'./res/'+get_sys_date(1)+r'_xiaoheihe_discount.json',
                ):
    
    if html == 404:
        return 404 #状态码不是200的情况
    else:
        soup = BeautifulSoup(html,"html.parser")
        for content in soup.find_all('div',class_ = 'game-index-wrapper'):
            most_popular_list = []
            discount_list = []
            #len(content.contents[0].contents)的长度为6
            #从0-5依次为最受欢迎游戏，最新上架，销量，价格降序，价格升序，steam促销
            #更改content.contents[0].contents[0].find_all('div',class_ = "mask") 的最后一个content值可以选择最后抓取对应的模块

            #steam最受欢迎
            if xiaoheihe_most_popular == True:
                count = 1
                print("抓取steam最受欢迎...\n")
                for items in content.contents[0].contents[0].find_all('div',class_ = "mask"):
                    for item in items.contents[0].contents:
                        if len(str(item)) < 10: #排除标题
                            continue
                        game_name = str(item.contents[0].contents[1].contents[0].string)
                        game_score = str(item.contents[0].contents[1].contents[1].contents[1].string)
                        game_price = str(item.contents[0].contents[1].contents[2].contents[0].contents[1].string + 
                            item.contents[0].contents[1].contents[2].contents[0].contents[2].string)
                        most_popular_item_dict = {
                            "Rank" : count,
                            "game_name" : game_name,
                            "game_score" : game_score,
                            "game_price" : game_price
                        }
                        print("{}\n".format(most_popular_item_dict))
                        most_popular_list.append(most_popular_item_dict)
                        count = count + 1
                        time.sleep(1)
                print("写入小黑盒流行游戏...\n")
                with open(file_path_for_xiaoheihe_most_popular,'w',encoding='utf-8') as file_object:
                    file_object.write(json.dumps(most_popular_list,indent = 4, ensure_ascii=False))
                file_object.close()



            #steam打折促销
            if xiaoheihe_discount == True:
                print("抓取steam促销...\n")
                count = 1
                for items in content.contents[0].contents[5].find_all('div',class_ = "mask"):
                    for item in items.contents[0].contents:
                        if len(str(item)) < 10: #排除标题
                            continue
                        game_name = str(item.contents[0].contents[1].contents[0].string)
                        game_score = str(item.contents[0].contents[1].contents[1].contents[1].string)
                        game_price = str(item.contents[0].contents[1].contents[2].contents[0].contents[1].string + 
                            item.contents[0].contents[1].contents[2].contents[0].contents[2].string)
                        most_popular_item_dict = {
                            "Rank" : count,
                            "game_name" : game_name,
                            "game_score" : game_score,
                            "game_price" : game_price
                        }
                        print("{}\n".format(most_popular_item_dict))
                        discount_list.append(most_popular_item_dict)
                        count = count + 1
                        time.sleep(1)

                print("写入打折促销...\n")
                with open(file_path_for_xiaoheihe_discount,'w',encoding='utf-8') as file_object:
                    file_object.write(json.dumps(discount_list,indent = 4, ensure_ascii=False))
                file_object.close()

        return 0
        





##############################
####小黑盒抓取总的控制函数####
#############################
#3个参数分别是：
#1.是否抓取steam最流行游戏（True/False）,默认True
#2.是否抓取steam促销（True/False）,默认True
#3.知乎热搜抓取结果存取路径，默认路径：'./res/日期_xiaoheihe.json'
def xiaoheihe(xiaoheihe_most_popular = True,xiaoheihe_discount = True,
    file_path_for_xiaoheihe_most_popular = r'./res/'+get_sys_date(1)+r'_xiaoheihe_most_popular.json',
    file_path_for_xiaoheihe_discount = r'./res/'+get_sys_date(1)+r'_xiaoheihe_discount.json'):

    #格式化真值
    if xiaoheihe_most_popular == 'True':
        xiaoheihe_most_popular = True
    if xiaoheihe_discount == 'True':
        xiaoheihe_discount = True

    
    url = "https://www.xiaoheihe.cn/games/index"
    path = r'./res/xiaoheihe_test.json'
    xiaoheihe_html = get_xiaoheihe_html(url)
    xiaoheihe_status_code = get_zhihu_hot_dict(xiaoheihe_html,xiaoheihe_most_popular,xiaoheihe_discount,
                                file_path_for_xiaoheihe_most_popular,file_path_for_xiaoheihe_discount)

    if xiaoheihe_status_code == 404:
        print("小黑盒网页链接失败,请检查网络...\n")
    if xiaoheihe_status_code == 0:
        print("小黑盒抓取成功...\n")

    return 0
    
