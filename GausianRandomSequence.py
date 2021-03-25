import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import math
import VirtualDoubleCoverage
from VirtualDoubleCoverage import *
import random
import NetworkFlow
from NetworkFlow import *
points = 0


def metric(server, request):
    # print("server ",server, "request ",request)
    difference = abs(request-server)
    # print("Actual distance is ",difference)
    if difference > points/2:
        difference = points-difference

    return difference


n = 100
k = 50
points = n
for t in range(10):
    print("\nTEST: ",t)
    r = np.random.normal(loc=10, scale=1, size=150)
    # print(r)
    sequence = [round(e) for e in r]
    sequence = [i if i> 0 and i <= n else n for i in sequence]
    print(sequence)
    initial = random.sample(range(1, n), k)  # [1, 3, 11]#
    initial.sort()
    initial_configuration = list(initial)
    print("First ",initial_configuration)
    test = VirtualDoubleCoverage(n, k, initial)
    # print(test.configuration)
    vCost = 0
    pCost = 0
    for r in sequence:
        p, v = test.processRequest(r)
        # print("-------------------------------------------------------")
        # print("Physical configurations: ", test.configuration)
        # print("Virtual configurations: ", test.vPosition)
        # print("Virtual distance : ", test.vDistance)
        # print("Virtual cost: ", v, " Physical cost: ", p)
        # print("-------------------------------------------------------\n")
        vCost += v
        pCost += p
    print(vCost, pCost)
    opt = ServerSpace(metric)
    print("Second",initial_configuration)
    opt.add_servers(initial_configuration)
    print(opt.servers)
    optimal_cost = opt.process_requests(sequence)[0]
    print("Total physical cost: ", pCost)
    print("Total virtual cost: ", vCost)
    print("Optimal cost: ", optimal_cost)
    print("(Virtual ) Competitive ratio: ", 1 if vCost ==
        optimal_cost else vCost/optimal_cost)
    print("(Physical ) Competitive ratio: ", 1 if pCost ==
        optimal_cost else pCost/optimal_cost)
    print()
    li=[vCost,pCost,optimal_cost,vCost/optimal_cost,pCost/optimal_cost,sequence]
    with open('dataset.csv','a') as csvfile:
        csvwriter=writer(csvfile)
        # csvwriter.writerow(fields)
        csvwriter.writerow(li)
        csvfile.close()
    print(len(sequence))
# print(sequence.count(10))
# print(sequence.count(9))
# print(sequence.count(8))
# print(sequence.count(11))
# print(sequence.count(12))
