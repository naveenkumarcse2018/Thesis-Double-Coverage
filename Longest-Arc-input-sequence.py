"""
	** Aamod Kore **
	Computer Science and Engineering,
	Indian Institute of Technology - Bombay.
	www.cse.iitb.ac.in/~aamod
	aamod[at]cse.iitb.ac.in
"""

import random
import sys

import VirtualDoubleCoverage
from VirtualDoubleCoverage import *

perim = 20
tests = 20


def c_metric(a, b):
    # a = 0 if not a else a % perim
    # b = 0 if not b else b % perim
    d = abs(b-a) #% perim
    if d > perim//2:
        return perim-d
    return d


def c_metric_mid(a, b):
    a = 0 if not a else a % perim
    b = 0 if not b else b % perim
    if a == b:
        return (a+perim//2) % perim
    d = (b-a) % perim
    return a+d//2


def generate(conf):
    n = len(conf)
    config = sorted(conf)
    maximum, ans = 0, 0
    for i in range(n):
        j = 0 if i == n-1 else i+1
        mid = c_metric_mid(config[i], config[j])
        dist = c_metric(config[i], mid)
        # print(config[i], config[j], mid, dist)
        if dist > maximum:
            maximum, ans = dist, mid
    return ans


if __name__ == "__main__":
    """Test case. Duh!"""
    ns = 5
    perim=20
    tests=150
    
    for t in range(10):
        request_sequence=[]
        vCost = 0
        pCost = 0
        print("TEST CASE: ",t)
        initial = random.sample(range(1,perim+1), ns)
        # initConfig = (0,0,0)
        initConfig = tuple(initial)
        initial_configuration = list(initial)
        print("Configuration ", initConfig)
        test = VirtualDoubleCoverage(perim,ns,list(initConfig))

        # print("Initial config:", end=" ")
        # for q in range(len(initial)) :
        # 	print(initial[q], end=" ")

        onlineCost = 0
        for i in range(tests):
            mid = generate(test.configuration)
            # wf.add_request(mid)
            request_sequence.append(mid)
            print("-----------------------------------------------")
            o=(i+1)%perim
            p, v = test.processRequest(o)

            print("Physical configurations: ", test.configuration)
            print("Virtual configurations: ", test.vPosition)
            print("Virtual distance : ", test.vDistance)
            print("Virtual cost: ", v, " Physical cost: ",p)
            vCost += v
            pCost += p
            print("-----------------------------------------------\n")

        print(request_sequence, "\n")
        print(len(request_sequence))
                # print(initial_configuration)
        # opt = ServerSpace(c_metric)
        # print("Second,", initial_configuration)
        # opt.add_servers(initial_configuration)
        # optimal_cost = opt.process_requests(request_sequence)[0]
        # # optimal_cost=1 if optimal_cost==0 else optimal_cost
        # print("Total physical cost: ", pCost)
        # print("Total virtual cost: ", vCost)
        # print("Optimal cost: ", optimal_cost)
        # pCost = 1 if pCost == 0 else pCost
        # vCost = 1 if vCost == 0 else vCost
        # optimal_cost = 1 if optimal_cost == 0 else optimal_cost
        # print("(Virtual ) Competitive ratio: ", vCost/optimal_cost)
        # print("(Physical ) Competitive ratio: ", pCost/optimal_cost)
        # print()
        li = [perim, ns,len(request_sequence),request_sequence]
        with open('Longest-Arc.csv','a') as csvfile:
            csvwriter=writer(csvfile)
            # csvwriter.writerow(fields)
            csvwriter.writerow(li)
            csvfile.close()
