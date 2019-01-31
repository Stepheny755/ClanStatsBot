import numpy as np
import json
import csv
import os

dir = "Data/testdata"

class Data():
    def __init__(self):
        pass


    def read(self,filename):
        with open(os.path.join(dir,filename).strip(),'r') as f:
            input = csv.reader(f,delimiter=',')
            for row in input:
                print(row)



if(__name__=="__main__"):
    d = Data()
    d.read('Book1.csv')
    print("done")
