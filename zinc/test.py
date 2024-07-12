import requests
import random
import time

# 构造请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}


# 获取代理IP
def get_proxies():
    # 这里使用免费代理网站进行获取，实际使用中需要替换成其他方式获取
    url = "https://www.zdaye.com/"
    response = requests.get(url).json()
    return [f"{i['protocol']}://{i['ip']}:{i['port']}" for i in response['data']['data_list']]


# 构造代理池
proxies_pool = get_proxies()


# 爬虫主体程序
def get_user_info(user_url):
    # 从代理池中随机选择一个代理IP
    proxies = random.choice(proxies_pool)
    try:
        response = requests.get(user_url, headers=headers, proxies={'http': proxies, 'https': proxies})
        if response.status_code == 200:
            print(response.text)
    except:
        print(f"{proxies}请求失败")


if __name__ == '__main__':
    user_list = ['https://www.zhihu.com/people/xie-ke-bai-11-86-24-2/followers',
                 'https://www.zhihu.com/people/gong-xin-10-61-53-51/followers',
                 'https://www.zhihu.com/people/y-xin-xin/followers']
    for user_url in user_list:
        get_user_info(user_url)
        time.sleep(5)