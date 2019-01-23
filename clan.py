import time

class Clan():

    def __init__(self):
        pass        

class Time():

    monthtime = 2592000
    renametime = 1547524924

    def __init__(self):
        pass

    def available(timezone):
        if(timezone=='EST'):
            temp = time.ctime(monthtime+renametime-5*3600)
        if(timezone=='PST'):
            temp = time.ctime(monthtime+renametime-8*3600)

    def available():
        temp = time.ctime(monthtime+renametime)
        return temp
