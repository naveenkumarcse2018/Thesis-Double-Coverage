import numpy as np
import random
import NetworkFlow
from NetworkFlow import *
import csv
import pandas as pd

# Import writer class from csv module
from csv import writer

points = 0
latest_served_location=0

"""
This metric function will calucate the distance between two points on a cycle

"""


def metric(server, request):
    difference = abs(request-server)
    if difference > points/2:
        difference = points-difference

    return difference


"""
This class will implement Double Coverage algorithm on cycle
"""


class VirtualDoubleCoverage(object):
    def __init__(self, n, k, config,r):  # initialization of class object
        self.noOfServers = k          # total no.of servers
        self.points = n               # Points on cycle
        self.configuration = config   # Configuration of servers
        # True if server has virtual move
        self.vMove = [False for i in range(k)]
        self.vPosition = [config[i]
            for i in range(k)]  # virtual server positions
        # virtual server travelled distance
        self.vDistance = [0 for i in range(k)]
        self.latest_server=r

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
    def distance(self, server, request):
        # print("server ",server, "request ",request)
        difference = abs(request-server)
        # print("Actual distance is ",difference)
        if difference > self.points/2:
            difference = self.points-difference

        return difference

    """
        This function will take server id by which the request is server and changes the configurations
        and other needful updates. 
    """
    def makeUpdates(self, i, request):
        print("Request ",request ," is served by the server ",self.configuration[i])
        # print("BEFORE HERE---------------", self.latest_server)
        self.latest_server=self.configuration[i]
        # print("HERE------------------", self.latest_server)
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

    for t in range(10):
        print("\nTEST CASE ,", t+1)
        test_flag_count=0
        previous_request=-1
        request_sequence=list()
        # [6,13,17 ,15, 11,  8 ,20, 12 , 7,  1]#
        # print(type(latest_served_location))
        sequence = np.random.randint(1, n+1, 1)
        # print("NP RANDOM ",sequence)
        # print(type(sequence))
        latest_served_location=(int)(sequence)
        # print("Naveen ",latest_served_location)
        request_sequence.append(latest_served_location)
        initial = random.sample(range(1, n+1), k)  # [1, 3, 11]#
        # print(sequence)
        initial.sort()
        initial_configuration = list(initial)
        print("First,", initial_configuration)
        print("Request sequence: ", sequence)
        print("Initial configurations ", initial, initial_configuration)
        test = VirtualDoubleCoverage(n, k, initial,latest_served_location)
        points = n
        vCost = 0
        pCost = 0
        print()
        
        while True:
            # if previous_request==latest_served_location:
            #     test_flag_count+=1
            # else:
            #     test_flag_count=0
            #     previous_request=latest_served_location
            # if test_flag_count==15:
            #     break
            print("-----------------------------------------------")
            print("Request is -- ",latest_served_location)
            p, v = test.processRequest(latest_served_location)

            print("Physical configurations: ", test.configuration)
            print("Virtual configurations: ", test.vPosition)
            print("Virtual distance : ", test.vDistance)
            print("Virtual cost: ", v, " Physical cost: ",p)
            vCost += v
            pCost += p
            latest_served_location=test.latest_server
            request_sequence.append(latest_served_location)
            print("-----------------------------------------------\n")
            if len(request_sequence)==100:
                break
        # print(initial_configuration)
        print("Request sequence," ,request_sequence)
        # exit()
        opt = ServerSpace(metric)
        print("Second,", initial_configuration)
        opt.add_servers(initial_configuration)
        optimal_cost = opt.process_requests(request_sequence)[0]
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

        li = [vCost, pCost,optimal_cost,vCost/optimal_cost,pCost/optimal_cost,request_sequence]
        with open('dataset.csv','a') as csvfile:
            csvwriter=writer(csvfile)
            # csvwriter.writerow(fields)
            csvwriter.writerow(li)
            csvfile.close()
        print(len(request_sequence))

#[9, 11, 8, 10, 12, 8, 9, 9, 10, 10, 11, 11, 9, 10, 10, 11, 10, 9, 11, 9, 10, 11, 9, 10, 12, 9, 10, 11, 10, 10, 9, 9, 9, 9, 10, 8, 9, 9, 11, 10, 11, 10, 11, 10, 10, 9, 10, 11, 10, 9]
#First  [13, 14, 15]