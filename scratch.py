# -*- encoding: utf-8 -*-


import urllib3
import requests

from bs4 import BeautifulSoup


url = r"http://www.uvkmulticines.com/multicines/cine/UVK-LARCOMAR"

def main():

    r = requests.get(url)
    print r.status_code
    html =  r.text.encode(encoding='utf-8', errors='replace')
    
    soup = BeautifulSoup(html)
    
    p1 = soup.find_all('div', class_='highslide-body')
    
    for p in p1:
        print p
        print '-'*15
    
    peliculas = p1[0].find_all('td', class_='bg_infotabla1')
    print peliculas



if __name__ == '__main__':

    main()