class DoubleCoverage(object):

    def __init__(self, n, k, config):
        self.servers = k
        self.points = n
        self.config = config
        # is Virtual move for the server?
        self.vMove = [False for i in range(k)]
        self.vPosition = [-1 for i in range(k)]  # virtual move position if any
        # direction of virtual move (-1,0,1)
        self.vDirection = [0 for i in range(k)]

    def findTwoServers(self, request):
        rightServer = -1
        n = self.points
        k = self.servers
        if request == 1:
            for i in range(n, 0, -1):
                if i in self.config:
                    rightServer = i
                    break
        else:
            for i in range(request-1, 0, -1):
                if i in self.config:
                    rightServer = i
                    break
            if rightServer == -1:
                for i in range(n, request, -1):
                    if i == request:
                        break
                    if i in self.config:
                        rightServer = i
                        break
        leftServer = -1
        if request == n:
            for i in range(1, request-1, 1):
                if i in self.config:
                    leftServer = -1
                    break
        else:
            for i in range(request+1, n+1, 1):
                # print(i)
                if i in self.config:
                    leftServer = i
                    break
            if leftServer == -1:
                for i in range(1, request, 1):
                    if i in self.config:
                        leftServer = i
                        break

        # RIGHT server will move in clock-wise direction and LEFT server will move in anti-clock-wise direction
        return leftServer, rightServer

    def distance(self, request, server):
        difference = abs(request-server)
        # print("Actual distance is ",difference)
        if difference > self.points/2:
            difference = self.points-difference

        return difference

    def process_Request(self, request):
        n = self.servers
        if request in self.config:
            index = self.config.index(request)
            print("The server is at requested location")
            self.vMove[index] = False
            self.vDirection[index] = 0
            self.vPosition[index] = -1
            return 0
        leftS, rightS = self.findTwoServers(request)
        print("Left: ", leftS, " Right: ", rightS)
        index_l = self.config.index(leftS)
        index_r = self.config.index(rightS)

        # if (self.vMove[index_l] == True) and (self.vMove[index_r] == True):
        #     if self.vPosition[index_l] == request and self.vPosition[index_r] == request:
        #         # write code to move lower id server to requested locations and make updates
        #         # print()
        #     elif self.vPosition[index_l] == request:
        #         # write code to move left server and make updates
        #         print()
        #     elif self.vPosition[index_r] == request:
        #         # write code ro move right server and makeupdates
        #         print()

        # if there is any virtual moves for the servers then we need to take that positions to handle
        leftS = self.vPosition[index_l] if self.vMove[index_l] == True else leftS
        rightS = self.vPosition[index_r] if self.vMove[index_r] == True else rightS
        print("Left: ", leftS, " Right: ", rightS)
        # here check if the virtual servers is front of the requested location in same direction

        # distances
        dl = 0
        dr = 0
        while True:
            if rightS == n+1:
                rightS = 1
            if leftS == 0:
                leftS = self.points
            rightS += 1
            leftS -= 1
            dl += 1
            dr += 1
            if rightS == request and leftS == request:
                # check for the condition if virtual server and physical servers at same distance

                # Both are virtual and have equal distance
                if self.vMove[index_l] == True and self.vMove[index_r] == True:
                    # choose lower id server to replace
                    if self.config[index_l] < self.config[index_r]:
                        temp = self.config[index_l]
                        self.config[index_l] = request
                        self.vMove[index_l] = False
                        self.vPosition[index_l] = -1
                        self.vDirection[index_l] = 0  # Request Served

                        self.vPosition[index_r] = rightS
                        self.vDirection[index_r] = 1
                        print("Server ", temp, " served request ", request)
                        return self.distance(request, temp)
                    else:
                        temp = self.config[index_r]
                        self.config[index_r] = request
                        self.vMove[index_r] = False
                        self.vPosition[index_r] = -1
                        self.vDirection[index_r] = 0

                        self.vPosition[index_l] = leftS
                        self.vDirection[index_l] = -1

                        # distance between server and request
                        print("Server ", temp, " served request ", request)
                        return self.distance(request, temp)
                # right server is physical server and left side is virtual
                elif self.vMove[index_r] == False and self.vMove[index_l] == True:
                    temp = self.config[index_r]
                    self.config[index_r] = request
                    self.vMove[index_r] = False
                    self.vPosition[index_r] = -1
                    self.vDirection[index_r] = 0

                    self.vMove[index_l] = True
                    self.vPosition[index_l] = leftS
                    self.vDirection[index_l] = -1
                    print("Server ", temp, " served request ", request)
                    return self.distance(request, temp)
                # left server is physical and right server is virtual
                elif self.vMove[index_r] == True and self.vMove[index_l] == False:
                    temp = self.config[index_l]
                    self.config[index_l] = request
                    self.vMove[index_l] = False
                    self.vPosition[index_l] = -1
                    self.vDirection[index_l] = 0

                    self.vMove[index_r] = True
                    self.vPosition[index_r] = rightS
                    self.vDirection[index_l] = 1
                    print("Server ", temp, " served request ", request)

                    return self.distance(request, temp)
                # both are physical servers
                else:
                    if self.config[index_l] < self.config[index_r]:
                        temp = self.config[index_l]
                        self.config[index_l] = request
                        self.vMove[index_l] = False
                        self.vPosition[index_l] = -1
                        self.vDirection[index_l] = 0  # Request Served

                        self.vPosition[index_r] = rightS
                        self.vDirection[index_r] = 1
                        print("Server ", temp, " served request ", request)
                        return self.distance(request, temp)
                    else:
                        temp = self.config[index_r]
                        self.config[index_r] = request
                        self.vMove[index_r] = False
                        self.vPosition[index_r] = -1
                        self.vDirection[index_r] = 0

                        self.vPosition[index_l] = leftS
                        self.vDirection[index_l] = -1

                        # distance between server and request
                        print("Server ", temp, " served request ", request)
                        return self.distance(request, temp)

                # write code for moving lower id server and make updates and break
                print()
            elif rightS == request:
                # move right server to requested loction and make updates and break
                # if self.vMove[index_r]==True:
                temp = self.config[index_r]
                self.config[index_r] = request
                self.vMove[index_r] = False
                self.vPosition[index_r] = -1
                self.vDirection[index_r] = 0

                self.vMove[index_l] = True
                self.vDirection[index_l] = -1
                self.vPosition[index_l] = leftS
                print("Server ", temp, " served request ", request)
                return self.distance(request, temp)
                # else:

                # print()
            elif leftS == request:
                # move left server and make updates and break
                temp = self.config[index_l]
                self.config[index_l] = request
                self.vMove[index_l] = False
                self.vPosition[index_l] = -1
                self.vDirection[index_l] = 0

                self.vMove[index_r] = True
                self.vDirection[index_r] = 1
                self.vPosition[index_r] = rightS
                print("Server ", temp, " served request ", request)
                return self.distance(request, temp)
                # print()
            # print()
            # break


#
if __name__ == "__main__":
    n = 20
    k = 3
    config = [5, 9, 20]
    # request = 5
    obj = DoubleCoverage(n, k, config)
    # left, right = obj.findTwoServers(request)
    # print(left, "<-- ", request, "--> ", right)
    # print(obj.config.index(left))
    # print(obj.config.index(right))
    # print(obj.vDirection)
    # print(obj.vMove)
    # print(obj.vPosition)
    print("Initial configuration of the servers ", obj.config)
    requestSequence = [11, 1, 3, 7, 17, 4, 5, 6, 17, 4]
    cost = 0
    # print(obj.vMove[0])
    for i in range(len(requestSequence)):
        print("\n----------------------------------------------")
        # print("Request--",requestSequence[i])
        cost += (obj.process_Request(requestSequence[i]))

        print("\nConfiguration: ", obj.config, " Cost: ", cost)
        print("\nVirtual: ", obj.vMove)
        print("Positions: ", obj.vPosition)
        print("----------------------------------------------")
