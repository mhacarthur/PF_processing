
import os
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup

def get_subdirectories(BASE_URL):
    res = requests.get(BASE_URL)
    soup = BeautifulSoup(res.text, 'html.parser')

    rows = soup.findAll('tr')

    years = []
    for row in rows[3:-2]:
        row = row.find('a')
        years.append(row.attrs['href'])

    return years

def get_url_files(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    
    rows = soup.findAll('tr')
    
    urls = list()

    for row in rows[3:-1]:
        row  = row.find('a')
        try:
            link = row.attrs['href']
            urls.append(os.path.join(url, link))
        except:
            pass
    return urls

def download_file(url_file,file_out):
    res = requests.get(url_file, stream=True)
    total_size = int(res.headers['content-length'])

    with open(file_out, 'wb') as handle:
        for data in tqdm(iterable=res.iter_content(chunk_size=1024), total=total_size/1024, unit='KB'):
            handle.write(data)
    # print("Done!")