
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

def dbz2mm(dbz_input, a=200.0, b=1.6):#ref wradlib, ref: machado a=174.8, b=1.56
    '''
    La refectividad (Z) y la taza de precipitacion (R), se encuentran relacionadas por la ecuacion:
    Z = a * R**b --> R = (Z/a)**(1/b)
    Primero se debe convertir de dBz (decibil de reflectividad de factor Z) a Z (factor de reflectividad), usando
    Z = 10**(dbz/10)
    '''
    # convert dbz to mm with marshall-palmer relation
    # dbz to Z: Z = 10**(dbz/10)
    # Z to R  : Z = a * R**b --> R = (Z/a)**(1/b)
    lvl = len(dbz_input)
    R = np.zeros(lvl)
    for n in range(lvl):
        if dbz_input[n] == 0:
            R[n] = 0
        else:
            Z = 10 ** (dbz_input / 10)
            R[n] = (Z[n] / a) ** (1 / b)
    return R

def mm2dbz(R_input, a=200.0, b=1.6):
    lvl = len(R_input)
    serie_out = np.zeros(lvl)
    for n in range(lvl):
        if R_input[n] == 0:
            serie_out[n] = 0
        else:
            Z = a * R_input[n]**b
            serie_out[n] = 10*np.log10(Z)

            # serie_out[n] = (b*np.log10(R_input[n]*a))
    return serie_out