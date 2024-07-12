import os
import shutil
from pathlib import Path
from typing import Callable
import requests
from urllib3 import HTTPSConnectionPool


def operation():
    # 1.获取调用该函数的.py文件的绝对路径
    caller_file_path = os.path.abspath(__file__)
    caller_directory = os.path.dirname(caller_file_path)
    return caller_directory


def read(file_path: str, read_as_line: bool = False, delete_after_read: bool = False, method: Callable = None):
    content = []
    with open(file_path, 'r') as file:
        if read_as_line:
            content = file.readlines()
        else:
            content = file.read()

    if delete_after_read:
        if read_as_line:
            with open(file_path, 'w') as file:
                file.writelines(content[1:])
        else:
            file.write("")
    if method is not None:

        content = method(content)
    return content


def append_by_line(file_path: str, content: str):
    with open(file_path, 'a') as file:
        file.write(f'{content}')


def overwrite(file_path: str, content: str):
    with open(file_path, 'w') as file:
        file.write(content)


def download_file(location: str, url: str, filename: str,proxies):
    # Send a HTTP request to the URL of the file
    if proxies is not None:
        try:
            response = requests.get(url, stream=True,proxies=proxies)
        except Exception as e:
            response = requests.get(url, stream=True,proxies=proxies)
    else:
        response = requests.get(url, stream=True)
    try:
        # Open the file in write mode
        with open(os.path.join(location, filename), 'wb') as file:
            # Write data read from the response
            for data_chunk in response.iter_content(chunk_size=8192):
                file.write(data_chunk)
    except Exception as e:
        print(e)



