"""
This block of code is used to generate input sequence (random) with gaussian distribution
"""
import numpy as np
import DoubleCoverage
from DoubleCoverage import *
import random
import NetworkFlow
from NetworkFlow import *
def metric(a, b):
    if a == None:
        if b == None:
            return 0
        else:
            return metric(b, a)
    if b != None:
        return metric((a[0]-b[0], a[1]-b[1]), None)
    else:
        return -a[0] if (a[0] < 0) else a[0]


class SequenceGeneration(object):
    def __init__(self, maximum, size):
        self.size = size
        self.maximum = maximum

    def generateSequence(self):
        sequence = np.random.randint(1, self.maximum, self.size)
        return sequence


if __name__ == "__main__":
    n = 20
    k = 3
    size = 10
    obj = SequenceGeneration(n, size)  # n=20,size=10
    requestSequence = obj.generateSequence()
    # print(requestSequence)
    cost = 0
    initial = random.sample(range(1,n), k)
    print("Initial config: ",initial)
    configNetworkFlow = []
    # print("N/F initial config: ",initial)
    #Configuration for NetWorkFlow
    for i in range(k):
        configNetworkFlow.append((initial[i], 0))
    dc = DoubleCoverage(20, 3, initial)

    requestTuple = []
    for i in range(len(requestSequence)):
        requestTuple.append((requestSequence[i], 0))
        print("\n----------------------------------------------")
        cost += dc.process_Request(requestSequence[i])
        print("\nConfiguration: ", dc.config, " Cost: ", cost)
        print("\nVirtual: ", dc.vMove)
        print("Positions: ", dc.vPosition)
        print("----------------------------------------------")

    print("\n\n")
   
    print(initial)
    print(configNetworkFlow)
    print(requestTuple)
    opt=ServerSpace(metric)
    opt.add_servers(configNetworkFlow)
    print(opt.process_requests(requestTuple))
