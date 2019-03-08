from data import Data
from API import API
from util import Util

class Post():

    def __init__(self):
        pass

    def clanReport(self,ID):
        dt = Data()
        api = API()
        ut = Util()
        stats = Stats()

        curtime = ut.getGMTTime()
        clanlist = dt.read('','ClanList')
        


if(__name__=="__main__"):
    d = Data()
