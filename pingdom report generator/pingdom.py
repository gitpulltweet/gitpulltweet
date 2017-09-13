
import pingdomlib
import sys
import datetime
import time
import json


api = pingdomlib.Pingdom('<<pingdom username>>','<<pingdom password>>','<<pingdom api key>>')
pingdomchecks = api.getChecks()
#print type(pingdomchecks)
cidl=[]#this will get the list of id's
cnamel=[]#this will get list of names
cstatusl=[]
bcnamel=[]
bcidl=[]
for check in pingdomchecks:
    # See pingdomlib.check documentation for information on PingdomCheck class
     cid=check.id
     cstatus=check.status
     cname=check.name
     cidl.append(cid)
     cnamel.append(cname)
     cstatusl.append(cstatus)


argmnt=sys.argv[1]
#print argmnt
argmnt2=sys.argv[2]
#print argmnt2
#argmnt3=sys.argv[3]
#print argmnt3

def statusfn(nam,env):
        for i in range(len(cidl)):
                if nam in cnamel[i] and env in cnamel[i]:
                        bcnamel.append(cnamel[i])
                        bcidl.append(cidl[i])


statusfn(argmnt,argmnt2)
data={}
a=[]
for checker in bcidl:
        timen=int(time.time())
        timef=timen-14400
        timebaseend=timef-604800
        timebasestart=timebaseend-14400
        ncheck=api.getCheck(checker)
        avgt=ncheck.averages( time_from = timef )
        baseavgt=ncheck.averages(time_from = timebasestart, time_to = timebaseend)
        avgt1=avgt[u'responsetime']
        avg=avgt1[u'avgresponse']
        baseavgt1=baseavgt[u'responsetime']
        baseavg=baseavgt1[u'avgresponse']
        #print "average response time of" + ncheck.name + "in last 4 hours is   -->  " + str(avg)
        #data[str(ncheck.name)]=str(avg)
        diff = avg - baseavg
        data['name']=str(ncheck.name)
        data['avgresponse']=str(avg)
        data['baseavgresponse']=str(baseavg)
        data['delta']=str(diff)
        a.append(dict(data))
        #print tabulate([[ncheck.name, str(avg)]], headers=['Name', 'Avg'])
abc=json.dumps(a)
print abc
