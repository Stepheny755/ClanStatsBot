import time

monthtime = 2592000
renametime = 1547524924


class Clan():

    def __init__(self):
        pass        





class Time():

    
    def __init__(self):
        pass

    def available(timezone):
        if(timezone=='EST'):
            temp = time.ctime(monthtime+renametime-5*3600)
        if(timezone=='PST'):
            temp = time.ctime(monthtime+renametime-8*3600)
        if(timezone=='UTC'):
            temp = time.ctime(monthtime+renametime)
        return temp
