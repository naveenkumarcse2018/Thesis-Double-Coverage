import numpy as np
import random
import NetworkFlow
from NetworkFlow import *
import csv
import pandas as pd

# Import writer class from csv module 
from csv import writer 

points=0
def metric(server, request):
    # print("server ",server, "request ",request)
    difference = abs(request-server)
    # print("Actual distance is ",difference)
    if difference > points/2:
        difference = points-difference

    return difference


class VirtualDoubleCoverage(object):
    def __init__(self, n, k, config):
        self.noOfServers = k
        self.points = n
        self.configuration = config
        self.vMove = [False for i in range(k)]
        self.vPosition = [config[i] for i in range(k)]
        self.vDistance = [0 for i in range(k)]

    def findTwoServers(self, request):
        rightServer = -1
        n = self.points
        k = self.noOfServers
        if request == 1:
            for i in range(n, 0, -1):
                if i in self.configuration:
                    rightServer = i
                    break
        else:
            for i in range(request-1, 0, -1):
                if i in self.configuration:
                    rightServer = i
                    break
            if rightServer == -1:
                for i in range(n, request, -1):
                    if i == request:
                        break
                    if i in self.configuration:
                        rightServer = i
                        break
        leftServer = -1
        if request == n:
            for i in range(1, request-1, 1):
                if i in self.configuration:
                    leftServer = i
                    break
        else:
            for i in range(request+1, n+1, 1):
                # print(i)
                if i in self.configuration:
                    leftServer = i
                    break
            if leftServer == -1:
                for i in range(1, request, 1):
                    if i in self.configuration:
                        leftServer = i
                        break

        # RIGHT server will move in clock-wise direction and LEFT server will move in anti-clock-wise direction
        return leftServer, rightServer

    def findTwoVirtualServers(self, request):
        # print("Request has ",request)
        rightServer = -1
        n = self.points
        k = self.noOfServers
        if request == 1:
            for i in range(n, 0, -1):
                if i in self.vPosition:
                    rightServer = i
                    break
        else:
            for i in range(request-1, 0, -1):
                if i in self.vPosition:
                    rightServer = i
                    break
            if rightServer == -1:
                for i in range(n, request-1, -1):
                    if i == request:
                        break
                    if i in self.vPosition:
                        rightServer = i
                        break
        leftServer = -1
        if request == n:
            # print("Naveen")
            for i in range(1, request-1, 1):
                if i in self.vPosition:
                    leftServer = i
                    break
        else:
            for i in range(request+1, n+1, 1):
                # print(i)
                if i in self.vPosition:
                    leftServer = i
                    break
            if leftServer == -1:
                for i in range(1, request, 1):
                    if i in self.vPosition:
                        leftServer = i
                        break

        # RIGHT server will move in clock-wise direction and LEFT server will move in anti-clock-wise direction
        return leftServer, rightServer

    def distance(self, server, request):
        # print("server ",server, "request ",request)
        difference = abs(request-server)
        # print("Actual distance is ",difference)
        if difference > self.points/2:
            difference = self.points-difference

        return difference

    def makeUpdates(self, i, request):
        # print("Server ", self.configuration[i],
            #   " is moved to requeste location ", request)
        self.configuration[i] = request
        self.vMove[i] = False
        self.vPosition[i] = self.configuration[i]
        self.vDistance[i] = 0

    def processRequest(self, request):
        n = self.points
        # physical server is at requested location but not having any virtual move
        if request in self.configuration and self.vMove[self.configuration.index(request)] == False:
            index = self.configuration.index(request)
            # print("Requested Location has server ")
            self.makeUpdates(index, request)
            
            return 0, 0
        elif request in self.vPosition:  # If the virtual servers at requested location
            # if two are more virtual servers at location then serve with lower id
            # print("Requested Locations has virtual server")
            if self.vPosition.count(request) > 1:
                ind = self.vPosition.index(request)
                server_id = self.configuration[ind]
                index = ind
                for i in range(ind+1, self.noOfServers):
                    if server_id > self.configuration[i]:
                        server_id = self.configuration[i]
                        index = i
                temp_config = list(self.configuration)
                virtual_cost = self.vDistance[index]
                self.makeUpdates(index, request)
                # for physical cost of the server
                physical_cost = self.distance(temp_config[index], request)
                return physical_cost, virtual_cost
            else:
                index = self.vPosition.index(request)
                temp_config = list(self.configuration)
                virtual_cost = self.vDistance[index]
                self.makeUpdates(index, request)
                physical_cost = self.distance(temp_config[index], request)
                return physical_cost, virtual_cost
        else:
            leftS, rightS = self.findTwoVirtualServers(request)
            # print("Right ",rightS, " left ",leftS)
            # print(self.vPosition)
            left_index = self.vPosition.index(leftS)
            right_index = self.vPosition.index(rightS)

            # if any virtual moves
            leftS = leftS if self.vMove[left_index] == False else self.vPosition[left_index]
            rightS = rightS if self.vMove[right_index] == False else self.vPosition[right_index]

            leftS_distance = self.vDistance[left_index]
            rightS_distance = self.vDistance[right_index]
            
            # print("Right ",rightS, " left ",leftS)

            while True:
                # print("In while loop ",rightS , " points ",n)

                rightS = rightS+1
                leftS -= 1
                if rightS == n+1:
                    # print("Naveen Kumar")
                    rightS = 1
                if leftS == 0:
                    leftS = n
                # print("Updated----Right ",rightS, " left ",leftS)
                leftS_distance += 1
                rightS_distance += 1
                # print("Updated----Right ",rightS_distance, " left ",leftS_distance)

                # if both servers are reached requested location
                if rightS == request and leftS == request:
                    # print("YESSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
                    # right server is smaller id
                    if self.configuration[right_index] < self.configuration[left_index]:
                        temp_config = list(self.configuration)
                        virtual_cost = rightS_distance
                        self.makeUpdates(right_index, request)
                        physical_cost = self.distance(
                            temp_config[right_index], request)
                        self.vDistance[left_index] = leftS_distance
                        self.vPosition[left_index] = leftS
                        self.vMove[left_index] = True
                        return physical_cost, virtual_cost
                    else:
                        temp_config = list(self.configuration)
                        virtual_cost = leftS_distance
                        self.makeUpdates(left_index, request)
                        physical_cost = self.distance(
                            temp_config[left_index], request)
                        self.vDistance[right_index] = rightS_distance
                        self.vPosition[right_index] = rightS
                        self.vMove[right_index] = True
                        return physical_cost, virtual_cost

                elif rightS == request:  # if right virtual server reached first
                    temp_config = list(self.configuration)
                    virtual_cost = rightS_distance
                    self.makeUpdates(right_index, request)
                    physical_cost = self.distance(
                        temp_config[right_index], request)
                    self.vDistance[left_index] = leftS_distance
                    self.vPosition[left_index] = leftS
                    self.vMove[left_index] = True
                    return physical_cost, virtual_cost
                elif leftS == request:  # if left server reaches first
                    # print("Left here ")
                    # print(rightS_distance)
                    # print("Right server ", rightS)
                    temp_config = list(self.configuration)
                    virtual_cost = leftS_distance
                    # print("Naveen ",temp_config)
                    self.makeUpdates(left_index, request)
                    # print("Anil , ", temp_config)
                    physical_cost = self.distance(
                        temp_config[left_index], request)
                    self.vDistance[right_index] = rightS_distance
                    self.vPosition[right_index] = rightS
                    self.vMove[right_index] = True
                    return physical_cost, virtual_cost


