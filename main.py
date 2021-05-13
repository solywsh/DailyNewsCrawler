import json
import time
from pathlib import Path #判断路径文件是否存在
from GetXiaoHeiHe.GetXiaoHeiHe import xiaoheihe
from GetZhihu.GetZhihu import zhihu
from SendMsg.SendMsg import send



def write_config(config,path = r'./config/config.json'):
    with open(path,'w',encoding='utf-8') as file_object:
            file_object.write(json.dumps(config,indent = 4, ensure_ascii=False))
    file_object.close()

#读取配置文件
def read_config(path=r'./config/config.json'):
    my_file = Path(path)
    if my_file.is_file():
        # 指定的文件存在
        with open(path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        f.close()
        return config
    else:
        print('文件不存在...')
        return 0


if __name__ == "__main__":
    while True:
        time_now = time.strftime("%H:%M:%S", time.localtime()) # 刷新
        if time_now == "09:30:10" or time_now == "09:30:11":#不知道是奇数还是偶数
            config = read_config()#读取配置文件
            get_status_zhihu = zhihu(config['zhihu_cookie'],config['get_zhihu_hot'],config['get_zhihu_everyday60s'])
            #抓取小黑盒
            get_status_xiaoheihe = xiaoheihe(config['get_xiaoheihe_most_popular'],config['get_xiaoheihe_discount'])
            #生成网页并且发送
            if get_status_zhihu == 0 and get_status_xiaoheihe == 0:
                send_status = send(config['PushPlus_token'],config['get_zhihu_hot'],config['get_zhihu_everyday60s'],
                                        config['get_xiaoheihe_most_popular'],config['get_xiaoheihe_discount'])

        time.sleep(2) # 停两秒


    

