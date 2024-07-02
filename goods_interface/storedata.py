import os
import re

script_dir = os.path.dirname(__file__)  # absolute dir the script is in
rel_path = "./store.txt"
abs_file_path = os.path.join(script_dir, rel_path)

def get(key: str) -> str:
    with open(abs_file_path, 'r', encoding='utf-8') as f:
        match = re.compile("(?:{0}[ ]*)(.*)".format(key))
        str = match.findall(f.read())[0]
        return str


def store(key: str, value: str) -> None:
    with open(abs_file_path, 'a+', encoding='utf-8') as f:
        f.seek(0)
        text = f.read()
        f.seek(0)
        try:
            new_text = text.replace(get(key), value, 1)
            text = new_text
        except Exception as e:
            text += '\n' + key + ' ' + value
        f.write(text)
        f.truncate()



if __name__ == '__main__':
    store('daichong_vip_cookiaae', 'aaaaaa')
