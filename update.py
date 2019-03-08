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

            clanID = api.getClanID(clan[0])
            clanname = api.getClanTag(clanID)
            playernum = len(players)
            clanavgpr = 0.0
            clanavgbt = 0
            clanavgdmg = 0.0
            clanavgkills = 0.0
            clanavgwr = 0.0
            clanavgspd = 0.0
            clanavgptd = 0.0

            data2 = []
            data.append([int(clanID)])
            data.append([clanname])

            if players is not None:
                for player in players:

                    data = []

                    name = api.getPlayerName(player)
                    pr = stats.PRcalculate(player)

                    bt = api.getPlayerBattles(player)
                    if(bt==0):
                        break

                    avgdmg = api.getPlayerAvgDmg(player)
                    avgwr = api.getPlayerAvgWR(player)
                    avgkills = api.getPlayerAvgKills(player)
                    avgspdmg = api.getPlayerAvgSpottingDmg(player)
                    avgptdmg = api.getPlayerAvgPotentialDmg(player)
                    # calculate avg dmg, wr,kills,

                    data.append([name])
                    data.append([player])
                    data.append([pr])
                    data.append([bt])
                    data.append([avgdmg])
                    data.append([avgkills])
                    data.append([avgwr])
                    data.append([avgspdmg])
                    data.append([avgptdmg])

                    clanavgpr += pr
                    clanavgbt += bt
                    clanavgdmg += avgdmg
                    clanavgkills += avgkills
                    clanavgwr += avgwr
                    clanavgspd += avgspdmg
                    clanavgptd += avgptdmg

                    temppath = str(clan[0])+"/"+str(name)
                    filename = str(curtime)+".csv"

                    print(temppath+" "+filename)
                    print(data)
                    dt.write(temppath,filename,data)

            data2.append([float(clanavgpr / playernum)])
            data2.append([int(clanavgbt / playernum)])
            data2.append([float(clanavgdmg / playernum)])
            data2.append([float(clanavgkills / playernum)])
            data2.append([float(clanavgwr / playernum)])
            data2.append([float(clanavgspd / playernum)])
            data2.append([float(clanavgptd / playernum)])

            dt.write(str(clan[0]),str(curtime)+".csv",data2)

        return 0

if(__name__=="__main__"):
    #sched = AsyncIOScheduler()
    #sched.start()
    #input('any key to exit')
    #while True:
        #time.sleep(10)
    u = Update()
    u.saveExpValues()
    u.saveStats()

#@sched.scheduled_job('cron', hour=4, minute=17, timezone='UTC')
#def scheduled_job():
#    u = Update()
#    u.saveExpValues()
#    u.saveStats()
#    t = Util()
#    print("Update Finished: "+str(t.getGMTTime()))
