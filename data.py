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

# INIT
# READ WRITE APPEND FUNCTIONS

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

    def readtxt(self,relativepath,filename):
        rdarr = []
        temppath = os.path.join(adir,relativepath).strip()
        with open(os.path.join(temppath,filename).strip(),'r') as r:
            return r.read()

    def writetxt(self,relativepath,filename,output):
        temppath = os.path.join(adir,relativepath).strip()
        if not os.path.exists(temppath):
            os.makedirs(temppath)
        with open(os.path.join(temppath,filename).strip(),'w+') as w:
            w.write(str(output))

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

# CLAN RELATED FUNCTIONS
# WOWSNUMBERS FUNCTIONS

    def getWMostRecent(self):
        #TODO: Find value (either ID or name of ship) in expected value csv, and return associated dmg,frag, and WR data
        lst = []
        for file in os.listdir(wdir):
            if file.endswith('.csv'):
                lst.append(file)
        return max(lst)

    def getExpectedData(self):
        filename = self.getWMostRecent()
        file = self.read('wowsnumbers',filename)
        #print(file)
        return file

# WOWSNUMBERS FUNCTIONS
# SHIP RELATED FUNCTIONS

    def getShipID(self,name):
        data = self.getExpectedData()
        for ship in data:
            if(ship[1]==name):
                return int(ship[0].strip())
        return None

    def getShipStats(self,sID):
        data = self.getExpectedData()
        for ship in data:
            if(int(ship[0])==sID and len(ship)>2):
                #print(ship[1])
                return ship[len(ship)-3],ship[len(ship)-2],ship[len(ship)-1]

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

if(__name__=="__main__"):

    d = Data()
    #d.testwrite('test','test1.csv',[['jacky','cool'],['jacky','smart']])
    #c = d.testread('Book1.csv')
    #c = d.read("",'ClanList')
    #print(c)
    #for i in c:
        #for z in i:
            #print(z)
    #print("done")
    #print(d.getWMostRecent())
    #print(d.getExpectedData())
    #print(d.trackClan('MIA',[['mod','shitter'],['ddak','absolut trash'],['warlord','legend']]))
    #d.addToClanlist('asdf')
    #print(d.read('','ClanList'))
    #print(d.getShipID("Dresden"))
    #print(d.getShipStats(d.getShipID("Alaska")))'
    ut = Util()
    data = [["wr",50.532],["avgdmg",203021],['kills',2],['pr',2410]]
    d.testwrite("MIA/test",str(ut.getGMTTime())+'.csv',data)
