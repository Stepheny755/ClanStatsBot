import numpy as np
import json

from API import API
from data import Data
from update import Update

class Stats():
    def __init__(self):
        print("works")

    expected = []

    def calculatePR(self,dmg,kills,WR): #player): #player is an object of Player()

        #self.expectedWins = (self.expectedWR/100)*self.Battles
        #print(self.expectedWins)

        rDmg = dmg#/self.expectedDmg
        rWR = WR#/self.expectedWR
        rKills = kills#/self.expectedKills

        nDmg = max(0,(rDmg-0.4)/(1-0.4))
        nWR = max(0,(rWR-0.7)/(1-0.7))
        nKills = max(0,(rKills-0.1)/(1-0.1))

        return (700*nDmg + 300*nKills + 150*nWR)
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

    def getShipData(self,ID):
        data = self.pullExpectedData() #remove this in the future as to not overload wowsnumbers
        for ship in data:
            if(ship[0]==ID):
                return ship
            #print(ship)

if(__name__=="__main__"):
    #a = float(input("dmg: "))
    #b = float(input("kills: "))
    #c = float(input("wr: "))
    #d = Stats()
    #print(d.calculatePR(a,b,c))
    s = Stats()
    #u = Update()
    #d.saveExpValues()
    #dt = Data('test')
    #dt.write('wowsnumbers',str('test'+'.csv'),'test')
    #u.saveExpValues()
    #print(s.pullExpectedData())
    d=input("dmg:")
    wr=input("wr:")
    ak=input("avg kills:")
    print(s.calculatePR(d,ak,wr))
    #print(s.getShipData('4292818736'))
