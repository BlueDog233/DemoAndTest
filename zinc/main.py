import time

import requests
import signal
import sys
from utils import read, download_file
from lxml import html
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

notdos = list()


def addWhiteip():
    myip = requests.get('https://api.ipify.org').text
    req = requests.post(
        url='https://www.hailiangip.com/window/getip/add-whites',
        headers={'Cookie':'hailianipUserSsId=9420lyif3gov; Hm_lvt_9e39edf70678fdfa22949c4a21bae902=1720771793; HMACCOUNT=458E1F30D73633CE; mediav=%7B%22eid%22%3A%22836637%22%2C%22ep%22%3A%22%22%2C%22vid%22%3A%22%5EQ%3AnvT%60KM%5D%3Dh%6089D%25jGS%22%2C%22ctn%22%3A%22%22%2C%22vvid%22%3A%22%5EQ%3AnvT%60KM%5D%3Dh%6089D%25jGS%22%2C%22_mvnf%22%3A1%2C%22_mvctn%22%3A0%2C%22_mvck%22%3A0%2C%22_refnf%22%3A0%7D; _clck=rgv730%7C2%7Cfne%7C0%7C1654; AGL_USER_ID=dcc1c7f3-2f2b-4082-bfc7-dbe309fd2137; userMobile=18180034455; menuShowFlag=1; userCertStatus_18180034455=1; _gid=GA1.2.805978769.1720773712; isOrder_18180034455=2; hailianipUserRefHost=unitradeprod.alipay.com; Qs_lvt_345494=1720771793%2C1720774430; _ga=GA1.2.1819772394.1720773711; _ga_DMP7XFZMMQ=GS1.1.1720773710.1.1.1720774765.0.0.0; _clsk=9rzzyj%7C1720774813824%7C14%7C1%7Cv.clarity.ms%2Fcollect; _uetsid=1e39f4f0402611efbbc1874b8679fa06; _uetvid=1e39e5a0402611ef8c41bb9741cff89f; _uetmsclkid=_uet419541f7db36183dcf5a27673ff38336; Hm_lpvt_9e39edf70678fdfa22949c4a21bae902=1720776220; Qs_pv_345494=2552500662699517000%2C482121187684405950%2C2882825190679268400%2C182922715033518460%2C4227238341980695000; liuguanphp_session=eyJpdiI6IkM1dFV5cUtuTXhzVVwvVHJCZkhxR0t3PT0iLCJ2YWx1ZSI6IkdCM0JCS0paZUdqZnFkSnh2NldzaHF6OUN1eWZcL0lrZ1FtQktZRWFTNDdYTUZGVElnOU9wUnhkbnZHY09xblpqZEJSS2tiNGYzUWljZnlTV1ZUeDMwdFdRaFRWQUZNZkFIbEo4N1B4cUZNTXhrYVN3OUJ0R2ptZ291NW52QTFhVSIsIm1hYyI6IjM2OTQ3MmZkNTFjN2VjOTdmNTg5NDZlNDAxZTk2YTQ2YTI3M2NiNDcwZWZkM2RiNzg1NDJjNGUxMzUyYzVlZjYifQ%3D%3D'},
        params={'orderId': 'O24071216114208275442', 'ip' :myip}
    )

proxy=''
def getProxy():
    res = requests.get(
        'http://api.hailiangip.com:8422/api/getIp?type=1&num=1&pid=-1&unbindTime=600&cid=-1&orderId=O24071216114208275442&time=1720777807&sign=190095c6737cd7e26b5856eaceaf8e43&noDuplicate=1&dataType=1&lineSeparator=0')
    content = res.text
    proxy = content
    return proxy

proxy=getProxy();
def save_progress():
    with open('./work.txt', 'w') as file:
        for item in notdos:
            file.write(f'{item}')
