import requests
import bs4
import json
import pprint
import time
from bs4 import BeautifulSoup

#解析知乎网页
def get_zhihu_html(url):
    headers={
	    'Host':'www.zhihu.com',
	    'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
	    'Connection':'keep-alive',
        'Cookie':'_zap=6fc5b396-f370-431b-a3c5-c3608fb51382; d_c0="AKBaZPGswBKPTgAQZvlfylIAGSPADCD5cYQ=|1614947883"; q_c1=076c9da0cdff4f5e8d22a2e1812e47a4|1615027663000|1615027663000; tshl=; _xsrf=X7gO6aKjQvlRaxFr6ubUFbSg3Fl4py91; tst=h; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1620214630,1620300809,1620302760,1620392803; SESSIONID=0hfzHzCmCRgDmAM9lW8BKWctDyFcnRrylQUExRYYn4t; JOID=VFsXBUr__DXvC2V8ZP_eKvFUpb9yypVXkkQaPg27q1OvYSM0XJ3Co48JYXln5zG7y4r9hYs_7dWjhnfiFxF3_L0=; osd=U1wRAUP4-zPrAmJ7YvvXLfZSobZ1zZNTm0MdOAmyrFSpZSozW5vGqogOZ31u4Da9z4P6go075NKkgHPrEBZx-LQ=; __snaker__id=s1GcabulQVqWg4M2; _9755xjdesxxd_=32; YD00517437729195%3AWM_NI=L%2Fg%2FO%2BaQmBm1hvDKp7lA74%2FRHISZ4Rui%2FKr5PLdPnhapr%2BnooYw9SOCvDxlt%2BxA2VYFstMbcI5J8%2BbC8nuJogtTahONfC%2B5LemmSE3JxugeIXkwstlyz3Ni7TL9gZ6qtdGs%3D; YD00517437729195%3AWM_NIKE=9ca17ae2e6ffcda170e2e6eea7f1458c9d9d8cf45ba1b08fa7c54e838b8f85b664f29fbea8d47dfcb99bb4f52af0fea7c3b92a90f1a9d0ce21a38fa3a3f03bacaa8cacf33db09ff9d5ae5a8c979dbbb75ab7b7e1acf13f9494acb1ed64a3b0becced65ad87b9dad24581aa8c99ef80e9a88fd3d55386adbcaee1698beb86d9aa6a81e8a296c965a5ac9c82eb458eba8dccb848a7b3a3b4c8398aa8bb88e8439cb5b994f768bba6fdafec3d9894f788d93eb3acaca8f237e2a3; YD00517437729195%3AWM_TID=R%2B%2Bd7dkz5NNAFVABRAM7lnArHEg8hATv; gdxidpyhxdE=XMNc1ACAXA5AJ7vq5KLVrSRXczjdjpP%5C4c244%2Fs29BDB2WBxBvw6BMcE8Ut8WjkolOqEXmKng5ItO79y6Hx2DhpUWELJ%2BUNU0dCXuox9JI%2BC00XMTDiC7XkPQS%2F8XPHuyO3C4nzkZCS0rvBydPO%5CmTBcAdm4Xx7iSM9Z6ebZJRJ%2BGlhE%3A1620397842547; captcha_session_v2="2|1:0|10:1620397577|18:captcha_session_v2|88:NUhqTVlIMktqckdUYjl1WXJVeWxITzY2blJxU0R2WldIS1NLWVI3ODFNeEd6WDRVdTE2STNtdE0vdEJ6UVJydQ==|e5715ab046db81a60a4a9b7ddfdaac5d5f102eea1c2ba4ad6cf65558bed17335"; captcha_ticket_v2="2|1:0|10:1620397583|17:captcha_ticket_v2|704:eyJ2YWxpZGF0ZSI6IkNOMzFfRVl5SHhfZ0MycXp3V1pmaHR6bE5Vc3pjeW5zNmpyeUouTnFwc3RwSXgwblc1aVpCcUgtWXoxbU4tYmtYUUg3dS0wTTB2ZU0uYXZDLnFpd0VCRFdPQ2dNWE5FUi54cWZYY1lvdU9wVEZIdzEuXzlOYy10cE1hTGZGdmlmY2Vtc3RHZUxoS3IuNTdMN2VGVU1fMGxydVI1QlA1NGxsNnh4WE9NR09tUmR4RWJDRHlDb29JRG9sR1RWNVNGbk9IcmR3RkZFN3VmejBJckt4OGZ6NjdvTDcuZ0wyamFJS2xpaE5seWlwZVNiLlkwQ0pUcWJKSW1OWTZ1aHpQYzB4V0NidjRCS0Nxa3FBYkViN2JEQUlySHRaN1BDdDRiYWdKdWIyRXVaVGt5OWV2VFpQWS1HVUlSMENNdDhMbVouUWg5NGxWLmlqVFNsZVRubEkya3dkLVFSNGo0bnBNMnFwTWw0WG1VaUZTQkk1WUZTYVZpS01aNDJ0OU8xcEQwaFZxOXNXMlpBLXRPWm1MemM3S3Aya3pkV09nNDZsLWlVUG9DWENSTVRoTWNKYnU0TmE0cld6ZkgyTk5mRC52TjVvSjlDWk4temZNSl9PTUdaREZ5YnhzRDlxRGI5Q0pUZDZ5NUhqVXVKT3Y5TGptVERMdi52Ul9JZHV2QU40ZzJyMyJ9|d1c578ba20eede109ede442be69d2d907e4589d84f3e3849ec48ae5386bac04b"; z_c0="2|1:0|10:1620397597|4:z_c0|92:Mi4xcXBpUUJRQUFBQUFBb0ZwazhhekFFaVlBQUFCZ0FsVk5IWnlDWVFBU1RGUDlHUm9GR3ZtNlVJWDMxY1dlXzI5Ujl3|c656568941a83357a02bbaaa2bb9b6a74b89cbae60aea6112d8e1ba2f317f131"; unlock_ticket="ACDC200iJQwmAAAAYAJVTSVVlWBtHaUQ2i8K0LD8JfFYpVbfiS12rw=="; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1620397597; KLBRSID=cdfcc1d45d024a211bb7144f66bda2cf|1620397599|1620392804',#添加cookie
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
                    break
                i = i + 1
                zhihu_lists.append(zhihu_dict)

        with open(file_path,'w',encoding='utf-8') as file_object:
            file_object.write(json.dumps(zhihu_lists,indent = 4, ensure_ascii=False))
        file_object.close()
        return 0

#处理时间格式，清除带0的数字
def get_sys_date():
    SystemDate_month = time.strftime("%m",time.localtime())
    SystemDate_day = time.strftime("%d",time.localtime())
    if SystemDate_month[0] == '0':
        SystemDate_month = SystemDate_month[1]
    if SystemDate_day[0] == '0':
        SystemDate_day = SystemDate_day[1]
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
        soup = BeautifulSoup(html,"html.parser")
        if len(soup.find_all('button',class_ = 'Button CountingDownButton SignFlow-smsInputButton Button--plain',text='获取短信验证码')) == 1:
            return -1 #在未登录的时候会显示登陆界面，通过查找界面是否有短信登陆按钮来判断是否登陆
        for writings in soup.find_all('div',class_ = 'RichText ztext Post-RichText'):
            for writing in writings.contents:
                print(str(writing))
        # with open(file_path,'w',encoding='utf-8') as file_object:
        #     file_object.write(json.dumps(zhihu_lists,indent = 4, ensure_ascii=False))
        # file_object.close()
        return 0