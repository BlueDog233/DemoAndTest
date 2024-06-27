import requests
import execjs

from goods_interface.storedata import get, store

def buy(tid:int,inputvalue:str,num:int=1)->str:
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

    response = requests.get('https://www.daichong.vip/?mod=buy&tid=56', headers=headers, verify=False)

    str = response.content.__str__()
    import re
    # 正则匹配hashsalt
    mat = re.compile(r'var hashsalt=(.*?);')
    ctx = execjs.compile('')
    # 组装下一次请求的data
    body = {
        'tid': tid,
        'inputvalue': inputvalue,  # 这里是输入值,可变
        'num': num,
        'hashsalt': ctx.eval(mat.findall(str)[0])
    }
    # 第二次请求,用于获取trade_no
    response = requests.post('https://www.daichong.vip/ajax.php?act=pay', headers=headers, data=body, verify=False)
    trade_no = response.json().get('trade_no')
    # 封装data
    body = {
        'orderid': trade_no
    }
    # 第三次最终请求
    response = requests.post('https://www.daichong.vip/ajax.php?act=payrmb', headers=headers, data=body, verify=False)
    return response.json()['msg']+'订单号'+response.json()['orderid']


