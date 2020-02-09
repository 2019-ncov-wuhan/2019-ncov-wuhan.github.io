import requests
import json

def requests_web_data(url):
    try:
        headers = {"User-Agent": "", "Cookie": ""}
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
    except:
        print('requests error!')
    else:
        return r.content
def get_weibo_historical_data():
    latest_time_id_url = 'https://www.eecso.com/test/weibo/apis/getlatest.php'
    latest_time_id = json.loads(requests_web_data(latest_time_id_url).decode('utf-8'))[0]  
    # 筛选获取time_id
    time_ids = []
    for x in range(39258, int(latest_time_id) + 1, 180):    # time_id=48438：2020-01-01（取间隔6小时的时间点）
        time_id_url = 'https://www.eecso.com/test/weibo/apis/getlatest.php?timeid=' + str(x)
        time_data = json.loads(requests_web_data(time_id_url).decode('utf-8'))
        if time_data is not None:
            time = time_data[1].split(' ')[1].split(':')[0]
            if time == '00' or time == '12':  ## 使用0点和12点两个时间点的time_id
                time_ids.append(time_data[0])
    if time_ids[-1] != latest_time_id:
        time_ids.append(latest_time_id)
    # 通过筛选的time_id获取一月份的热搜数据
    weibo_hot_data = []
    for time_id in time_ids:
        historical_data_url = 'https://www.eecso.com/test/weibo/apis/currentitems.php?timeid=' + str(time_id)
        data = json.loads(requests_web_data(historical_data_url).decode('utf-8'))
        for i in data:
            weibo_hot_data.append(i)
    return weibo_hot_data
