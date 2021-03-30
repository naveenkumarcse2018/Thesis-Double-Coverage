import numpy as np
import random
import NetworkFlow
from NetworkFlow import *
import csv
import pandas as pd

# Import writer class from csv module
from csv import writer

points = 0

"""
This metric function will calucate the distance between two points on a cycle

"""


def metric(a, b):
    # a = 0 if not a else a % points
    # b = 0 if not b else b % points
    d = abs(b-a) #% points
    if d > points//2:
        return points-d
    return d


"""
This class will implement Double Coverage algorithm on cycle
"""


class VirtualDoubleCoverage(object):
    def __init__(self, n, k, config):  # initialization of class object
        self.noOfServers = k          # total no.of servers
        self.points = n               # Points on cycle
        self.configuration = config   # Configuration of servers
        # True if server has virtual move
        self.vMove = [False for i in range(k)]
        self.vPosition = [config[i] for i in range(k)]  # virtual server positions
        # virtual server travelled distance
        self.vDistance = [0 for i in range(k)]

    """
        This function takes a point (requested location) and returns the two servers in which the request
        is placed. We say these two servers as left and right servers.
    """

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


    """
    This function takes a requested location and returns two virtual servers which
    right and left side of the request. (The request will be between these two servers)
    """

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

    # Calculates distance between two points
    def distance(self, a, b):
        # # print("server ",server, "request ",request)
        # difference = abs(request-server)
        # # print("Actual distance is ",difference)
        # if difference > self.points/2:
        #     difference = self.points-difference

        # return difference
        # a = 0 if not a else a % self.points
        # b = 0 if not b else b % self.points
        d = abs(b-a) #% self.points
        if d > self.points//2:
            return self.points-d
        return d

    """
        This function will take server id by which the request is server and changes the configurations
        and other needful updates. 
    """
    def makeUpdates(self, i, request):
        print("Request ",request ," is served by the server ",self.configuration[i])
        self.configuration[i] = request
        self.vMove[i] = False
        self.vPosition[i] = self.configuration[i]
        self.vDistance[i] = 0

    """
        This processRequest function will take a request and serves it using Double Coverage algorithm.

    """

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
            print("Requested Locations has virtual server")
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
            prev_r=rightS
            prev_l=leftS
            # print("Right ",rightS, " left ",leftS)

            while True:
                # print("In while loop ",rightS , " points ",n)
                prev_r=rightS
                prev_l=leftS
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
                        leftS_distance-=1
                        leftS=prev_l
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
                        rightS_distance-=1
                        rightS=prev_r
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
                elif leftS-1==request and rightS+1==request:
                    print("----------Both servers are at same distance---->")
                    # if leftS-1==request and rightS+1==request:
                    if self.configuration[right_index] < self.configuration[left_index]:
                        temp_config = list(self.configuration)
                        rightS_distance+=1
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
                        leftS_distance+=1
                        virtual_cost = leftS_distance
                        self.makeUpdates(left_index, request)
                        physical_cost = self.distance(
                            temp_config[left_index], request)
                        self.vDistance[right_index] = rightS_distance
                        self.vPosition[right_index] = rightS
                        self.vMove[right_index] = True
                        return physical_cost, virtual_cost
                    # elif leftS-1==request:
                    #     temp_config = list(self.configuration)
                    #     leftS_distance+=1
                    #     virtual_cost = leftS_distance
                    #     # print("Naveen ",temp_config)
                    #     self.makeUpdates(left_index, request)
                    #     # print("Anil , ", temp_config)
                    #     physical_cost = self.distance(
                    #         temp_config[left_index], request)
                    #     self.vDistance[right_index] = rightS_distance
                    #     self.vPosition[right_index] = rightS
                    #     self.vMove[right_index] = True
                    #     return physical_cost, virtual_cost
                    # else:
                    #     temp_config = list(self.configuration)
                    #     rightS_distance+=1
                    #     virtual_cost = rightS_distance
                    #     self.makeUpdates(right_index, request)
                    #     physical_cost = self.distance(
                    #         temp_config[right_index], request)
                    #     self.vDistance[left_index] = leftS_distance
                    #     self.vPosition[left_index] = leftS
                    #     self.vMove[left_index] = True
                    #     return physical_cost, virtual_cost



if __name__ == "__main__":
    n = 20
    k = 3
    for t in range(1):
        print("\nTEST CASE ,", t+1)
        # [6,13,17 ,15, 11,  8 ,20, 12 , 7,  1]#
        sequence = np.random.randint(1, n+1, 15)
        initial =random.sample(range(1, n+1), k)  #[13, 14, 15]#[5, 8, 10, 12, 14]#[7, 8, 17,18,20]#random.sample(range(1, n+1), k)  # [1, 3, 11]#
        # print(sequence)
        initial.sort()
        initial_configuration = list(initial)
        print("First,", initial_configuration)
        print("Request sequence: ", sequence)
        print("Initial configurations ", initial, initial_configuration)
        test = VirtualDoubleCoverage(n, k, initial)
        points = n
        vCost = 0
        pCost = 0
        # print(type(sequence[0]))
        # exit()
        print()
        for i in range(len(sequence)):
            print("-----------------------------------------------")
            p, v = test.processRequest(sequence[i])

            print("Physical configurations: ", test.configuration)
            print("Virtual configurations: ", test.vPosition)
            print("Virtual distance : ", test.vDistance)
            print("Virtual cost: ", v, " Physical cost: ",p)
            vCost += v
            pCost += p
            print("-----------------------------------------------\n")
        # print(initial_configuration)
        opt = ServerSpace(metric)
        print("Second,", initial_configuration)
        opt.add_servers(initial_configuration)
        optimal_cost = opt.process_requests(sequence)[0]
        # optimal_cost=1 if optimal_cost==0 else optimal_cost
        print("Total physical cost: ", pCost)
        print("Total virtual cost: ", vCost)
        print("Optimal cost: ", optimal_cost)
        pCost = 1 if pCost == 0 else pCost
        vCost = 1 if vCost == 0 else vCost
        optimal_cost = 1 if optimal_cost == 0 else optimal_cost
        print("(Virtual ) Competitive ratio: ", vCost/optimal_cost)
        print("(Physical ) Competitive ratio: ", pCost/optimal_cost)
        print()
        # fields=['VirtualDC-Cost','PhysicalCost','OptimalCost','vCost

        li = [vCost, pCost,optimal_cost,vCost/optimal_cost,pCost/optimal_cost,sequence]
        # with open('special-Case.csv','a') as csvfile:
        #     csvwriter=writer(csvfile)
        #     # csvwriter.writerow(fields)
        #     csvwriter.writerow(li)
        #     csvfile.close()
        print(len(sequence))

#[9, 11, 8, 10, 12, 8, 9, 9, 10, 10, 11, 11, 9, 10, 10, 11, 10, 9, 11, 9, 10, 11, 9, 10, 12, 9, 10, 11, 10, 10, 9, 9, 9, 9, 10, 8, 9, 9, 11, 10, 11, 10, 11, 10, 10, 9, 10, 11, 10, 9]
#First  [13, 14, 15]