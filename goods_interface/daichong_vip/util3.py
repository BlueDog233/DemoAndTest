import os
from bs4 import BeautifulSoup

# specify the directory path
path = './tem'

# specify the CSS selectors of the elements to extract
css_selectors = [
    '#good-img',
    'em',
    'body > div.container > div.public-shop-info > div.body',
    '#inputsname > div',
    'body > div.container > div.public-shop > div.info > div.money.container'
]

# Get a list of all HTML files in the directory
files = [f for f in os.listdir(path) if f.endswith('.html')]

for file in files:
    with open(os.path.join(path, file), encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'lxml')
        file_output = []
        for css_selector in css_selectors:
            element = soup.select_one(css_selector)
            if element:
                file_output.append(str(element))
        output_filename = os.path.join(path, os.path.splitext(file)[0] + '.txt')
        with open(output_filename, 'w', encoding='utf-8') as f_output:
            for item in file_output:
                f_output.write("%s\n" % item)
