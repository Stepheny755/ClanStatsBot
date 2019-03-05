import numpy as np
import json

from API import API
from data import Data
from update import Update

class Stats():
    def __init__(self):
        print("works")

    expected = []

    def PRnumerator(self):
        pass

    def PRdenominator(self):
        pass

    def PRratios(self,dmg,kills,WR,sID):
        d = Data()
        val = d.getShipStats(sID)
        rD = float(dmg/float(val[0]))
        rK = float(kills/float(val[1]))
        rWR = float(WR/float(val[2]))
        return rD,rK,rWR

    def PRnorm(self,dmg,kills,WR):
        nDmg = float(max(0,(dmg-0.4)/(1.0-0.4)))
        nWR = float(max(0,(WR-0.7)/(1.0-0.7)))
        nKills = float(max(0,(kills-0.1)/(1.0-0.1)))
        return nDmg,nKills,nWR

    def PRcalculate(self,playerID): #player PR calculation
        a = API()
        d = Data()

        data = a.getPlayerShipStats(playerID)
        for ship in data:
            print(ship)
            d = a.getShipDmg(ship)
            k = a.getShipKills(ship)
            w = a.getShipWins(ship)
            id = a.getShipID(ship)
        #return (700*dmg + 300*kills + 150*WR)
        pass

        #may need to save PR in update.py as the average PR of the partial values of all ships

    def pullExpectedData(self):
        dt = Data()
        api = API()

        file = dt.getExpectedData()
        val = []

        for i in file:
            val.append(i)

        self.expected = val
        return val

    def getServerAvg(self):
        data = self.pullExpectedData()
        count = 0
        tdg = 0.0 #total damage
        twr = 0.0 #total wr
        tkl = 0.0 #total avg kills
        for i in data:
            print(i)
            if(len(i)>3):
                count+=1
                tdg+=float("%.3f" % float(i[len(i)-3]))
                tkl+=float("%.3f" % float(i[len(i)-2]))
                twr+=float("%.3f" % float(i[len(i)-1]))
        print(tdg/count)
        print(tkl/count)
        print(twr/count)

        print(count)

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
    c = s.PRcalculate(a.getPlayerID("Modulatus"))
    print(c)

    #print(s.calculatePR(d,ak,wr))
    #print(s.getShipData('4292818736'))
    #print(s.getShipData(a.getShip))
