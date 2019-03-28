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
        """
        Note: Test function, do not use

        Parameters:
        filename: name of file

        Returns:
        read data from file
        """
        rdarr = []
        with open(os.path.join(tdir,filename).strip(),'r') as r:
            rdarr = list(csv.reader(r,delimiter=','))
        return rdarr

    def testwrite(self,relativepath,filename,output):
        """
        Note: Test function, do not use

        Parameters:
        relativepath: path to write file to
        filename: name of file
        output: data to write
        """
        temppath = os.path.join(tdir,relativepath).strip()
        if not os.path.exists(temppath):
            os.makedirs(temppath)
        with open(os.path.join(temppath,filename).strip(),'w+') as w:
            out = csv.writer(w)
            out.writerows(output)

    def read(self,relativepath,filename):
        """
        Used for CSV files (majority of files in this project)

        Parameters:
        relativepath: path to read file from
        filename: name of file

        Returns:
        read data from file (lst)
        """
        rdarr = []
        temppath = os.path.join(adir,relativepath).strip()
        with open(os.path.join(temppath,filename).strip(),'r') as r:
            rdarr = list(csv.reader(r,delimiter=','))
        return rdarr

    def write(self,relativepath,filename,output):
        """
        Used for CSV files (majority of files in this project)

        Parameters:
        relativepath: path to read file from
        filename: name of file
        output: data to write
        """
        temppath = os.path.join(adir,relativepath).strip()
        if not os.path.exists(temppath):
            os.makedirs(temppath)
        with open(os.path.join(temppath,filename).strip(),'w+') as w:
            out = csv.writer(w)
            out.writerows(output)

    def readtxt(self,relativepath,filename):
        """
        Parameters:
        relativepath: path to read file from
        filename: name of file

        Returns:
        read data from file (lst)
        """
        rdarr = []
        temppath = os.path.join(adir,relativepath).strip()
        with open(os.path.join(temppath,filename).strip(),'r') as r:
            return r.read()

    def writetxt(self,relativepath,filename,output):
        """
        Parameters:
        relativepath: path to read file from
        filename: name of file
        output: data to write
        """
        temppath = os.path.join(adir,relativepath).strip()
        if not os.path.exists(temppath):
            os.makedirs(temppath)
        with open(os.path.join(temppath,filename).strip(),'w+') as w:
            w.write(str(output))

    def append(self,relativepath,filename,output):
        """
        Parameters:
        relativepath: path to read file from
        filename: name of file
        output: data to append
        """
        temppath = os.path.join(adir,relativepath).strip()
        if not os.path.exists(temppath):
            os.makedirs(temppath)
        with open(os.path.join(temppath,filename).strip(),'a+') as a:
            a.write(output+"\n")

# READ WRITE APPEND FUNCTIONS
# CLAN RELATED FUNCTIONS

    def addToClanlist(self,name):
        """
        Note: Clanlist dictates which clans are included in the update process

        Parameters:
        name: Name of clan

        - Adds clan to the clanlist
        """
        templist = self.read('','ClanList')
        for clanname in templist:
            if(clanname[0]==name):
                print(clanname[0])
                return
        self.append('','ClanList',name)

    def trackClan(self,clanname,data):
        """
        NO LONGER IN USE

        Parameters:
        clanname: Name of clan
        data: Data to store
        """
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
        """
        Returns:
        Most recemnt wowsnumbers expected value filename (str)
        """
        lst = []
        for file in os.listdir(wdir):
            if file.endswith('.csv'):
                lst.append(file)
        return max(lst)

    def getExpectedData(self):
        """
        Returns:
        Most recent expected value data from wowsnumbers (list of lists)
        """
        filename = self.getWMostRecent()
        file = self.read('wowsnumbers',filename)
        #print(file)
        return file

# WOWSNUMBERS FUNCTIONS
# SHIP RELATED FUNCTIONS

    def getShipID(self,name):
        """
        For some reason, WG api does not have a find ship ID by name

        Parameters:
        name: Name of ship

        Returns:
        WG ship ID (found via wowsnumbers data) (int)
        """
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

# SHIP RELATED FUNCTIONS
# SAVED STATS FUNCTIONS

    def getMostRecent(self,path):
        """
        Parameters:
        path: folder directory/path to look in

        Returns:
        filename (filename is unix time) (str)
        """
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

    def getLatestBeforeDate(self,path,time):
        """
        Looking for file that is the most recent but before param time

        Parameters:
        path: folder directory/path to look in
        time: latest time to look from

        Returns:
        filename (filename is unix time) (str)
        """
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
    #d.testwrite('test','test1.csv',[['jacky','cool'],['jacky','smart']])
    #c = d.testread('Book1.csv')
    #c = d.read("",'ClanList')
    #print(c)
    #for i in c:
        #for z in i:
            #print(z)
    #print("done")
    #print(d.getWMostRecent())
    print(d.getExpectedData())
    #print(d.trackClan('MIA',[['mod','shitter'],['ddak','absolut trash'],['warlord','legend']]))
    #d.addToClanlist('asdf')
    #print(d.read('','ClanList'))
    #print(d.getShipID("Dresden"))
    #print(d.getShipStats(d.getShipID("Alaska")))'
    ut = Util()
    print(d.getMostRecent("MIA-E/Modulatus"))
    print(d.getLatestBeforeDate("MIA-E/Modulatus",ut.countWeekSec()))
    print(d.read("MIA-E/Modulatus",d.getMostRecent("MIA-E/Modulatus/")))
    print(d.read("MIA-E/Modulatus",d.getLatestBeforeDate("MIA-E/Modulatus",ut.countWeekSec())))
    #data = [["wr",50.532],["avgdmg",203021],['kills',2],['pr',2410]]
    #d.testwrite("MIA/test",str(ut.getGMTTime())+'.csv',data)
