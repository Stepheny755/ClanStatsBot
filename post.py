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
            temp = d.read(rpath,d.getMostRecent(rpath))
            postname=api.getPlayerName(i)+"   (ID: "+str(i)+")"

            PR = float(temp[2][0])
            print(PR)
            dmg = temp[4][0]
            bt = temp[3][0]
            k = temp[5][0]
            wr = temp[6][0]

            ret1 = "**PR:** "+str(u.round3(PR))+" **Battles:** "+bt+" **Avg Damage:** "+dmg+" **Avg Kills:** "+k+" **WR:** "+wr+"%"
            print(ret1)
            ret2 = "```diff\n +c +c \n-c +x```"
            ret = ret1+"\n"+ret2

            embed.add_field(name=postname,value=ret,inline=False)
        return embed

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
