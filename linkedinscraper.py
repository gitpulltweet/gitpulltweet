import time
from selenium import webdriver
from splinter.browser import Browser
import requests
import re
from bs4 import BeautifulSoup
import json
import csv

inputfile = raw_input("enter the file name which you want to feed as input(ex:inputsheet.csv):")
username = raw_input("username/emailid of the linkedin account you want to use:")
password = raw_input("password of the linkedin account you want to use:")
action = raw_input("what do you want to fetch leads for?(enter 1 for same company and 2 for other company):")
def get_same_company_details(inputfile,username,password):

    leads={}
    input_file = csv.DictReader(open("{}".format(inputfile)))
    br = Browser('chrome')
    br.driver.set_window_position(0,0)
    br.visit('http://linkedin.com')
    br.fill('session_key', '{}'.format(username))
    br.fill('session_password', '{}'.format(password))
    br.find_by_id('login-submit').first.click()
    dickey = 0
    print "started processing for the given input file {}".format(inputfile)
    #rws = list(input_file)
    for i in input_file:
        print "processing record {} of total 11".format(dickey+1)
        findet=[]
        prfurl=[]
        ccr=[]
        loc=[]
        names=[]
        fnames=[]
        lnames=[]
        br.visit('https://www.linkedin.com/search/results/companies/?keywords={}&origin=GLOBAL_SEARCH_HEADER'.format(i['4 Company']))
        time.sleep(2)
        abc = br.html
        soup = BeautifulSoup(abc,'html.parser')
        alinks = soup.find_all("a",{"data-control-name":"search_srp_result"})
        if (len(alinks)<1):
            print "no matching company found for this record"
            continue
        compid = alinks[0]['href'].split('/')[2]
        br.visit('https://www.linkedin.com/search/results/people/?facetCurrentCompany=%5B%22{}%22%5D&origin=GLOBAL_SEARCH_HEADER&title={}'.format(compid,i['5 career']))
        de = br.html
        dtl = BeautifulSoup(de,'html.parser')
        snames = dtl.find_all("span",{"class":"name actor-name"})
        detail = dtl.find_all("div",{"class":"search-result__info pt3 pb4 ph0"})
        for m in detail:
            j = m.find('a')['href']
            if '#' in j:
                continue
            else:
                findet.append(m)
                prfurl.append(j)
        cnt = 0
        sortarray = ['a','b','c','d','e','f','g','h','i','j']
        for j in range(len(snames)):
            cnt1 = 0
            names.append(snames[j].text)
            i['{}{} fullname_{}'.format(sortarray[cnt],cnt1,cnt)]=snames[j].text.encode('utf8')
            cnt1+=1
            fname = snames[j].text
            i['{}{} first_name_{}'.format(sortarray[cnt],cnt1,cnt)]=fname.split(' ')[0].encode('utf8')
            fnamekey='{}{} first_name_{}'.format(sortarray[cnt],cnt1,cnt)
            cnt1+=1
            i['{}{} last_name_{}'.format(sortarray[cnt],cnt1,cnt)]=fname.split(' ',1)[1].encode('utf8')
            lnamekey='{}{} last_name_{}'.format(sortarray[cnt],cnt1,cnt)
            k = findet[j].find('p',{"class":"subline-level-1 Sans-15px-black-85% search-result__truncate"}).text
            l = findet[j].find('p',{"class":"subline-level-2 Sans-13px-black-55% search-result__truncate"}).text.strip()
            cnt1+=1
            i['{}{} career_{}'.format(sortarray[cnt],cnt1,cnt)]=k
            cnt1+=1
            i['{}{} location_{}'.format(sortarray[cnt],cnt1,cnt)]=l
            cnt1+=1
            i['{}{} email_{}'.format(sortarray[cnt],cnt1,cnt)]= get_email_by_domain(i,fnamekey,lnamekey)
            cnt+=1
        leads[dickey] = i
        dickey+=1
    return leads

