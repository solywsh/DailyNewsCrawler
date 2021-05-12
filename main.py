import json
import time
from pathlib import Path #判断路径文件是否存在
from GetZhihu.GetZhihu import zhihu
from SendMsg.SendMsg import send

#zhihu_file_path_for_hot = r'./res/zhihu_hot.json'
#zhihu_file_path_for_everyday60s= r'./res/zhihu_everyday60s.json'

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
    config = read_config()#读取配置文件
    #抓取知乎，config['get_zhihu_hot'],config['get_zhihu_everyday60s']两项默认为True,在为True的时候可以省略
    #zhihu(config['zhihu_cookie'],config['get_zhihu_hot'],config['get_zhihu_everyday60s'])
    # get_status = zhihu(config['zhihu_cookie'])
    # if get_status == 0:
    #     send_status = send(config['PushPlus_token'],config['get_zhihu_hot'],config['get_zhihu_everyday60s'])
    send_status = send(config['PushPlus_token'],config['get_zhihu_hot'],config['get_zhihu_everyday60s'])
    
    
    # while True:
    #     time_now = time.strftime("%H:%M:%S", time.localtime()) # 刷新
    #     if time_now == "09:30:10" or time_now == "09:30:11":#不知道是奇数还是偶数
    #         config = read_config()#读取配置文件
    #         #抓取知乎，config['get_zhihu_hot'],config['get_zhihu_everyday60s']两项默认为True,在为True的时候可以省略
    #         #zhihu(config['zhihu_cookie'],config['get_zhihu_hot'],config['get_zhihu_everyday60s'])
    #         get_status = zhihu(config['zhihu_cookie'])
    #         if get_status == 0:
    #             send_status = send(config['PushPlus_token'],config['get_zhihu_hot'],config['get_zhihu_everyday60s'])

    #     time.sleep(2) # 停两秒


    

