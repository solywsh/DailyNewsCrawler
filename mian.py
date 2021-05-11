import json
from pathlib import Path #判断路径文件是否存在
from GetZhihu.GetZhihu import zhihu

#zhihu_file_path_for_hot = r'./res/zhihu_hot.json'
#zhihu_file_path_for_everyday60s= r'./res/zhihu_everyday60s.json'

def write_config(config,path = r'./config/config.json'):
    with open(path,'w',encoding='utf-8') as file_object:
            file_object.write(json.dumps(config,indent = 4, ensure_ascii=False))
    file_object.close()

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
    config = read_config()
    zhihu(config['zhihu_cookie'])