# DailyNewsCrawler
爬取每天的新闻并发送给你，还在施工中...

## 配置文件

在`config/config.json`文件下:

写入对应的内容：

```json
{
    "zhihu_cookie": "{你知乎的cookie}",
    "PushPlus_token": ["你pushplus的token1","你pushplus的token2"],
    "get_zhihu_hot": "True",//知乎的热搜
    "get_zhihu_everyday60s": "True",//每天60s读懂世界
    "get_xiaoheihe_most_popular": "True",//steam流行游戏
    "get_xiaoheihe_discount": "True"//steam打折促销
}
```

