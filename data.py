import numpy as np
import json
import csv
import os

#dir = "Data"

class Data():
    def __init__(self):
        pass


    def read(self,filename):
        with open(filename,'r') as f: #os.path.join(dir,filename).strip(),'r') as f:
            print(f)
            input = csv.reader(f,delimiter=',')
            print(input)
            for row in input:
                print(row)
                print(', '.join(row))
                print(input)



if(__name__=="__main__"):
    d = Data()
    d.read('Book1.csv')
    print("done")