def get_different_company_details(inputfile,username,password):
    
    leads={}
    input_file = csv.DictReader(open("{}".format(inputfile)))
    br = Browser('chrome')
    br.driver.set_window_position(0,0)
    br.visit('http://linkedin.com')
    br.fill('session_key', '{}'.format(username))
    br.fill('session_password', '{}'.format(password))
    br.find_by_id('login-submit').first.click()
    time.sleep(10)
    dickey = 0
    print "started processing for the given input file {}".format(inputfile)
    
    for i in input_file:
        time.sleep(2)
        print "processing record {} of total 9".format(dickey+1)
        findet=[]
        prfurl=[]
        ccr=[]
        loc=[]
        names=[]
        fnames=[]
        lnames=[]
        '''
        br.visit('https://www.linkedin.com/search/results/companies/?keywords={}&origin=GLOBAL_SEARCH_HEADER'.format(i['4 Company']))
        time.sleep(2)
        abc = br.html
        soup = BeautifulSoup(abc,'html.parser')
        alinks = soup.find_all("a",{"data-control-name":"search_srp_result"})
        if (len(alinks)<1):
            print "no matching company found for this record"
            continue
        compid = alinks[0]['href'].split('/')[2]
        '''
        br.visit('https://www.linkedin.com/search/results/people/?facetGeoRegion=%5B%22us%3A0%22%5D&origin=GLOBAL_SEARCH_HEADER&title={}'.format(i['5 career']))
        de = br.html
        dtl = BeautifulSoup(de,'html.parser')
        snames = dtl.find_all("span",{"class":"name actor-name"})
        detail = dtl.find_all("div",{"class":"search-result__info pt3 pb4 ph0"})
        for m in detail:
            j = m.find('a')['href']
            if '#' in j:
                continue
            else:
                findet.append(m)
                prfurl.append(j)
        cnt = 0
        sortarray = ['a','b','c','d','e','f','g','h','i','j']
        for j in range(len(snames)):
            cnt1 = 0
            names.append(snames[j].text)
            i['{}{} fullname_{}'.format(sortarray[cnt],cnt1,cnt)]=snames[j].text.encode('utf8')
            cnt1+=1
            fname = snames[j].text
            i['{}{} first_name_{}'.format(sortarray[cnt],cnt1,cnt)]=fname.split(' ')[0].encode('utf8')
            fnamekey='{}{} first_name_{}'.format(sortarray[cnt],cnt1,cnt)
            cnt1+=1
            i['{}{} last_name_{}'.format(sortarray[cnt],cnt1,cnt)]=fname.split(' ',1)[1].encode('utf8')
            lnamekey='{}{} last_name_{}'.format(sortarray[cnt],cnt1,cnt)
            k = findet[j].find('p',{"class":"subline-level-1 Sans-15px-black-85% search-result__truncate"}).text
            l = findet[j].find('p',{"class":"subline-level-2 Sans-13px-black-55% search-result__truncate"}).text.strip()
            z1 = findet[j].find('p',{"class":"search-result__snippets mt2 Sans-13px-black-55% ember-view"})
            #z1t = type(z1)
            #print z1
            if z1 is None:
                z=''
            else:
                z=z1.text        
            cnt1+=1
            i['{}{} career_{}'.format(sortarray[cnt],cnt1,cnt)]=k
            cnt1+=1
            if 'at ' in k:
                i['{}{} company_{}'.format(sortarray[cnt],cnt1,cnt)]=k.split('at ')[1].encode('utf8')
            elif 'at ' in z:
                i['{}{} company_{}'.format(sortarray[cnt],cnt1,cnt)]=z.split('at ')[1].encode('utf8')
            else:
                #br.visit("https://linkedin.com{}".format(prfurl[j]))
                #soup2 = BeautifulSoup(br.html,'html.parser')    soup2.find('span',{"class":"pv-entity__secondary-title"}).text
                i['{}{} company_{}'.format(sortarray[cnt],cnt1,cnt)]="none"
            compkey='{}{} company_{}'.format(sortarray[cnt],cnt1,cnt)
            cnt1+=1
            i['{}{} location_{}'.format(sortarray[cnt],cnt1,cnt)]=l
            cnt1+=1
            i['{}{} email_{}'.format(sortarray[cnt],cnt1,cnt)]= get_email_by_company(i,fnamekey,lnamekey,compkey)
            cnt+=1
        leads[dickey] = i
        dickey+=1
        if action == "1":
            inputfile1= "samecompany"+inputfile
        elif action == "2":
            inputfile1= "diffcompany"+inputfile
        with open("output_{}.json".format(inputfile1),"w") as file:
            json.dump(leads, file)
    time.sleep(5)
    return leads

def get_email_by_domain(i,fnamekey,lnamekey):
    try:
        s = requests.session()
        rawmail = s.get("https://api.hunter.io/v2/email-finder?domain={}&first_name={}&last_name={}&api_key=<<hunter api key should come here>>".format(i['3 Domain'],i[fnamekey],i[lnamekey]))
        mailop = rawmail.json()
        return mailop['data']['email']
    except:
        return "no email found"

def get_email_by_company(i,fnamekey,lnamekey,compkey):
    try:
        s = requests.session()
        rawmail = s.get("https://api.hunter.io/v2/email-finder?company={}&first_name={}&last_name={}&api_key=<<hunter api key should come here>>".format(i[compkey],i[fnamekey],i[lnamekey]))
        mailop = rawmail.json()
        return mailop['data']['email']
    except:
        return "no email found"
def safe_encode(obj):
    if isinstance(obj, (list, dict)):
        for i, item in iterable_list_or_dict(obj):
            obj[safe_encode(i)] = safe_encode(item)
    try:
        return obj.encode('utf8')
    except AttributeError:
        return obj
def write_to_csv(leads,inputfile):
    with open("output_{}.json".format(inputfile),"w") as file:
        json.dump(leads, file)
    time.sleep(5)
    with open("output_{}.json".format(inputfile),"r") as file:
        leads1 = json.loads(file.read())
    
    print "Writing the results to an output csv file output_{}".format(inputfile)
    with open("output_{}".format(inputfile),"wb") as f:
        headers = sorted(reduce(lambda accum_value, x: accum_value | set(x.keys()), leads1.values(), set()))
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows({safe_encode(k):safe_encode(v) for k,v in row.items()} for row in leads1.values() if row)



if inputfile == "" or action == "" or username == "" or password == "":
    print " "
    print "you havent given full details, run again and please make sure you give all the details correctly"
else:
    if action == "1":
        leads = get_same_company_details(inputfile,username,password)
        inputfile1= "samecompany"+inputfile
        write_to_csv(leads,inputfile1)
    elif action == "2":
        leads = get_different_company_details(inputfile,username,password)
        inputfile1= "diffcompany"+inputfile
        write_to_csv(leads,inputfile1)

    
