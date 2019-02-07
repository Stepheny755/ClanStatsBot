import numpy as np
import json,csv,os

from util import Util

tdir = "Data/testdata"
adir = "Data"
wdir = "Data/wowsnumbers"

class Data():

    name = ''

    def __init__(self): #,inp):
        #self.name = inp
        pass

    def testread(self,filename):
        rdarr = []
        with open(os.path.join(tdir,filename).strip(),'r') as r:
            rdarr = list(csv.reader(r,delimiter=','))
        return rdarr
 
    def testwrite(self,relativepath,filename,output):
        temppath = os.path.join(tdir,relativepath).strip()
        if not os.path.exists(temppath):
            os.makedirs(temppath)
        with open(os.path.join(temppath,filename).strip(),'w+') as w:
            out = csv.writer(w)
            out.writerows(output)
    
    def read(self,relativepath,filename):
        rdarr = []
        temppath = os.path.join(adir,relativepath).strip()
        with open(os.path.join(temppath,filename).strip(),'r') as r:
            rdarr = list(csv.reader(r,delimiter=','))
        return rdarr
 
    def write(self,relativepath,filename,output):
        temppath = os.path.join(adir,relativepath).strip()
        if not os.path.exists(temppath):
            os.makedirs(temppath)
        with open(os.path.join(temppath,filename).strip(),'w+') as w:
            out = csv.writer(w)
            out.writerows(output)

    def getMostRecent(self):
        #TODO: Find value (either ID or name of ship) in expected value csv, and return associated dmg,frag, and WR data
        lst = []
        for file in os.listdir(wdir):
            if file.endswith('.csv'):
                lst.append(file)
        return max(lst)

    def getExpectedData(self):
        filename = self.getMostRecent()
        file = self.read('wowsnumbers',filename)
        #print(file)
        return file

    def trackClan(self,clanname,data):
        temppath = os.path.join(adir,clanname).strip()
        if not os.path.exists(temppath):
            os.makedirs(temppath)
        u = Util()
        time = u.getGMTTime()
        self.write(clanname,str(time)+'.csv',data)
        pass

if(__name__=="__main__"):

    d = Data()
    #d.testwrite('test','test1.csv',[['jacky','cool'],['jacky','smart']])
    #c = d.testread('Book1.csv')
    #c = d.read("",'ClanList')
    #print(c)
    #for i in c:
        #for z in i:
            #print(z)
    print("done")
    #print(d.getMostRecent())
    #print(d.getExpectedData())
    print(d.trackClan('MIA',[['mod','shitter'],['ddak','absolut trash'],['warlord','legend']]))
