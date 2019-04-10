import time,calendar
#TODO:
#Phone Number Processing (from (778) 800-6793 to +17788006793) (E164 Formatting)

class Util():
    def __init__(self): pass

    def GTimeToSec(self,a): return calendar.timegm(time.strptime(a))
    def SecToGTime(self,a): return time.asctime(time.gmtime(a))
    def getGMTTime(self): return int(calendar.timegm(time.gmtime())) #GMT == UTC
    def smaller(self,a,b): return a if a<b else b
    def larger(self,a,b): return a if a>b else b

    def daysToSec(self,num): return 24*60*60*num
    def secToDays(self,num): return num/(60*60*24)
    def countPreviousDays(self,days): return self.SecToGTime(self.getGMTTime()-self.daysToSec(days))
    def countWeekSec(self): return self.getGMTTime() - self.daysToSec(7)
    def countMonthSec(self):return self.getGMTTime() - self.daysToSec(30)

    def r3(self,input): return float(format(input,'.3f'))
    def r2(self,input): return float(format(input,'.2f'))
    def r1(self,input): return float(format(input,'.1f'))
    def ifPos(self,a): return ("+"+str(a)) if a>0 else (str(a))

    def countNL(self,txt): return txt.count('\n')
    def countLen(self,txt): return len(txt)

if(__name__=="__main__"):
    u = Util()
    print(u.SecToGTime(10000000000))
    print(u.ifPos(-124124))
    print(u.countPreviousDays(1))
    print(u.countNL("hi\nasdasd\nasd\n"))
