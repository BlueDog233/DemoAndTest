import os
import requests
from lxml import etree

from goods_interface.storedata import store, get

headers = {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "sec-ch-ua": "\"Microsoft Edge\";v=\"123\", \"Not:A-Brand\";v=\"8\", \"Chromium\";v=\"123\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-requested-with": "XMLHttpRequest",
    'Origin':
        'https://www.daichong.vip',
    'Referer':
        'https://www.daichong.vip/?mod=buy&tid=56',

}
try:
    headers['Cookie'] = get('daichong_vip_cookie')
except Exception as e:
    cookie = requests.post('https://www.daichong.vip/user/ajax.php?act=login',
                           data={'user': get('daichong_vip_user'), 'pass': get('daichong_vip_pass')},
                           headers={'Referer': 'https://www.daichong.vip/',
                                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'})
    store('daichong_vip_cookie', cookie.headers['Set-Cookie'].replace('path=/,', ''))
    headers['Cookie'] = get('daichong_vip_cookie')

for tid in range(59,4001):  # Loop from 0 to 4000:
    response = requests.get(f"https://www.daichong.vip/?mod=buy&tid={tid}",headers=headers,verify=False)

    # It's good practice to check if request was successful
    if response.status_code == 200:
        parser = etree.HTMLParser()
        tree = etree.fromstring(response.content, parser)
        result = tree.xpath('//html/body/div[1]/div[2]/div[1]/img')

        if result:
            with open(f'./tem/{tid}.html', 'w', encoding='utf-8') as f:
                f.write(response.text)

        else:
            continue
    else:
        print(f"Request for tid={tid} failed with status code {response.status_code}.")