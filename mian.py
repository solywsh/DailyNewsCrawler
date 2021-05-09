from getZhihu.getZhihu import *
import pprint #漂亮打印 pprint.pprint(zhihu_everyday60s_html)

zhihu_file_path_for_hot = r'./res/zhihu_hot.json'
zhihu_file_path_for_everyday60s = r'./res/zhihu_everyday60s.json'

    
def zhihu(zhihu_hot,zhihu_everyday60s):
    #知乎热搜
    if zhihu_hot == True:
        url_zhihu_hot = "https://www.zhihu.com/hot"
        zhihu_hot_html = get_zhihu_html(url_zhihu_hot)
        zhihu_status_code = get_zhihu_hot_dict(zhihu_file_path_for_hot,zhihu_hot_html)
        if zhihu_status_code == 0:
            print("知乎热搜抓取成功...")
        elif zhihu_status_code == 404:
            print("网页链接失败...请检查网络")
        elif zhihu_status_code == -1:
            print("cookie失效,请重新更换cookie...")

    #每天60s读懂世界
    if zhihu_everyday60s == True:
        #'每天60s读懂世界'的个人界面
        url_zhihu_everyday60s = "https://www.zhihu.com/people/mt36501"
        #访问'每天60s读懂世界'个人界面，找到今天的文章链接
        zhihu_everyday60s_list_html = get_zhihu_html(url_zhihu_everyday60s)
        zhihu_everyday60s_today_url = get_zhihu_everyday60s_url(zhihu_everyday60s_list_html)
        #得到今天文章的url之后开始网页
        if zhihu_everyday60s_today_url != 404:
            zhihu_everyday60s_content_html = get_zhihu_writings_html(zhihu_everyday60s_today_url)
            zhihu_status_code = get_zhihu_everyday60s_content(zhihu_file_path_for_everyday60s,zhihu_everyday60s_content_html)

        

def main():
    zhihu_hot = False #用于控制是否抓取
    zhihu_everyday60s = True #用于控制是否抓取
    zhihu(zhihu_hot,zhihu_everyday60s)




if __name__ == "__main__":
    main()