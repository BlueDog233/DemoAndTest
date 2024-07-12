import threading
import time

import requests
import signal
import sys
from utils import read, download_file
from lxml import html
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

notdos = list()
proxy='O24071218402747623548_1:PyMNKosT@static-qiye.hailiangip.com:41549'

def changeProxy():
    req = requests.post(
        url='https://www.hailiangip.com/window/getip/add-whites',
        headers={'Cookie':'hailianipUserSsId=9420lyif3gov; Hm_lvt_9e39edf70678fdfa22949c4a21bae902=1720771793; HMACCOUNT=458E1F30D73633CE; mediav=%7B%22eid%22%3A%22836637%22%2C%22ep%22%3A%22%22%2C%22vid%22%3A%22%5EQ%3AnvT%60KM%5D%3Dh%6089D%25jGS%22%2C%22ctn%22%3A%22%22%2C%22vvid%22%3A%22%5EQ%3AnvT%60KM%5D%3Dh%6089D%25jGS%22%2C%22_mvnf%22%3A1%2C%22_mvctn%22%3A0%2C%22_mvck%22%3A0%2C%22_refnf%22%3A0%7D; _clck=rgv730%7C2%7Cfne%7C0%7C1654; AGL_USER_ID=dcc1c7f3-2f2b-4082-bfc7-dbe309fd2137; userMobile=18180034455; menuShowFlag=1; userCertStatus_18180034455=1; _gid=GA1.2.805978769.1720773712; hailianipUserRefHost=unitradeprod.alipay.com; hailianipUserBaiduIdWord=; _ga=GA1.1.1819772394.1720773711; Qs_lvt_345494=1720771793%2C1720774430%2C1720779337%2C1720780882; isOrder_18180034455=4; _uetsid=1e39f4f0402611efbbc1874b8679fa06; _uetvid=1e39e5a0402611ef8c41bb9741cff89f; _uetmsclkid=_uet419541f7db36183dcf5a27673ff38336; _clsk=184gx4x%7C1720781229680%7C14%7C1%7Cp.clarity.ms%2Fcollect; _ga_DMP7XFZMMQ=GS1.1.1720777115.2.1.1720781292.0.0.0; Qs_pv_345494=4348573549595559400%2C1713882812210094300%2C1883150101786618400%2C4439158842232267300%2C2758183938432298000; Hm_lpvt_9e39edf70678fdfa22949c4a21bae902=1720781294; liuguanphp_session=eyJpdiI6InlGbDVZaFBxcEYzSGZzQUg1QzNsaUE9PSIsInZhbHVlIjoiaU53Y3FKamdaSlhXKzMwREEwWGF0eEdPVVBhbFpJSk5Yekp6WnExSmZabzI3ZHh1Vjk5bUtiOUpzTzhpN2lYREF1VjBWNFd1SWpLSDhod1ZMZG1GTW43cXh6ZHlSR3U2dUw3SFFzM01wOFwvcE94V3NIanJTY0JiekJGaVB4bWR5IiwibWFjIjoiZDI3ZjY0OWVkMjlhYzhlNmU3MjhjYzEzM2ZlZjk4NzI0ZjZhYjkyMDczOGE3YTcwZjBjNTUwNTM0YjM4ZGEyZSJ9'},
        params={'id': '9359', 'pid' :-1,'cid':-1}
    )
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
        time.sleep(60)
        save_progress()
        time_count=time_count+1
        if time_count==120 :
            changeProxy()

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
