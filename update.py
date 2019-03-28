import asyncio

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
        self.clanvals = {}

    #TODO:post data differences for players
    #TODO: Remake Update (Save Avg Dmg, WR, Battles Played, Spotting, Potential, Capping, PR and WTR)

    async def saveExpValues(self):
        dt = Data()
        api = API()

        temp = api.expectedValues()
        time = temp['time']

        out = []


        from concurrent.futures import ThreadPoolExecutor
        executor = ThreadPoolExecutor(max_workers=20)
        loop = asyncio.get_event_loop()

        futures = [loop.run_in_executor(executor, getPlayerData, clan, player) for player in players]
        await asyncio.wait(futures)

        for shipid,shipdata in temp['data'].items():
            lst = []
            lst.append(shipid)
            print(shipid) #this function takes a while so print ship ID's to keep us occupied. The dark is scary
            #print(shipdata)
            name = api.getShipName(shipid)
            if name is None:
                lst.append("None")
            else:
                lst.append(name)
            if(len(shipdata)!=0):
                lst.append(shipdata['average_damage_dealt'])
                lst.append(shipdata['average_frags'])
                lst.append(shipdata['win_rate'])
            out.append(lst)

        #print(out)
        dt.write('wowsnumbers',(str(time)+'.csv').strip(),out)
        return temp['data']

    async def saveStats(self):
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
            clan = str(clan).replace('[','')
            clan = str(clan).replace(']','')
            clan = str(clan).replace("'",'')
            print('Adding clan {}'.format(clan))
            self.clanvals[clan] = {
                'clanavgpr' : 0,
                'clanavgbt': 0,
                'clanavgdmg': 0,
                'clanavgkills': 0,
                'clanavgwr': 0,
                'clanavgspd': 0,
                'clanavgptd': 0
            }

            data2 = []
            data2.append([int(clanID)])
            data2.append([clanname])


            def getPlayerData(clan, player):
                data = []

                name = api.getPlayerName(player)
                pr = stats.PRcalculate(player)

                bt = api.getPlayerBattles(player)
                if(bt==0):
                    return

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

                self.clanvals[clan]['clanavgpr'] += pr
                self.clanvals[clan]['clanavgbt'] += bt
                self.clanvals[clan]['clanavgdmg'] += avgdmg
                self.clanvals[clan]['clanavgkills'] += avgkills
                self.clanvals[clan]['clanavgwr'] += avgwr
                self.clanvals[clan]['clanavgspd'] += avgspdmg
                self.clanvals[clan]['clanavgptd'] += avgptdmg


                temppath = str(clan)+"/"+str(name)
                filename = str(curtime)+".csv"

                print(temppath+" "+filename)
                print(data)
                dt.write(temppath,filename,data)

            if players is not None:
                print('getting {numb} players for {clan}'.format(
                    numb=len(players), clan=clan
                ))
                from concurrent.futures import ThreadPoolExecutor
                executor = ThreadPoolExecutor(max_workers=10)
                loop = asyncio.get_event_loop()

                futures = [loop.run_in_executor(executor, getPlayerData, clan, player) for player in players]
                await asyncio.wait(futures)
            print('**************')
            print('**************')
            print('**************')
            print('Clan: {}'.format(clan))
            print(self.clanvals[clan])


            print('**************')
            print('**************')




            # data2.append([float(clanavgpr / playernum)])
            # data2.append([int(clanavgbt / playernum)])
            # data2.append([float(clanavgdmg / playernum)])
            # data2.append([float(clanavgkills / playernum)])
            # data2.append([float(clanavgwr / playernum)])
            # data2.append([float(clanavgspd / playernum)])
            # data2.append([float(clanavgptd / playernum)])

            # dt.write(str(clan[0]),str(curtime)+".csv",data2)

        return 0

if(__name__=="__main__"):
    #sched = AsyncIOScheduler()
    #sched.start()
    #input('any key to exit')
    #while True:
        #time.sleep(10)
    u = Update()
    loop = asyncio.get_event_loop()
    # loop.run_until_complete(u.saveExpValues())

    loop.run_until_complete(u.saveStats())


    

#@sched.scheduled_job('cron', hour=4, minute=17, timezone='UTC')
#def scheduled_job():
#    u = Update()
#    u.saveExpValues()
#    u.saveStats()
#    t = Util()
#    print("Update Finished: "+str(t.getGMTTime()))
