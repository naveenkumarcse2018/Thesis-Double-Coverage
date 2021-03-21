class VirtualDoubleCoverage(object):
    def __init__(self, n, k, config):
        self.noOfServers = k
        self.points = n
        self.configuration = config
        self.vMove = [False for i in range(k)]
        self.vPosition = [-1 for i in range(k)]
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
                    leftServer = -1
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

    def distance(self, server, request):
        # print("server ",server, "request ",request)
        difference = abs(request-server)
        # print("Actual distance is ",difference)
        if difference > self.points/2:
            difference = self.points-difference

        return difference

    def makeUpdates(self, i, request):
        self.configuration[i] = request
        self.vMove[i] = False
        self.vPosition[i] = -1
        self.vDistance[i] = 0

    def processRequest(self, request):
        n = self.noOfServers
        # physical server is at requested location but not having any virtual move
        if request in self.configuration and self.vMove[self.configuration[request]] == False:
            index = self.configuration.index(request)
            self.makeUpdates(index, request)
            return 0, 0
        elif request in self.vPosition:  # If the virtual servers at requested location
            # if two are more virtual servers at location then serve with lower id
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
            leftS, rightS = self.findTwoServers(request)
            left_index = self.configuration.index(leftS)
            right_index = self.configuration.index(rightS)

            # if any virtual moves
            leftS = leftS if self.vMove[left_index] == False else self.vPosition[left_index]
            rightS = rightS if self.vMove[right_index] == False else self.vPosition[right_index]

            leftS_distance = self.vDistance[left_index]
            rightS_distance = self.vDistance[right_index]
            # print("Right ",rightS, " left ",leftS)
            # print("Right ",rightS, " left ",leftS)

            while True:
                if rightS == n+1:
                    rightS = 1
                if leftS == 0:
                    leftS = n
                rightS += 1
                leftS -= 1
                leftS_distance += 1
                rightS_distance += 1
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
    obj = VirtualDoubleCoverage(20, 3, [1, 5, 19])
    print(obj.noOfServers)
    print(obj.points)
    print(obj.configuration)
    print(obj.vMove)
    print(obj.vPosition)
    print(obj.vDistance)
    request = 3
    leftS, rightS = obj.findTwoServers(request)
    print(leftS, "<--- ", request, " --->", rightS)
    print("-------------------------------")
    print(obj.configuration)
    print(obj.processRequest(14))
    print(obj.configuration, obj.vPosition)
    print(obj.processRequest(12))
    print(obj.configuration, obj.vPosition)
    print("-----------------------------------")
