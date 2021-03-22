import csv
import pandas as pd

# Import writer class from csv module 
from csv import writer 

fields=['Sequence','VirtualDC-Cost','PhysicalCost','OptimalCost','Competitive-Ratio']
li=[[2,3,4,3,1,2,5,4,41,4],12,23,43,1.33]
with open('dataset.csv','a') as csvfile:
    csvwriter=writer(csvfile)
    # csvwriter.writerow(fields)
    csvwriter.writerow(li)
    csvfile.close()

