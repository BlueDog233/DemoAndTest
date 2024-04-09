import re


def get(key: str) -> str:
    with open('../store.txt', 'r', encoding='utf-8') as f:
        match = re.compile("(?:{0}[ ]*)(.*)".format(key))
        str = match.findall(f.read())[0]
        return str


def store(key: str, value: str) -> None:
    with open('../store.txt', 'r+', encoding='utf-8') as f:
        text = f.read()
        try:
            str = text.replace(get(key), value, 1)
            text=str
        except Exception as e:
            text += '\n' + key + ' ' + value
        f.write(text)
        f.close()


if __name__ == '__main__':
    store('daichong_vip_cookiaae', 'aaaaaa')
