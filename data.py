import json,csv,os,pickle

from util import Util

adir = "Data"

class Data():

    name = ''

    def __init__(self):
        pass

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


    def append(self,relativepath,filename,output):
        temppath = os.path.join(adir,relativepath).strip()
        if not os.path.exists(temppath):
            os.makedirs(temppath)
        with open(os.path.join(temppath,filename).strip(),'a+') as a:
            a.write(output+"\n")

# READ WRITE APPEND FUNCTIONS
# CLAN RELATED FUNCTIONS

    def addToClanlist(self,name):
        templist = self.read('','ClanList')
        for clanname in templist:
            if(clanname[0]==name):
                print(clanname[0])
                return
        self.append('','ClanList',name)

    def trackClan(self,clanname,data):
        temppath = os.path.join(adir,clanname).strip()
        if not os.path.exists(temppath):
            os.makedirs(temppath)
        u = Util()
        time = u.getGMTTime()
        self.write(clanname,str(time)+'.csv',data)
        pass

    def getWMostRecent(self):
        #TODO: Find value (either ID or name of ship) in expected value csv, and return associated dmg,frag, and WR data
        lst = []
        for file in os.listdir(wdir):
            if file.endswith('.csv'):
                lst.append(file)
        return max(lst)

    def getMostRecent(self,path):
        lst = []
        rpath = os.path.join(adir,path).strip()
        for file in os.listdir(rpath):
            if file.endswith('.txt') or file.endswith('.csv'):
                lst.append(file)
        if lst:
            t = max(lst)
        else:
            return None
        return t

    def getLatestbeforeDate(self,path,time):
        lst = []
        rpath = os.path.join(adir,path).strip()
        for file in os.listdir(rpath):
            if file.endswith('.csv'):
                if(int(file[:-4])<time):
                    lst.append(file)
        if lst:
            t = max(lst)
        else:
            return None
        return t

if(__name__=="__main__"):

    d = Data()
