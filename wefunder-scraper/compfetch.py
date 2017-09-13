import requests
from bs4 import BeautifulSoup
import json
s = requests.Session()
compname=[]
headers ={
        'Accept':'*/*',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With':'XMLHttpRequest'
        }
for i in range(15):
    result = s.post("https://wefunder.com/axaj_render_cards_v4?type=funded&page={}&first_offset=6".format(i), headers=headers)
    soup = BeautifulSoup(result.text)
    for j in soup.find_all('div',{"flipped":"false"}):
        l=j.find('a',href=True)
        print l['href']
        
        compname.append(j.a['href'])
    print compname
    
    
