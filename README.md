# DailyNewsCrawler（每日新闻爬虫）

爬取每天的新闻并发送给你，还在施工中...

## 配置文件

在`config/config.json`文件下:

```
{
    "zhihu_cookie": "{你知乎的cookie}",
    "PushPlus_token": ["你pushplus的token1","你pushplus的token2"],
    "get_zhihu_hot": "True", // 知乎的热搜
    "get_zhihu_everyday60s": "True", // 每天60s读懂世界
    "get_xiaoheihe_most_popular": "True", // steam流行游戏
    "get_xiaoheihe_discount": "True" // steam打折促销
}
```

理论上只需要在配置文件选择对应的功能真值以及填入正确的`cookie`和`token`，就可以正常的使用了。

## 抓取知乎的函数

知乎相关的代码已经封装好了，在`GetZhihu`下的`GetZhihu.py`文件里，python导入的时候只需`from GetZhihu.GetZhihu import zhihu`或者`from GetZhihu.GetZhihu import *`(导入里边的所有函数)

`zhihu()函数`需要的参数为：`zhihu(cookie,zhihu_hot=True,zhihu_everyday60s=True,zhihu_file_path_for_hot = r'./res/'+get_sys_date(1)+r'_zhihu_hot.json',zhihu_file_path_for_everyday60s= r'./res/'+get_sys_date(1)+r'_zhihu_everyday60s.json')`

分别是：

```python
cookie,//知乎的cookie
zhihu_hot=True,//是否抓取知乎热搜
zhihu_everyday60s=True,//是否抓取知乎用户'每天60s读懂世界'的文章
zhihu_file_path_for_hot = r'./res/'+get_sys_date(1)+r'_zhihu_hot.json',//知乎热搜抓取结果的存入文件路径
zhihu_file_path_for_everyday60s= r'./res/'+get_sys_date(1)+r'_zhihu_everyday60s.json'//知乎用户'每天60s读懂世界'的文章取结果的存入文件路径
```

- ==除了cookie，其他参数都设置了默认值，所以在使用的时候传入知乎的cookie即可正常使用==

## 抓取小黑盒的steam游戏信息

同理，小黑盒的相关代码也已经封装好了，在`GetXiaoHeiHe`的`GetXiaoHeiHe.py`文件里，`from GetXiaoHeiHe.GetXiaoHeiHe import xiaoheihe`或者`from GetXiaoHeiHe.GetXiaoHeiHe import *`导入。

`xiaoheihe()函数`需要的参数为：`xiaoheihe(xiaoheihe_most_popular = True,xiaoheihe_discount = True,file_path_for_xiaoheihe_most_popular =r'./res/'+get_sys_date(1)+r'_xiaoheihe_most_popular.json',file_path_for_xiaoheihe_discount = r'./res/'+get_sys_date(1)+r'_xiaoheihe_discount.json')`

分别是:

```python
xiaoheihe_most_popular = True,//是否抓取steam当下最流行的游戏
xiaoheihe_discount = True,//是否抓取steam打折促销
file_path_for_xiaoheihe_most_popular=r'./res/'+get_sys_date(1)+r'_xiaoheihe_most_popular.json',//steam当下最流行的游戏抓取结果的存取路径
file_path_for_xiaoheihe_discount = r'./res/'+get_sys_date(1)+r'_xiaoheihe_discount.json'//steam打折促销抓取结果的存取路径
```

- ==因为所有参数都设置默认值，所以单独使用的时候可以不需要传入参数进去==

## 发送信息

> 因为pushplus可以传入html网页，所以发送时候是把结果转换成html的文本然后传入pushplus发送过去。

发送信息函数的路径为`SendMsg\SendMsg.py`，所以导入只需要`from SendMsg.SendMsg import send`即可

`send()函数`的参数为：`send(pushplus_tokens,zhihu_hot=True,zhihu_everyday60s=True,xiaoheihe_most_popular=True,xiaoheihe_discount = True,zhihu_file_path_for_hot = r'./res/'+get_sys_date(1)+r'_zhihu_hot.json',zhihu_file_path_for_everyday60s=r'./res/'+get_sys_date(1)+r'_zhihu_everyday60s.json',file_path_for_xiaoheihe_most_popular = r'./res/'+get_sys_date(1)+r'_xiaoheihe_most_popular.json',file_path_for_xiaoheihe_discount = r'./res/'+get_sys_date(1)+r'_xiaoheihe_discount.json')`

分别为：

```python
pushplus_tokens,//pushplus的token
zhihu_hot=True,
zhihu_everyday60s=True,
xiaoheihe_most_popular=True,
xiaoheihe_discount = True,
zhihu_file_path_for_hot = r'./res/'+get_sys_date(1)+r'_zhihu_hot.json',
zhihu_file_path_for_everyday60s= r'./res/'+get_sys_date(1)+r'_zhihu_everyday60s.json',
file_path_for_xiaoheihe_most_popular = r'./res/'+get_sys_date(1)+r'_xiaoheihe_most_popular.json',
file_path_for_xiaoheihe_discount = r'./res/'+get_sys_date(1)+r'_xiaoheihe_discount.json'
```

- ==除了pushplus_tokens没有设置默认值，其余都设置了默认值，所以如果前面两个抓取函数的存取路径没变的话，其他参数不用更改，需要注意的是，pushplus_tokens是一个列表，可以给多人发送信息。==

