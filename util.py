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
        if(a>b):
            return b
        else:
            return a

    def getLater(self,a,b):
        if(a>b):
            return a
        else:
            return b

if(__name__=='__main__'):
    test = Util()
    #print(test.getEarlier(123222222456,test.getGMTTime()))
    #a = calendar.timegm(time.gmtime())
    #print(a)
    #b = test.SecToGTime(a)
    #print(b)
    # b is GMT/UTC, and c is localtime (PST)
    #print()
    #print(time.ctime(a))
    #d = test.GTimeToSec(b)
    #print(d)
