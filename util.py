import numpy as np
import time,calendar


#Throw all the miscellaneous functions in here
class Util():
    def __init__(self):
        pass

    def GTimeToSec(self,a):
        t = time.strptime(a)
        return calendar.timegm(t)

    def SecToGTime(self,a):
        t = time.gmtime(a)
        return time.asctime(t)

    def getGMTTime(self): #GMT == UTC
        return int(calendar.timegm(time.gmtime()))

    def getEarlier(self,a,b):
        return a if a<b else b

    def getLater(self,a,b):
        return a if a>b else b


    def dToS(self,num):
        return 24*60*60*num

    def sToD(self,num):
        return num/(60*60*24)

    def countPreviousDays(self,days):
        curtime = self.getGMTTime()
        curtime -= self.dToS(days)
        return self.SecToGTime(curtime)

    def round3(self,input):
        return float(format(input,'.3f'))

    def round2(self,input):
        return float(format(input,'.2f'))

if(__name__=='__main__'):
    test = Util()
    print(test.countPreviousDays(test.dToS(7)))
    #print(test.sToD(134124))
    #print(test.countPreviousDays(7))
    #print(test.getLater(12322456,test.getGMTTime()))
    #a = calendar.timegm(time.gmtime())
    #print(a)
    #b = test.SecToGTime(a)
    #print(b)
    # b is GMT/UTC, and c is localtime (PST)
    #print()
    #print(time.ctime(a))
    #d = test.GTimeToSec(b)
    #print(d)
