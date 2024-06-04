import requests
from utils import read, download_file
from lxml import html
from concurrent.futures import ThreadPoolExecutor

notdos=list()
def download(keyword:str):
    keyword=keyword.replace('\n','')
    try:
        response=requests.get('https://zinc20.docking.org/substances/search/?q='+keyword)
        response.raise_for_status()
        web_content = html.fromstring(response.content)
        href_value = web_content.xpath('//*[@id="print"]/div/div[1]/div/h4/a/@href')[0]
        x=href_value.split('/')[2]
        download_file(url="https://zinc20.docking.org/substances/"+x+'.sdf',location='./data',filename=keyword+'_'+x+'.sdf')
        notdos.remove(keyword)
        print(keyword+' 成功下载')
    except Exception as e:
        print(keyword+'发生错误')
        pass
def work(keyword):
    download(keyword)
    pass

with ThreadPoolExecutor(max_workers=40) as executor:
    workLists = read(file_path='./work.txt', read_as_line=True, delete_after_read=False)
    workLists=list(set(workLists))
    notdos=workLists
    tasks = [executor.submit(work, keyword) for keyword in workLists]
    for task in tasks:
        task.result()

# Added new lines to overwrite the remaining notdos list to work.txt
with open('./work.txt', 'w') as file:
    for item in notdos:
        file.write(f'{item}')