import numpy as np
import json

from API import API
from data import Data
from update import Update

class Stats():
    def __init__(self):
        print("works")

    expectedDmg = 10587.423605547
    expectedWR = 46.05060493065
    expectedWins = 0
    expectedKills = 0.44863235747298

    def calculatePR(self,dmg,kills,WR): #player): #player is an object of Player()
        
        #self.expectedWins = (self.expectedWR/100)*self.Battles
        #print(self.expectedWins)

        rDmg = dmg/self.expectedDmg
        rWR = WR/self.expectedWR
        rKills = kills/self.expectedKills

        nDmg = max(0,(rDmg-0.4)/(1-0.4))
        nWR = max(0,(rWR-0.7)/(1-0.7))
        nKills = max(0,(rKills-0.1)/(1-0.1))

        return (700*nDmg + 300*nKills + 150*nWR)

    def pullExpectedData(self):
        dt = Data('test')
        api = API()

        file = dt.getExpectedData()

        for 
        print(file)

if(__name__=="__main__"):
    #a = float(input("dmg: "))
    #b = float(input("kills: "))
    #c = float(input("wr: "))
    #d = Stats()
    #print(d.calculatePR(a,b,c))
    s = Stats()
    u = Update()
    #d.saveExpValues()
    #dt = Data('test')
    #dt.write('wowsnumbers',str('test'+'.csv'),'test')
    #u.saveExpValues()
    s.pullExpectedData()