# proxy=getProxy();
def signal_handler(sig, frame):
    print('Caught signal:', sig, 'Saving notdos and exiting.')
    save_progress()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def download(keyword: str):
    global proxy
    keyword = keyword.replace('\n', '')
    try:
        myip = requests.get('https://api.ipify.org').text
        req = requests.post(
            url='https://www.hailiangip.com/window/getip/add-whites',
            headers={
                'Cookie': 'hailianipUserSsId=9420lyif3gov; Hm_lvt_9e39edf70678fdfa22949c4a21bae902=1720771793; HMACCOUNT=458E1F30D73633CE; mediav=%7B%22eid%22%3A%22836637%22%2C%22ep%22%3A%22%22%2C%22vid%22%3A%22%5EQ%3AnvT%60KM%5D%3Dh%6089D%25jGS%22%2C%22ctn%22%3A%22%22%2C%22vvid%22%3A%22%5EQ%3AnvT%60KM%5D%3Dh%6089D%25jGS%22%2C%22_mvnf%22%3A1%2C%22_mvctn%22%3A0%2C%22_mvck%22%3A0%2C%22_refnf%22%3A0%7D; _clck=rgv730%7C2%7Cfne%7C0%7C1654; AGL_USER_ID=dcc1c7f3-2f2b-4082-bfc7-dbe309fd2137; userMobile=18180034455; menuShowFlag=1; userCertStatus_18180034455=1; _gid=GA1.2.805978769.1720773712; isOrder_18180034455=2; hailianipUserRefHost=unitradeprod.alipay.com; Qs_lvt_345494=1720771793%2C1720774430; _ga=GA1.2.1819772394.1720773711; _ga_DMP7XFZMMQ=GS1.1.1720773710.1.1.1720774765.0.0.0; _clsk=9rzzyj%7C1720774813824%7C14%7C1%7Cv.clarity.ms%2Fcollect; _uetsid=1e39f4f0402611efbbc1874b8679fa06; _uetvid=1e39e5a0402611ef8c41bb9741cff89f; _uetmsclkid=_uet419541f7db36183dcf5a27673ff38336; Hm_lpvt_9e39edf70678fdfa22949c4a21bae902=1720776220; Qs_pv_345494=2552500662699517000%2C482121187684405950%2C2882825190679268400%2C182922715033518460%2C4227238341980695000; liuguanphp_session=eyJpdiI6IkM1dFV5cUtuTXhzVVwvVHJCZkhxR0t3PT0iLCJ2YWx1ZSI6IkdCM0JCS0paZUdqZnFkSnh2NldzaHF6OUN1eWZcL0lrZ1FtQktZRWFTNDdYTUZGVElnOU9wUnhkbnZHY09xblpqZEJSS2tiNGYzUWljZnlTV1ZUeDMwdFdRaFRWQUZNZkFIbEo4N1B4cUZNTXhrYVN3OUJ0R2ptZ291NW52QTFhVSIsIm1hYyI6IjM2OTQ3MmZkNTFjN2VjOTdmNTg5NDZlNDAxZTk2YTQ2YTI3M2NiNDcwZWZkM2RiNzg1NDJjNGUxMzUyYzVlZjYifQ%3D%3D'},
            params={'orderId': 'O24071216114208275442', 'ip': myip}
        )
        response = requests.get('https://zinc20.docking.org/substances/search/?q=' + keyword, proxies={'https':proxy})
        response.raise_for_status()
        web_content = html.fromstring(response.content)
        href_value = web_content.xpath('//*[@id="print"]/div/div[1]/div/h4/a/@href')[0]
        x = href_value.split('/')[2]
        download_file(url="https://zinc20.docking.org/substances/" + x + '.sdf', location='./data',
                      filename=keyword + '_' + x + '.sdf',proxies={'https': proxy})
        print(keyword + ' 成功下载')
        return keyword + '\n'
    except Exception as e:
        print(e)
        if '702' in e.__str__():
            proxy=getProxy()
        if '704' in e.__str__():
            addWhiteip()
        print(keyword + '发生错误')
        return None


with ThreadPoolExecutor(max_workers=32) as executor:
    workLists = read(file_path='./work.txt', read_as_line=True, delete_after_read=False)
    workLists = list(set(workLists))
    notdos = workLists
    tasks = {executor.submit(download, keyword): keyword for keyword in workLists}
    pbar = tqdm(total=len(workLists), ncols=70)

    for future in as_completed(tasks):
        keyworded = tasks[future]
        try:
            keyword_returned = future.result()
        except Exception as exc:
            print(f'Generated an exception: {exc}')
        else:
            if keyword_returned is not None:
                notdos.remove(keyword_returned)
        pbar.update(1)

    pbar.close()

save_progress()
