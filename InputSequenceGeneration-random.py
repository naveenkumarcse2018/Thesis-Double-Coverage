"""
This block of code is used to generate input sequence (random) with gaussian distribution 
"""
import numpy as np
import DoubleCoverage
from DoubleCoverage import *
class SequenceGeneration(object):
    def __init__(self, maximum, size):
        self.size = size
        self.maximum = maximum

    def generateSequence(self):
        sequence = np.random.randint(1, self.maximum, self.size)
        return sequence


if __name__ == "__main__":
    obj = SequenceGeneration(20, 10)
    requestSequence = obj.generateSequence()
    print(requestSequence)
    cost=0
    dc=DoubleCoverage(20,3,[1,5,20])
    requestTuple=[]
    for i in range(len(requestSequence)):
        requestTuple.append((requestSequence[i],0))
        print("\n----------------------------------------------")
        cost+=dc.process_Request(requestSequence[i])
        print("\nConfiguration: ",dc.config," Cost: ",cost)
        print("\nVirtual: ",dc.vMove)
        print("Positions: ",dc.vPosition)
        print("----------------------------------------------")
    print(requestTuple)

