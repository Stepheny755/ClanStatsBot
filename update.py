from data import Data
from API import API

class Update():
    def saveExpValues(self):
        dt = Data('test')
        api = API()

        temp = api.expectedValues()
        time = temp['time']

        out = []
        for shipid,shipdata in temp['data'].items():
            lst = []
            lst.append(shipid)
            print(shipid) #this function takes a while so print ship ID's to keep us occupied. The dark is scary
            name = api.getShipName(shipid)
            if name is not None:
                lst.append(name)
            for key in shipdata:
                lst.append(shipdata[key])
            out.append(lst)

        #print(out)
        dt.write('wowsnumbers',(str(time)+'.csv').strip(),out)
        return temp['data']

if(__name__=="__main__"):
    u = Update()
    u.saveExpValues()
