from data import Data
from API import API
from util import Util
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import time

class Update():

    def __init__(self):
        u = Util()
        print("Updated Started: "+str(u.getGMTTime()))

    #TODO:post data differences for players

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

        curtime = ut.getGMTTime()

        clanlist = dt.read('','ClanList')

        for clan in clanlist:
            IDs = api.getClanMembers(api.getClanID(clan[0]))
            print(IDs)
            if IDs is not None:
                for player in IDs:
                    name = api.getPlayerName(player)
                    stats = api.getPlayerStats(player)

                    temppath = str(clan[0])+"/"+str(name)
                    filename = str(curtime)+".txt"
                    print(temppath+" "+filename)
                    print(stats)

                    dt.writetxt(temppath,filename,stats)

if(__name__=="__main__"):
    sched = AsyncIOScheduler()
    sched.start()
    input('any key to exit')
    #while True:
        #time.sleep(10)
    #u.saveExpValues()
    #u.saveStats()

#@sched.scheduled_job('cron', hour=4, minute=17, timezone='UTC')
#def scheduled_job():
#    u = Update()
#    u.saveExpValues()
#    u.saveStats()
#    t = Util()
#    print("Update Finished: "+str(t.getGMTTime()))
