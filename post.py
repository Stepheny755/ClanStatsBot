import asyncio

from data import Data
from API import API
from util import Util

class Post():

    def __init__(self):
        pass

    def clanReport(self,ID):
        dt = Data()
        api = API()
        ut = Util()
        stats = Stats()

        curtime = ut.getGMTTime()
        clanlist = dt.read('','ClanList')

    def getPlayerData(self,clanID):
        api = API()
        clantag = api.getClanTag(ID)
        players = api.getClanMembers(ID)
        if players is not None:
            for player in players:
                name = api.getPlayerName(player)

    def createEmbed(self,clantag,embed,start,end):
        api = API()
        d = Data()
        u = Util()
        players = api.getClanMembers(api.getClanID(clantag))
        print(players[start:])
        templen = 0
        if(end>len(players)):
            end = len(players)
        for i in players[start:end]:
            name = api.getPlayerName(i)
            bt = api.getPlayerBattles(i)
            if(bt==0):
                break
            rpath = str(clantag)+"/"+str(name)
            print(rpath)
            temp = d.read(rpath,d.getMostRecent(rpath))
            postname=api.getPlayerName(i)+"   (ID: "+str(i)+")"

            cur = []

            cur.append(u.round3(float(temp[2][0])))
            cur.append(int(temp[3][0]))
            cur.append(float(temp[4][0]))
            cur.append(float(temp[5][0]))
            cur.append(float(temp[6][0]))

            wdelta = self.getWeekDeltas(rpath)
            mdelta = self.getMonthDeltas(rpath)

            ret = self.formatString(cur,wdelta,mdelta)
            templen+=len(ret)
            print(len(ret))
            print(ret)
            #embed.add_field(name=postname,value=ret,inline=False) REMOVE COMMENT LATER


            #REMOVE COMMENT LATER




        print(templen)
        return embed

    def formatString(self,cur,wdelta,mdelta):
        u = Util()

        string = ""
        retp = "**PR:** "+str(cur[0])+" "
        retb = "**Battles:** "+str(cur[1])+" "
        retd = "**Avg Damage:** "+str(cur[2])+" "
        retk = "**Avg Kills:** "+str(cur[3])+" "
        retw = "**WR:** "+str(cur[4])+"%"

        temp =[retp,retb,retd,retk,retw]

        retwe = "W"
        retmo = "M"

        for i in range(5):
            if(len(wdelta)>0):
                retwe+=self.equalizeToString(temp[i],u.ifPos(wdelta[i]))+" "
            if(len(mdelta)>0):
                retmo+=self.equalizeToString(temp[i],u.ifPos(mdelta[i]))+" "

        string = retp+retb+retd+retk+retw+"\n```"
        if(len(retwe)>1):
            string += "\n" + retwe
            print(retwe)
        if(len(retmo)>1):
            string += "\n" + retmo
        string+="```"
        #print(string)
        return string
        #TODO:
        #make delta functions and cur array just ints/floats. That way you can manipulate them easier
        #add + for positive numbers
        #format string with spacing
    def getWeekDeltas(self,rpath):
        ut = Util()
        dt = Data()

        try:
            week = dt.read(rpath,dt.getLatestbeforeDate(rpath,ut.countWeekSec()))
            recent = dt.read(rpath,dt.getMostRecent(rpath))
        except:
            return []

        values = []

        values.append(ut.round3((float(recent[2][0])-float(week[2][0]))/7))
        values.append(ut.round2((int(recent[3][0])-int(week[3][0]))/7))
        values.append(ut.round2((float(recent[4][0])-float(week[4][0]))/7))
        values.append(ut.round3((float(recent[5][0])-float(week[5][0]))/7))
        values.append(ut.round3((float(recent[6][0])-float(week[6][0]))/7))

        return values

    def getMonthDeltas(self,rpath):
        ut = Util()
        dt = Data()

        try:
            month = dt.read(rpath,dt.getLatestbeforeDate(rpath,ut.countWeekSec()))
            recent = dt.read(rpath,dt.getMostRecent(rpath))
        except:
            return []

        values = []

        values.append(ut.round3((float(recent[2][0])-float(month[2][0]))/30))
        values.append(ut.round2((int(recent[3][0])-int(month[3][0]))/30))
        values.append(ut.round2((float(recent[4][0])-float(month[4][0]))/30))
        values.append(ut.round3((float(recent[5][0])-float(month[5][0]))/30))
        values.append(ut.round3((float(recent[6][0])-float(month[6][0]))/30))

        return values

    def getClanData(self,clanID):
        api = API()
        clantag = str(api.getClanTag(clanID))
        temp = d.getMostRecent(clantag)
        tempdata = d.read(clantag,str(temp))
        data = []
        for i in tempdata:
            val = float(i[0])
            data.append(val)
        return data

    def addSpace(self,string,num):
        ret = ""
        for i in range(num):
            ret += " "
        ret += string
        return ret

    def equalizeToString(self,s1,s2):
        len1 = int(len(s1)/2)
        len2 = len(s2)
        ret = self.addSpace(s2,len1-len2)
        return ret

if(__name__=="__main__"):
    d = Data()
    a = API()
    p = Post()
    #print(d.getMostRecent("MIA"))
    #print(p.getClanData(a.getClanID("MIA")))
    #print(p.equalizeToString("PR: 32","+0.339"))
    print(p.createEmbed("MIA-C",'',0,24))
