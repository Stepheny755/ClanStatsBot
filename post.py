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

    def createEmbed(self,clantag,embed):
        api = API()
        d = Data()
        u = Util()
        for i in api.getClanMembers(api.getClanID(clantag)):
            name = api.getPlayerName(i)
            bt = api.getPlayerBattles(i)
            if(bt==0):
                break
            rpath = str(clantag)+"/"+str(name)
            print(rpath)
            temp = d.read(rpath,d.getMostRecent(rpath))
            postname=api.getPlayerName(i)+"   (ID: "+str(i)+")"

            cur = []

            cur.append(str(u.round3(float(temp[2][0]))))
            cur.append(str(int(temp[3][0])))
            cur.append(str(float(temp[4][0])))
            cur.append(str(float(temp[5][0])))
            cur.append(str(float(temp[6][0])))

            wdelta = self.getWeekDeltas(rpath)
            mdelta = self.getMonthDeltas(rpath)

            ret = self.formatString(cur,wdelta,mdelta)

            embed.add_field(name=postname,value=ret,inline=False)
        return embed

    def formatString(self,cur,wdelta,mdelta):
        string = ""
        retp = "**PR:** "+cur[0]+" "
        retb = "**Battles:** "+cur[1]+" "
        retd = "**Avg Damage:** "+cur[2]+" "
        retk = "**Avg Kills:** "+cur[3]+" "
        retw = "**WR:** "+cur[4]+"%"

        ret = retp+retb+retd+retk+retw
        ret2 = wdelta[0]+wdelta[1]+wdelta[2]+wdelta[3]+wdelta[4]
        string = ret + "\n" + ret2

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

        values.append(str(ut.round3((float(recent[2][0])-float(week[2][0]))/7))+" ")
        values.append(str(ut.round2((int(recent[3][0])-int(week[3][0]))/7))+" ")
        values.append(str(ut.round2((float(recent[4][0])-float(week[4][0]))/7))+" ")
        values.append(str(ut.round3((float(recent[5][0])-float(week[5][0]))/7))+" ")
        values.append(str(ut.round3((float(recent[6][0])-float(week[6][0]))/7))+" ")

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

        values.append(str(ut.round3((float(recent[2][0])-float(month[2][0]))/30))+" ")
        values.append(str(ut.round2((int(recent[3][0])-int(month[3][0]))/30))+" ")
        values.append(str(ut.round2((float(recent[4][0])-float(month[4][0]))/30))+" ")
        values.append(str(ut.round3((float(recent[5][0])-float(month[5][0]))/30))+" ")
        values.append(str(ut.round3((float(recent[6][0])-float(month[6][0]))/30))+" ")

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


if(__name__=="__main__"):
    d = Data()
    a = API()
    p = Post()
    print(d.getMostRecent("MIA"))
    print(p.getClanData(a.getClanID("MIA")))
