import requests
import signal
import sys
from utils import read, download_file
from lxml import html
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

notdos = list()

def save_progress():
    with open('./work.txt', 'w') as file:
        for item in notdos:
            file.write(f'{item}')

def signal_handler(sig, frame):
    print('Caught signal:', sig, 'Saving notdos and exiting.')
    save_progress()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def download(keyword: str):
    keyword = keyword.replace('\n', '')
    try:
        response = requests.get('https://zinc20.docking.org/substances/search/?q=' + keyword)
        response.raise_for_status()
        web_content = html.fromstring(response.content)
        href_value = web_content.xpath('//*[@id="print"]/div/div[1]/div/h4/a/@href')[0]
        x = href_value.split('/')[2]
        download_file(url="https://zinc20.docking.org/substances/" + x + '.sdf', location='./data',
                      filename=keyword + '_' + x + '.sdf')
        print(keyword + ' 成功下载')
        return keyword + '\n'
    except Exception as e:
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
