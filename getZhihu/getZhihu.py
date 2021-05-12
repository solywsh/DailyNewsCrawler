import requests
import bs4
import json
import pprint
import time
from bs4 import BeautifulSoup
from requests.api import get

#解析知乎网页
def get_zhihu_html(url,cookie):
    headers={
	    'Host':'www.zhihu.com',
	    'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
	    'Connection':'keep-alive',
        'Cookie':cookie,
	    'Cache-Control':'no-cache',
	    'Upgrade-Insecure-Requests':'1',
	    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	    'User-Agent':'Mozilla/5.0 (Macintosh; Inter Mac OS X 10_12_4) '
				    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    }
    
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status() #如果不是返回状态码200，则产生异常
        r.encoding = 'utf-8'
        return r.text
    except:
        #返回-1，表示get失败，此时即使cookie失效也会生成网页只是会叫你登陆，所以需要在下面的函数解析网页
        return 404

#解析知乎网页
def get_zhihu_writings_html(url):
    headers={ 
	    'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
	    'Cache-Control':'max-age=0',
	    'Upgrade-Insecure-Requests':'1',
	    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	    'User-Agent':'Mozilla/5.0 (Macintosh; Inter Mac OS X 10_12_4) '
				    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    }
    
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status() #如果不是返回状态码200，则产生异常
        r.encoding = 'utf-8'
        return r.text
    except:
        #返回-1，表示get失败，此时即使cookie失效也会生成网页只是会叫你登陆，所以需要在下面的函数解析网页
        return 404

#抓取知乎热搜的字典
def get_zhihu_hot_dict(file_path,html):
    if html == 404:
        return 404 #状态码不是200的情况
    else:
        soup = BeautifulSoup(html,"html.parser")
        if len(soup.find_all('button',class_ = 'Button CountingDownButton SignFlow-smsInputButton Button--plain',text='获取短信验证码')) == 1:
            return -1 #在未登录的时候会显示登陆界面，通过查找界面是否有短信登陆按钮来判断是否登陆
        zhihu_lists = []
        i = 1
        for HotItem_content in soup.find_all('div',class_ = 'HotItem-content'):
            for HotItem in HotItem_content.find_all('a',target = "_blank"):
                #有时候题主并没有写简介，所以需要一个判断，如果没有就默认简介为标题
                if len(HotItem.contents) > 1:
                    detailed = HotItem.contents[1].string
                else: 
                    detailed = HotItem.contents[0].string
                
                #此处for是为了寻找“热度”这个关键字
                for HI in HotItem_content.find_all('div',class_ = "HotItem-metrics HotItem-metrics--bottom"):
                    zhihu_dict = {
                    'Rank ' : i,
                    'hot' : HI.contents[1].string,
                    'title' : HotItem['title'],
                    'url' : HotItem['href'],
                    'detailed ' : detailed
                    }
                    pprint.pprint(zhihu_dict)
                    print('\n')
                    time.sleep(1)
                    break
                i = i + 1
                zhihu_lists.append(zhihu_dict)

        with open(file_path,'w',encoding='utf-8') as file_object:
            file_object.write(json.dumps(zhihu_lists,indent = 4, ensure_ascii=False))
        file_object.close()
        return 0

#处理时间格式，清除带0的数字
#默认type为0，也就是用与比对抓取的标题的，此时个位数字不带0
#当type不为0时，返回个位数字带0的数字，用于生成标题
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

#处理标题时间格式
def format_title_date(title):
    date = title.split('，',1)[0]#获取标题日期，如"5月10日"
    date_num = len(date)
    if date_num == 4:
        return date[0] + date[2]
    if date_num == 6:
        return date[0:2] + date[3:6]
    if date_num == 5:
        if title[1] == '月':
            return date[0] + date[2:4]
        else:
            return date[0:2] + date[3]

#得到'每天60s读懂世界'今天文章的url
def get_zhihu_everyday60s_url(html):
    if html == 404:
        return 404 #状态码不是200的情况
    else:
        SystemDate_today = get_sys_date()
        soup = BeautifulSoup(html,"html.parser")
        if len(soup.find_all('button',class_ = 'Button CountingDownButton SignFlow-smsInputButton Button--plain',text='获取短信验证码')) == 1:
            return -1 #在未登录的时候会显示登陆界面，通过查找界面是否有短信登陆按钮来判断是否登陆
        for ListShortcut in soup.find_all('div',class_ = 'List ProfileActivities'):
            title = ListShortcut.contents[1].contents[0].contents[1].contents[2]['content']
            title_date = format_title_date(title)#处理标题时间格式
            if SystemDate_today ==  title_date:
                url = 'https:'+ListShortcut.contents[1].contents[0].contents[1].contents[3]['content']
                return url


