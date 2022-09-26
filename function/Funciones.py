
import os
import requests
import numpy as np
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

def dbz2mm(serie_in):
    # convert dbz to mm with marshall-palmer relation
    # R = (10**(Z/10)/200)**0.625
    # Z = 10*np.log10(R**0.625*200)
    lvl = len(serie_in)
    serie_out = np.zeros(lvl)
    for n in range(lvl):
        if serie_in[n] == 0:
            serie_out[n] = 0
        else:
            # serie_out[n] = ((10**(serie_in[n]/10))/200)**0.625
            serie_out[n] = 10**(serie_in[n]/10)
    return serie_out

def mm2dbz(serie_in):
    lvl = len(serie_in)
    serie_out = np.zeros(lvl)
    for n in range(lvl):
        if serie_in[n] == 0:
            serie_out[n] = 0
        else:
            # serie_out[n] = 10*np.log10((serie_in[n]*200)**0.625)
            serie_out[n] = 10*np.log10(serie_in[n])
    return serie_out