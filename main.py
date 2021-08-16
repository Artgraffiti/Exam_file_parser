import os
from bs4 import BeautifulSoup
import requests
from urllib.request import urlretrieve
from urllib.error import HTTPError


start = int(input("Enter start of range: "))
variant_id = input("Enter the variant id: ")


def save_as_file(fileobject, filename):
    with open(filename, 'wb') as f:
        f.write(fileobject)


res = requests.get(f'https://inf-ege.sdamgia.ru/test?id={variant_id}&nt=True&pub=False')
res.encoding = 'utf-8'
soup = BeautifulSoup(res.text, 'lxml')

probs = soup.find_all('div', {'class': 'prob_list'})[0]
probs_A = probs.find_all('a', text='Файл A')
probs_B = probs.find_all('a', text='Файл B')


base_link = 'https://inf-ege.sdamgia.ru'

for n, prob_A, prob_B in zip(range(start, start+len(probs_A)), probs_A, probs_B):
    link_part_A = prob_A['href']
    link_part_B = prob_B['href']
    print(f'{n}: {link_part_A=}, {link_part_B=}')
    directory = f'27-{n}'
    f1 = f'{directory}/Файл А.txt'
    f2 = f'{directory}/Файл В.txt'
    os.mkdir(directory)
    main_f = open(f'{directory}/main.py', 'w')
    main_f.close()
    try:
        urlretrieve(base_link + link_part_A, f1)
        urlretrieve(base_link + link_part_B, f2)
    except HTTPError:
        file_obj_A = requests.get(base_link + link_part_A).content
        file_obj_B = requests.get(base_link + link_part_B).content
        save_as_file(file_obj_A, f1)
        save_as_file(file_obj_B, f2)
    print(f'{n}: Done')
