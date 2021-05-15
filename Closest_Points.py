import math
import sys

class Point:
    def __init__(self, x , y):
        self.x = x
        self.y = y
    def stringPoint(self):
        string = "(" + str(self.x) + "," + str(self.y) + ")"
        return string
    def getX(self):
        return self.x
    def getY(self):
        return self.y

# distance formula
def distance(point1 , point2):
    return math.sqrt((point2.x - point1.x)**2 + (point2.y - point1.y)**2)

# Global Variables
iterations = 0
closePoint1 = Point(0,0)
closePoint2 = Point(0,0)

# This algorithm is a very simple brute force algorithm, selects a point, then looks at the distance from that point to
#  every other point. It repeats this with every point and returns the 2 closest point with their distance
def bruteForce(listPoints):
    check1 = 0                                                      # declarations 
    check2 = 0
    point1 = Point(0,0)
    point2 = Point(0,0)
    global iterations

    dis = sys.maxsize
    for i in listPoints:                                            # iterations
        for j in listPoints:
            iterations += 1
            pointDis = distance(i,j)
            if pointDis < dis and check1 != check2:                 # if distance is min, save the distance as new min
                point1 = i                                          # if they are not the same point
                point2 = j
                dis = pointDis
            check2 += 1
        check2 = 0
        check1 += 1
        global closePoint1
        global closePoint2
        closePoint1 = point1
        closePoint2 = point2
    return dis
    
#These are functions are to sort the list in order x and in order y
def mergeSortX(listPoints):
    size = len(listPoints)
    if size > 1:
        middle = size // 2
        left = listPoints[:middle]
        right = listPoints[middle:]

        mergeSortX(left)
        mergeSortX(right)

        p = 0
        q = 0
        r = 0

        leftSize = len(left)
        rightSize = len(right)
        while p < leftSize and q < rightSize:
            if left[p].getX() < right[q].getX():
                listPoints[r] = left[p]
                p += 1
            else:  
                listPoints[r] = right[q]
                q += 1
            r += 1

        while p < leftSize:
            listPoints[r] = left[p]
            p += 1
            r += 1

        while q < rightSize:
            listPoints[r] = right[q]
            q += 1
            r += 1
    
        return listPoints

def mergeSortY(listPoints):
    size = len(listPoints)
    if size > 1:
        middle = size // 2
        left = listPoints[:middle]
        right = listPoints[middle:]

        mergeSortY(left)
        mergeSortY(right)

        p = 0
        q = 0
        r = 0

        leftSize = len(left)
        rightSize = len(right)
        while p < leftSize and q < rightSize:
            if left[p].getY() < right[q].getY():
                listPoints[r] = left[p]
                p += 1
            else:  
                listPoints[r] = right[q]
                q += 1
            r += 1

        while p < leftSize:
            listPoints[r] = left[p]
            p += 1
            r += 1

        while q < rightSize:
            listPoints[r] = right[q]
            q += 1
            r += 1
    
        return listPoints

#For the unlucky case where the closest points are in between of the 2 sorted by x list of points
def checkSplit(Xright , Y , d):
    midPoint = Xright[1]
    S = []
    global closePoint1
    global closePoint2
    for i in Y:
        if i.getX() >= d - midPoint.getX() or i.getX() <= d + midPoint.getX():      #if the numbers are further than the min distance between points in the sectors, filter them out
            S.append(i)
    for i in range(len(S)-3):                                   # check every poit in that distance while keeping the run time O(n)
        for j in range(3):
            P = S[i]
            Q = S[i+j]
            if distance(P,Q) < d and P != Q:                    # if a point is found, make that point the new distance and return it
                closePoint2 = Q
                closePoint1 = P
                d = distance(P,Q)
    return d  

def divideAndConquer(listPoints):
    return closestPoint(mergeSortX(listPoints),mergeSortY(listPoints))
    

def closestPoint(X,Y):
    global iterations
    iterations += 1
    if len(X) <= 3:
        return bruteForce(X)
    
    mid = len(X)//2
    Xleft = X[:mid]
    Xright = X[mid:]

    dis_left = closestPoint(Xleft , Y)
    dis_right = closestPoint(Xright , Y)

    dis = min(dis_left,dis_right)

    dis = checkSplit(Xright,Y,dis)
    
    return dis

def getInput():
    print("Enter P for premade points")
    print("Enter C to create new points")
    testPoints = [Point(-1230.0,1234.0), Point(234.0,23.0), Point(234.0,432.0), Point(3456235.0,341.0), Point(-1204234.0,-123234.0)]
    premade_or_create = input("Enter: ")
    if premade_or_create == "C":
        testPoints = createPoints()
    elif premade_or_create != "P":
        print("You know what, you get premade points since you cant follow instructions")
    
    if len(testPoints) > 1:
        print("\nEnter D to find the closest points using the Divide and Conquer Algorithm")
        print("Enter B to find the closest points using the Brute Force Algorithm")
        choice = input("Enter: ")
        printPoints = []
        for i in testPoints:
            printPoints.append(i.stringPoint())
        print("Points:" , printPoints)
        if choice == "B":
            print("Brute Force Algorithm: ")
            print("Distance: ",bruteForce(testPoints) , "Points: ", closePoint1.stringPoint() , closePoint2.stringPoint())
            print(str(len(testPoints)) + " values given with " + str(iterations) + " iterations, making this a O(n^2) algorithm\n\n" )
        elif choice == "D":
            print("Divide and Conquer Algorithm: ")
            print("Distance: ", divideAndConquer(testPoints) , "Points: ",closePoint1.stringPoint() , closePoint2.stringPoint())
            print("Prove O(nlg(n)) using masters theorm: \nRecursive equation: T(n) = 2T(n/2) + n \nValues: a = 2 , b = 2, d = 1 \n(log_2(2)) = 1 = d \nTherefore the run time is O(nlg(n))")
    else:
        print("It's really hard to find the closest distance between points when you do not have at least 2 points...")




def createPoints():
    newPoint = "Y"
    result = []
    while(newPoint != "N"):
        newPoint = input("New Point? (Enter Y/N): ")
        if newPoint == "Y":
            x = input("Enter x value: ")
            y = input("Enter y value: ")
            try:
                x = float(x)
                y = float(y)
            except ValueError as e:
                print(e)

            result.append(Point(x,y))
    return result




getInput()
input("Enter anything to exit: ")