#抓取'每天60s读懂世界'的字典
def  get_zhihu_everyday60s_content(file_path,html):
    if html == 404:
        return 404 #状态码不是200的情况
    else:
        zhihu_lists = []
        soup = BeautifulSoup(html,"html.parser")
        if len(soup.find_all('button',class_ = 'Button CountingDownButton SignFlow-smsInputButton Button--plain',text='获取短信验证码')) == 1:
            return -1 #在未登录的时候会显示登陆界面，通过查找界面是否有短信登陆按钮来判断是否登陆
        for writings in soup.find_all('div',class_ = 'RichText ztext Post-RichText'):
            for writing in writings.contents:
                if len(writing)== 1:
                    print(writing.string+'\n')
                    zhihu_lists.append(writing.string)
                    time.sleep(1)
        with open(file_path,'w',encoding='utf-8') as file_object:
            file_object.write(json.dumps(zhihu_lists,indent = 4, ensure_ascii=False))
        file_object.close()
        return 0


############################
####知乎抓取总的控制函数####
###########################
#5个参数分别是：
#1.知乎账号的cookie
#2.是否抓取知乎热搜（True/False）,默认True
#3.是否抓取'每天60s读懂世界'（True/False）,默认True
#4.知乎热搜抓取结果存取路径，默认路径：'./res/zhihu_hot.json'
#5.'每天60s读懂世界'抓取结果存取路径，默认路径：./res/zhihu_everyday60s.json
def zhihu(cookie,zhihu_hot=True,zhihu_everyday60s=True,
    zhihu_file_path_for_hot = r'./res/'+get_sys_date(1)+r'_zhihu_hot.json',
    zhihu_file_path_for_everyday60s= r'./res/'+get_sys_date(1)+r'_zhihu_everyday60s.json'):
    #知乎热搜
    if zhihu_hot == True or zhihu_hot == 'True':
        print("开始抓取知乎热搜...\n")
        url_zhihu_hot = "https://www.zhihu.com/hot"
        zhihu_hot_html = get_zhihu_html(url_zhihu_hot,cookie)
        zhihu_status_code = get_zhihu_hot_dict(zhihu_file_path_for_hot,zhihu_hot_html)
        
        if zhihu_status_code == 0:
            print("知乎热搜抓取成功...\n")
        elif zhihu_status_code == 404:
            print("知乎热搜抓取失败,网页链接失败...请检查网络\n")
            return zhihu_status_code
        elif zhihu_status_code == -1:
            print("知乎热搜抓取失败,cookie失效,请重新更换cookie...\n")
            return zhihu_status_code

    #每天60s读懂世界
    if zhihu_everyday60s == True or zhihu_everyday60s == 'True' :
        print("开始抓取'每天60s读懂世界'...\n")
        #'每天60s读懂世界'的个人界面
        url_zhihu_everyday60s = "https://www.zhihu.com/people/mt36501"
        #访问'每天60s读懂世界'个人界面，找到今天的文章链接
        zhihu_everyday60s_list_html = get_zhihu_writings_html(url_zhihu_everyday60s)
        zhihu_everyday60s_today_url = get_zhihu_everyday60s_url(zhihu_everyday60s_list_html)
        
        #得到今天文章的url之后开始网页
        zhihu_everyday60s_content_html = get_zhihu_writings_html(zhihu_everyday60s_today_url)
        zhihu_status_code = get_zhihu_everyday60s_content(zhihu_file_path_for_everyday60s,zhihu_everyday60s_content_html)
        
        if zhihu_status_code == 0:
            print("'每天60s读懂世界'抓取成功...\n")
        elif zhihu_status_code == 404:
            print("'每天60s读懂世界'抓取失败,网页链接失败...请检查网络\n")
            return zhihu_status_code
        elif zhihu_status_code == -1:
            print("'每天60s读懂世界'抓取失败,cookie失效,请重新更换cookie...\n")
            return zhihu_status_code

    return 0