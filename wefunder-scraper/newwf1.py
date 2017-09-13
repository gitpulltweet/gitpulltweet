## This file is to scrape all the investor details of one comapny           ##
## The methods in this file will be called in the file wefundercontinous.py ##

import requests
import re
from bs4 import BeautifulSoup
import json
import csv


##This Function will fetch all the list of investor profile links##

def get_investors_of_single_company(wcompany):
    prf=[]
    s = requests.Session()

    ##range will be number of investors/30 as we have 30 per page, as no company has more than 6000 i made it fixed at 200##

    for k in range(200):
        headers ={
        'Accept':'*/*',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With':'XMLHttpRequest'
        }
        data={'page':'{}'.format(k)}
        print k
        urltopost = "https://wefunder.com/api/{}/investors".format(wcompany)
        result = s.post(urltopost, data=data, headers=headers)
        print data
        soup = BeautifulSoup(result.text)
        for a in soup.find_all('a',class_="name", href=True):
            prf.append(a['href'])
        
        print "number of investors fetched"
        print len(prf)
        #print prf
        
    ##This is extra part to fetch the investors which appears on homepage of company, before clicking on more ##
        
    result1 = s.get("https://wefunder.com/{}".format(wcompany))
    soup1 = BeautifulSoup(result1.text)
    if soup1.find('div',{"class":"render_investors investors"}) is not None:
        flst = soup1.find('div',{"class":"render_investors investors"})
        
    
        #print flst.text
        for a in flst.find_all('a',class_="name", href=True):
            prf.append(a['href'])
    investors = {}
    return prf

## get_details This function is to get full details of each investor fetched by above function ##
      
def get_details(prf):
    count = 0
    print prf
    print count
    investors={}
    for wlink in prf:
        count+=1
        '''
        if (count<=43):
            continue
        '''
        ##Below three lines are for printing the status of number of investors scraped of total number ##

        print "scraping investor"
        print wlink
        print "{} of {}".format(count,len(prf))
        
        investor ={}
        investor['3_linkedin'] = ""
        investor['4_facebook'] = ""
        investor['5_twitter'] = ""

        s = requests.Session()
        investor['0_wefunderlink']= "https://wefunder.com{}".format(wlink)
        profpage = s.get("https://wefunder.com/{}".format(wlink))
        if 'home_v4' in profpage.text:
            continue
        dickey = "https://wefunder.com{}".format(wlink)

        soup = BeautifulSoup(profpage.text,'html.parser')
        ## This if condition is to identify an unofficial profile such as y combinator and ignore it
        if 'unofficial' in profpage.text:
            print "unofficial profile identified"
            continue

        name = (soup.find('h1').text).split(" ",1)

        investor['1_first_name'] = name[0].encode('utf-8')
        investor['2_last_name'] = name[1].encode('utf-8')

        for lnk in soup.find_all('a', href=True):
            if 'linkedin.com' in lnk['href']:
                investor['3_linkedin'] = lnk['href'].encode('utf-8')
            elif 'facebook.com' in lnk['href'] and 'http://facebook.com/wefunder' not in lnk['href']:
                investor['4_facebook'] = lnk['href'].encode('utf-8')
            elif 'twitter.com' in lnk['href'] and 'http://twitter.com/wefunder' not in lnk['href']:
                investor['5_twitter'] = lnk['href'].encode('utf-8')
        if soup.find("div",{"class":"my_link"}) is not None:
            investor['6_my_link'] = soup.find("div",{"class":"my_link"}).a['href'].encode('utf-8')



        investor['6_location'] = (soup.find("div",{"class":"dimmer location"}).text.encode('utf-8')).strip().split("\n",1)[0]
        if soup.find("i",{"class":"bio"}) is not None:
            desc = soup.find("i",{"class":"bio"}).text
            investor['7_description'] = desc.encode('utf-8')
        else:
            investor['7_description'] = ""
            
        ## This part is fetch the investments of that investor ##
            
        if soup.find("span",{"class":"investment_count"}) is not None:
            
            invcount = str(soup.find("span",{"class":"investment_count"}).text).split(" ")[0]
            print invcount
            invname = []
            invlink = []
            for l in soup.find("div",{"class":"portfolio"}).find_all('a',href=True):
                invlink.append("https://wefunder.com{}".format(l['href']))
            for k in soup.find_all("div",{"class":"company"}):
                a = k.find('img', alt=True)
                invname.append(str(a['alt']))

            investment = []
            if (int(invcount)<=5):
                r = int(invcount)
            else:
                r = int('5')
            for i in range(r):
                #print i
                nam="investment_{}_name".format(i)
                lnk="investment_{}_link".format(i)
                
                investor[nam]=invname[i]
                investor[lnk]=invlink[i]
        else:
            investor['7_investments']=""

        investors[dickey]=investor

    return investors

## This function is to write the dictionary of investors to a csv file with keys as headers ##
def write_investors_to_csv(investors,wcompany):
    with open("{}.csv".format(wcompany),"wb") as f:
        headers = sorted(reduce(lambda accum_value, x: accum_value | set(x.keys()), investors.values(), set()))
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(investors.values())

        

