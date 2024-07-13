import threading
import time

import requests
import signal
import sys
from utils import read, download_file
from lxml import html
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from DrissionPage import WebPage
from DrissionPage import ChromiumPage

notdos = list()
proxy='O24071218402747623548_1:PyMNKosT@static-qiye.hailiangip.com:41549'

def changeProxy():
    page = ChromiumPage()
    page.get('https://www.hailiangip.com/')
    try:
        page.ele('@@class=new-before-close@@onClick=closeIpStaticCoupons()').click()
    except Exception as e:
        pass
    try:
        page.ele('@id=top-login-btn').click()
        page.ele('@name=username-mobile').input('18180034455')
        page.ele('@name=password').input('bluedog233')
        page.ele('@class=btn btn-primary login-button').click()
    except Exception as e:
        pass
    page.get('https://www.hailiangip.com/personal/order/detail?orderId=O24071218402747623548')
    page.listen.start('webOrder/getOrderRedirectLinePage')
    page.ele('@class=search').click()
    i=0
    for packet in page.listen.steps():
        i=i+1
        cookie=packet.request.extra_info.headers.get('cookie')
        req = requests.post(
            url='https://www.hailiangip.com/update/new/lineConfig',
            headers={
                'Cookie': cookie},
            params={'id': '9359', 'pid': -1, 'cid': -1}
        )
        print(req.content)
        if(i==1):
            break

changeProxy()
def save_progress():
    with open('./work.txt', 'w') as file:
        for item in notdos:
            file.write(f'{item}')
# proxy=getProxy();




length=999
count=0
def download(keyword: str):
    global count
    global save_point
    keyword = keyword.replace('\n', '')
    try:
        response = requests.get('https://zinc20.docking.org/substances/search/?q=' + keyword, proxies={'https':proxy})
        response.raise_for_status()
        web_content = html.fromstring(response.content)
        href_value = web_content.xpath('//*[@id="print"]/div/div[1]/div/h4/a/@href')[0]
        x = href_value.split('/')[2]
        download_file(url="https://zinc20.docking.org/substances/" + x + '.sdf', location='./data',
                      filename=keyword + '_' + x + '.sdf',proxies={'https': proxy})
        print(keyword + ' 成功下载')
        save_point=save_point+1

        return keyword + '\n'
    except Exception as e:
        print(e)
        print(keyword + '发生错误')
    finally:
        count=count+1
        print(str(count)+'/'+str(length)+'   SUCCCESS:'+str(save_point))


time_count=0
def delay_save():
    global time_count
    while 1:
        time.sleep(5)
        save_progress()
        time_count=time_count+1
        if time_count==120 :
            changeProxy()
            time_count=0

save_point=0

with ThreadPoolExecutor(max_workers=32) as executor:
    try:
        workLists = read(file_path='./work.txt', read_as_line=True, delete_after_read=False)
        workLists = list(set(workLists))
        length=len(workLists)
        notdos = workLists
        executor.submit(delay_save)
        tasks = {executor.submit(download, keyword): keyword for keyword in workLists}
        for future in as_completed(tasks):
            keyworded = tasks[future]
            try:
                keyword_returned = future.result()
            except Exception as exc:
                print(f'Generated an exception: {exc}')
            else:
                if keyword_returned is not None:
                    notdos.remove(keyword_returned)
    except Exception as e:
        print(e)
        save_progress()
save_progress()

import signal
import time
import multiprocessing as mp

def worker():
    while True:
        print('Worker running...')
        time.sleep(1)

def signal_handler(sig, frame):
    print('Caught signal:', sig, 'Saving notdos and exiting.')
    save_progress()
    sys.exit(0)
