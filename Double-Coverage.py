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

    def process_Request(self, request):
        if request in self.config:
            index = self.config.index(request)
            self.vMove = False
            self.vDirection = 0
            self.vPosition = -1
            return 0
        leftS, rightS = self.findTwoServers(request)
        index_l = self.config.index(leftS)
        index_r = self.config.index(rightS)

        if self.vMove[index_l] == True and self.vMove[index_r] == True:
            if self.vPosition[index_l] == request and self.vPosition[index_r] == request:
                # write code to move lower id server to requested locations and make updates
                print()
            elif self.vPosition[index_l] == request:
                # write code to move left server and make updates
                print()
            elif self.vPosition[index_r] == request:
                # write code ro move right server and makeupdates
                print()

        # if there is any virtual moves for the servers then we need to take that positions to handle
        leftS = self.vPosition[index_l] if self.vMove[index_l] == True else leftS
        rightS = self.vPosition[index_r] if self.vMove[index_r] == True else rightS

        # here check if the virtual servers is front of the requested location in same direction

        # distances
        dl = 0
        dr = 0
        print("NAveen")
        # process request using moves
        # 1. Check for the condition in which virtual and physical servers at equal distance

        while True:
            if rightS == n+1:
                rightS = 1
            if leftS == 0:
                leftS = self.points
            rightS += 1
            leftS += 1
            dl += 1
            dr += 1
            if rightS == request and leftS == request:
                # check for the condition if virtual server and physical servers at same distance
                # write code for moving lower id server and make updates and break
                print()
            elif rightS == request:
                # move right server to requested loction and make updates and break
                print()
            elif leftS == request:
                # move left server and make updates and break
                print()
            print()
            break


#
if __name__ == "__main__":
    n = 10
    k = 3
    config = [10, 1, 3]
    request = 5
    obj = DoubleCoverage(n, k, config)
    left, right = obj.findTwoServers(request)
    print(left, "<-- ", request, "--> ", right)
    print(obj.config.index(left))
    print(obj.config.index(right))
    print(obj.vDirection)
    print(obj.vMove)
    print(obj.vPosition)
    print(obj.process_Request(request))
