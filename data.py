import numpy as np
import json
import csv
import os

tdir = "Data/testdata"
adir = "Data"

class Data():

    name = ''

    def __init__(self,inp):
        self.name = inp

    def testread(self,filename):
        rdarr = []
        with open(os.path.join(tdir,filename).strip(),'r') as r:
            rdarr = list(csv.reader(r,delimiter=','))
        return rdarr
 
    def testwrite(self,filename,output):
        with open(os.path.join(tdir,filename).strip(),'w+') as w:
            out = csv.writer(w)
            out.writerows(output)
    
    def read(self,filename):
        rdarr = []
        with open(os.path.join(adir,filename).strip(),'r') as r:
            rdarr = list(csv.reader(r,delimiter=','))
        return rdarr
 
    def write(self,filename,output):
        with open(os.path.join(adir,filename).strip(),'w+') as w:
            out = csv.writer(w)
            out.writerows(output)

    def find(self):
        #TODO: Find value (either ID or name of ship) in expected value csv, and return associated dmg,frag, and WR data
        pass


if(__name__=="__main__"):

    d = Data('MIA')
    d.testwrite('test1.csv',[['jacky','cool'],['jacky','smart']])
    c = d.testread('Book1.csv')
    print(c)
    for i in c:
        for z in i:
            print(z)
    print("done")