if __name__ == "__main__":
    n = 20
    k = 3
    # obj = VirtualDoubleCoverage(10, 2, [1, 8])
    # print(obj.noOfServers)
    # print(obj.points)
    # print(obj.configuration)
    # print(obj.vMove)
    # print(obj.vPosition)
    # print(obj.vDistance)
    # request = 5
    # leftS, rightS = obj.findTwoServers(request)
    # print(leftS, "<--- ", request, " --->", rightS)
    # print("-------------------------------")
    # print(obj.configuration)
    # print("Cost: ",obj.processRequest(request))
    # print(obj.configuration, obj.vPosition)
    # print("Cost: ",obj.processRequest(2))
    # print(obj.configuration, obj.vPosition)
    # print("-----------------------------------")

    # # np.random.randint(1, n, 10)
    # sequence = [18,  6,  9, 12,  3,  2,  7,  8, 17,  6]#np.random.randint(1, n, 10)#[4,13,10,15,3,16,3,7,18]##[13, 8, 14, 9, 17, 15, 17, 15, 1, 2]
    # initial = [1, 13, 18]#random.sample(range(1, n), k)#[1,9,12]##[1, 5, 11]  # 


    n = 20
    k = 3
    for t in range(1):
        print("\nTEST CASE ,",t+1)
        sequence=np.random.randint(1,n+1,10)#[6,13,17 ,15, 11,  8 ,20, 12 , 7,  1]#
        initial=random.sample(range(1,n),k)#[1, 3, 11]#
        initial.sort()
        initial_configuration = list(initial)
        print("Request sequence: ", sequence)
        print("Initial configurations ", initial, initial_configuration)
        test = VirtualDoubleCoverage(n, k, initial)
        points=n
        vCost = 0
        pCost = 0
        print()
        for i in range(len(sequence)):
            # print("-----------------------------------------------")
            p, v = test.processRequest(sequence[i])

            # print("Physical configurations: ", test.configuration)
            # print("Virtual configurations: ", test.vPosition)
            # print("Virtual distance : ",test.vDistance)
            # print("Virtual cost: ",v," Physical cost: ",p)
            vCost += v
            pCost += p
            # print("-----------------------------------------------\n")
        # print(initial_configuration)
        opt = ServerSpace(metric)
        opt.add_servers(initial_configuration)
        optimal_cost=opt.process_requests(sequence)[0]
        print("Total physical cost: ", pCost)
        print("Total virtual cost: ", vCost)
        print("Optimal cost: ",optimal_cost)
        print("(Virtual ) Competitive ratio: ", 1 if vCost==optimal_cost else vCost/optimal_cost)
        print("(Physical ) Competitive ratio: ", 1 if pCost==optimal_cost else  pCost/optimal_cost)
        print()
        #fields=['VirtualDC-Cost','PhysicalCost','OptimalCost','vCost/OPT','pCost/OPT,'Sequence']
        # li=[vCost,pCost,optimal_cost,vCost/optimal_cost,pCost/optimal_cost,sequence]
        # with open('dataset.csv','a') as csvfile:
        #     csvwriter=writer(csvfile)
        #     # csvwriter.writerow(fields)
        #     csvwriter.writerow(li)
        #     csvfile.close()
        # print(len(sequence))

