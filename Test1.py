import requests
import json
import urllib
import time
import execjs
import os
from urllib import parse

Header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    'cookie': 'kg_mid=cb54e58efea812bb4680430db6405448; kg_dfid=3exwR42RaI9i1H9fmB193XTl; kg_dfid_collect=d41d8cd98f00b204e9800998ecf8427e'
}


def get_signature(text):
    with open("kugou.js", "r", encoding='utf-8') as o:
        js_str = o.read()
    if js_str:
        js_obj = execjs.compile(js_str)
        return js_obj.call('faultylabs.MD5', text)


def get_url(keyword):
    search = "https://complexsearch.kugou.com/v2/search/song?callback=callback123&keyword={keyword}&page=1&pagesize=30&bitrate=0&isfuzzy=0&tag=em&inputtype=0&platform=WebFilter&userid=-1&clientver=2000&iscorrection=1&privilege_filter=0&srcappid=2919&clienttime={time}&mid={time}&uuid={time}&dfid=-&signature={signature}"
    key_code = "NVPh5oo715z5DIWAeQlhMDsWXXQV4hwtbitrate=0callback=callback123clienttime={time}clientver=2000dfid=-inputtype=0iscorrection=1isfuzzy=0keyword={keyword}mid={time}page=1pagesize=30platform=WebFilterprivilege_filter=0srcappid=2919tag=emuserid=-1uuid={time}NVPh5oo715z5DIWAeQlhMDsWXXQV4hwt"
    millis = str(round(time.time() * 1000))
    signature = get_signature(key_code.format(time=millis, keyword=keyword))
    search_url = search.format(keyword=keyword, time=millis, signature=signature)
    return search_url


if __name__ == '__main__':
    Name = input("请输入需要搜索的歌曲名:")
    x = 0;y = 0
    path = 'D:/Users/21878/Music/'+ Name + '/'
    print(f'保存路径为:{path}')
    if not os.path.exists(path):
        os.mkdir(path)
    for load in json.loads(requests.get(get_url(Name), headers=Header).text[12:-2])['data']['lists']:
        MusicUrls = f"https://wwwapi.kugou.com/yy/index.php?r=play/getdata&hash={load['FileHash']}&album_audio_id={load['MixSongID']}"
        try:
            MusicUrl = json.loads(requests.get(MusicUrls, headers=Header).text)['data']['play_url']
            MusicName = load['SingerName'] + f'-{Name}' + load['Suffix']
            music = requests.get(MusicUrl, headers=Header)
            with open(f'{path}{MusicName}.mp3', 'wb') as f:
                f.write(music.content)
            x = x + 1
        except Exception:
            print(f"{MusicName}:失败+1{Exception}")
            y = y + 1
            continue
        print('音乐名:', MusicName)
    print(f"共下载成功{x}首歌曲,失败{y}首")
