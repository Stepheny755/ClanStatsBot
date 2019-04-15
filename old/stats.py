import numpy as np
import json

from API import API
from data import Data
from util import Util

class Stats():
    def __init__(self):
        print()

    expected = []

    def PRnormDmg(self,dmg,edmg):
        if(edmg!=0):
            dmg/=edmg
        else:
            return 0
        nDmg = float(max(0,(dmg-0.4)/(1.0-0.4)))
        return nDmg

    def PRnormWin(self,wins,ewins):
        if(ewins!=0):
            wins/=ewins
        else:
            return 0
        nWins = float(max(0,(wins-0.7)/(1.0-0.7)))
        return nWins

    def PRnormKil(self,kills,ekills):
        if(ekills!=0):
            kills/=ekills
        else:
            return 0
        nKills = float(max(0,(kills-0.1)/(1.0-0.1)))
        return nKills

    def calculateOverallPR(self,playerID): #player PR calculation
        a = API()
        d = Data()
        u = Util()

        eDmg = 0
        eWin = 0
        eKil = 0

        aDmg = 0
        aWin = 0
        aKil = 0

        btot = 0

        data = a.getPlayerShipStats(playerID)
        for shipdata in data:
            #print(shipdata)
            b = a.getShipBattles(shipdata)
            id = a.getShipID(shipdata)
            expectedstats = d.getShipStats(id)
            #print(expectedstats)

            if expectedstats is not None:
                eDmg += float(expectedstats[0]) * b
                eKil += float(expectedstats[1]) * b
                eWin += float(expectedstats[2]) * b/100

                aDmg += a.getShipDmg(shipdata)
                aKil += a.getShipKills(shipdata)
                aWin += a.getShipWins(shipdata)

                btot += b
            #print(b)
            #print(str(aWin))

        dmg = self.PRnormDmg(aDmg,eDmg)
        kills = self.PRnormKil(aKil,eKil)
        wins = self.PRnormWin(aWin,eWin)
        #print(str(dmg)+" "+str(kills)+" "+str(wins))
        return (700*dmg + 300*kills + 150*wins)

        #may need to save PR in update.py as the average PR of the partial values of all ships

    def calculateShipPR(self,playerID,shipID):
        a = API()
        d = Data()
        u = Util()

        data = a.getPlayerShipStats(playerID)
        print(data)

if(__name__=="__main__"):
    #a = float(input("dmg: "))
    #b = float(input("kills: "))
    #c = float(input("wr: "))
    #d = Stats()
    #print(d.calculatePR(a,b,c))
    s = Stats()
    #u = Update()
    d = Data()
    a= API()
    #u = Update()
    #s.getServerAvg()
    #d.saveExpValues()
    #dt = Data('test')
    #dt.write('wowsnumbers',str('test'+'.csv'),'test')
    #u.saveExpValues()
    #print(s.pullExpectedData())
    #d=float((46516/14102.207358134+14782/16015.896946565)/2)
    #wr=float((0/48.257995811777+100/51.231125954199)/2)
    #ak=float((2/0.70378500451673+2/0.72540076335877)/2)
    #print(a.getPlayerShipStats(a.getPlayerID("Modulatus"),d.getShipID("Dresden")))
    #a = s.PRratios(46516,2,0,d.getShipID("Dresden"))
    #a1 = s.PRratios(14782,2,100,d.getShipID("Diana"))
    #b = []
    #for i in range(3):
        #b.append(float((a[i]+a1[i])))
    #a = s.PRnorm(b[0],b[1],b[2])
    #a = s.PRnorm(1.44653083935,2.51747177976,1.24949075502)
    #a = s.PRnorm(b[0],b[1],b[2])
    #c = s.calculateOverallPR(a.getPlayerID("ddak26"))
    print(s.calculateShipPR(a.getPlayerID("Modulatus"),a.getShipID(a.getPlayerShipStats(a.getPlayerID("Modulatus")))))

    #print(s.calculatePR(d,ak,wr))
    #print(s.getShipData('4292818736'))
    #print(s.getShipData(a.getShip))
