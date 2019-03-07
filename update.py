from data import Data
from API import API
from util import Util
from stats import Stats
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import time

class Update():

    def __init__(self):
        u = Util()
        print("Updated Started: "+str(u.getGMTTime()))

    #TODO:post data differences for players
    #TODO: Remake Update (Save Avg Dmg, WR, Battles Played, Spotting, Potential, Capping, PR and WTR)

    def saveExpValues(self):
        dt = Data()
        api = API()

        temp = api.expectedValues()
        time = temp['time']

        out = []
        for shipid,shipdata in temp['data'].items():
            lst = []
            lst.append(shipid)
            print(shipid) #this function takes a while so print ship ID's to keep us occupied. The dark is scary
            name = api.getShipName(shipid)
            if name is None:
                lst.append("None")
            else:
                lst.append(name)
            for key in shipdata:
                lst.append(shipdata[key])
            out.append(lst)

        #print(out)
        dt.write('wowsnumbers',(str(time)+'.csv').strip(),out)
        return temp['data']

    def saveStats(self):
        dt = Data()
        api = API()
        ut = Util()
        stats = Stats()

        curtime = ut.getGMTTime()
        clanlist = dt.read('','ClanList')

        for clan in clanlist:
            players = api.getClanMembers(api.getClanID(clan[0]))

            if players is not None:
                for player in players:

                    data = []

                    name = api.getPlayerName(player)
                    pr = stats.PRcalculate(player)

                    avgdmg = api.getPlayerAvgDmg(player)
                    avgwr = api.getPlayerAvgWR(player)
                    avgkills = api.getPlayerAvgKills(player)
                    avgspdmg = api.getPlayerAvgSpottingDmg(player)
                    avgptdmg = api.getPlayerAvgPotentialDmg(player)
                    # calculate avg dmg, wr,kills,

                    data.append(name)
                    data.append(ID)
                    data.append(pr)
                    data.append(avgdmg)
                    data.append(avgkills)
                    data.append(avgwr)

                    temppath = str(clan[0])+"/"+str(name)
                    filename = str(curtime)+".txt"
                    
                    print(temppath+" "+filename)
                    print(data)

                    #dt.writetxt(temppath,filename,stats)
        pass

if(__name__=="__main__"):
    #sched = AsyncIOScheduler()
    #sched.start()
    #input('any key to exit')
    #while True:
        #time.sleep(10)
    u = Update()
    #u.saveExpValues()
    u.saveStats()

#@sched.scheduled_job('cron', hour=4, minute=17, timezone='UTC')
#def scheduled_job():
#    u = Update()
#    u.saveExpValues()
#    u.saveStats()
#    t = Util()
#    print("Update Finished: "+str(t.getGMTTime()))
