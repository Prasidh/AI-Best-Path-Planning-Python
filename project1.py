# print("Start of program")
import random
from heapq import heappush, heappop, heapify  

class cell: #Node storing each cell of grid
    def __init__(self):
        self.rowNum = -1
        self.colNum = -1
        self.blocked = 0 # 0 denotes False, all cells are initially unblocked
        self.f = 0 # Distance from start node
        self.g = 0 # Distance from goal node
        self.h = 0 # Total cost ( h = f + g )
        self.parent = None

class MinHeap: 
    # Constructor to initialize a heap 
    def __init__(self): 
        self.heap = []  
  
    def parent(self, i): 
        return (i-1)/2
      
    # Inserts a new key 'k' 
    def insertKey(self, k): 
        heappush(self.heap, k)            
  
    # Decrease value of key at index 'i' to new_val 
    # It is assumed that new_val is smaller than heap[i] 
    def decreaseKey(self, i, new_val): 
        self.heap[i]  = new_val  
        while(i != 0 and self.heap[self.parent(i)] > self.heap[i]): 
            # Swap heap[i] with heap[parent(i)] 
            self.heap[i] , self.heap[self.parent(i)] = ( 
            self.heap[self.parent(i)], self.heap[i]) 
              
    # Method to remove minium element from min heap 
    def extractMin(self): 
        return heappop(self.heap) 
  
    # This functon deletes key at index i. It first reduces 
    # value to minus infinite and then calls extractMin() 
    def deleteKey(self, i): 
        self.decreaseKey(i, float("-inf")) 
        self.extractMin() 
  
    # Get the minimum element from the heap 
    def getMin(self): 
        return self.heap[0]

totalRows = 10
totalCols = 10
cellsArray = [[cell() for j in range(totalCols)] for i in range(totalRows)]

def decision(): # Generates probability value for generating maze
    return random.random() < 0.7

def create_grid():
    # Instantiates all the cell objects
    for i in range(totalRows):
        for j in range(totalCols):
            cellsArray[i][j] = cell()
            cellsArray[i][j].rowNum = i
            cellsArray[i][j].colNum = j

numUnblocked = 0

def generate_maze():
    global numBlocked
    global numUnblocked
    global cellsArray
    for i in range(totalRows):
        for j in range(totalCols):
            if decision(): # Randomly decides whether the cell is blocked or unblocked
                cellsArray[i][j].blocked = 0
                numUnblocked = numUnblocked+1
            else:
                cellsArray[i][j].blocked = 1



start_row = -1
start_col = -1
end_row = -1
end_col = -1

# Randomly picks 2 unblocked cells to be the starting and ending point
def set_start_and_end(unblockedCells):
    global start_row
    global start_col
    global end_row
    global end_col
    ctr1 = 0
    for i in range(totalRows):
        for j in range(totalCols):
            if cellsArray[i][j].blocked == 0:
                unblockedCells[ctr1] = cellsArray[i][j]
                ctr1 = ctr1+1
    
    #Initialize start position
    startIndex = random.randint(0,len(unblockedCells)-1)
    start_row = unblockedCells[startIndex].rowNum
    start_col = unblockedCells[startIndex].colNum

    #Initialize target position
    endIndex = random.randint(0, len(unblockedCells)-1)
    end_row = unblockedCells[endIndex].rowNum
    end_col = unblockedCells[endIndex].colNum


def print_grid():
    for i in range(totalRows):
        for j in range(totalCols):
            if cellsArray[i][j].rowNum == start_row and cellsArray[i][j].colNum == start_col:
                print("S"),
            elif cellsArray[i][j].rowNum == end_row and cellsArray[i][j].colNum == end_col:
                print("T"),
            else:
                if cellsArray[i][j].blocked == 0:
                    print("O"),
                else:
                    print("X"),
        print()

def Astar_search():
    global start_row
    global start_col
    global end_row
    global end_col
    # Initialize start and end cells
    startCell = cellsArray[start_row][start_col] 
    endCell = cellsArray[end_row][end_col]

    # Initialize open and closed lists
    openList = []
    closedList = []

    # Add starting position to open list
    openList.append(cellsArray[start_row][start_col])

    # Loop until we find target cell
    while(len(openList) > 0):
        #Get current cell
        currentCell = openList[0]
        currentIndex = 0

        # Pop current cell from open list and add to closed list
        openList.pop(currentIndex)
        closedList.append(currentCell)

        # Check if we found the goal (success case)
        if currentCell.rowNum == end_row and currentCell.colNum == end_col:
            print("Target found successfully!")
            path = []
            cur = currentCell
            while cur is not None:
                pos = [cur.rowNum, cur.colNum]
                path.append(pos)
                cur = cur.parent
            return path[::-1]

        # Generate children
        children = []
        if currentCell.rowNum > 0: #check if up child exists
            if cellsArray[currentCell.rowNum -1][currentCell.colNum].blocked == 0: # check if it's blocked
                # cellsArray[currentCell.rowNum -1][currentCell.colNum].parent = currentCell
                children.append(cellsArray[currentCell.rowNum -1][currentCell.colNum])

        if currentCell.colNum < totalCols -1: #check if right child exists
            if cellsArray[currentCell.rowNum][currentCell.colNum+1].blocked == 0: # check if it's blocked
                # cellsArray[currentCell.rowNum][currentCell.colNum+1].parent = currentCell
                children.append(cellsArray[currentCell.rowNum][currentCell.colNum+1])

        if currentCell.rowNum < totalRows -1: #check if down child exists
            if cellsArray[currentCell.rowNum +1][currentCell.colNum].blocked == 0: # check if it's blocked
                # cellsArray[currentCell.rowNum +1][currentCell.colNum].parent = currentCell
                children.append(cellsArray[currentCell.rowNum +1][currentCell.colNum])


        if currentCell.colNum > 0: #check if left child exists
            if cellsArray[currentCell.rowNum][currentCell.colNum-1].blocked == 0: # check if it's blocked
                # cellsArray[currentCell.rowNum][currentCell.colNum-1].parent = currentCell
                children.append(cellsArray[currentCell.rowNum][currentCell.colNum-1])

        # Loop through children
        for i in range(0, len(children)):

            # Set child to current index in children
            curChild = children[i]

            # Check if child on closed list
            isClosed = 0
            for closedChild in closedList:
                if curChild.rowNum == closedChild.rowNum and curChild.colNum == closedChild.colNum:
                    isClosed = 1
                    continue
            if not isClosed:
                curChild.parent = currentCell # Set child's parent to current cell

            # Create f, g, and h values
            curChild.g = currentCell.g + 1
            curChild.h = abs(curChild.rowNum - end_row) + abs(curChild.colNum - end_col) 
            curChild.f = curChild.g + curChild.h

            # Check if child on open list
            noPathCtr = 0
            for openCell in openList:
                noPathCtr = noPathCtr + 1
                if noPathCtr > 1000000:
                    return None
                if curChild.rowNum == openCell.rowNum and curChild.colNum == curChild.colNum == openCell.colNum and curChild.g > openCell.g:
                    continue

            # Finally, add child to open list
            openList.append(curChild)

def backwards_Astar():
    global start_row
    global start_col
    global end_row
    global end_col
    # Initialize start and end cells
    startCell = cellsArray[start_row][start_col] 
    endCell = cellsArray[end_row][end_col]

    # Initialize open and closed lists
    openList = []
    closedList = []

    # Add target position to open list
    openList.append(cellsArray[end_row][end_col])

    # Loop until we find starting point
    while(len(openList) > 0):
        #Get current cell
        currentCell = openList[0]
        currentIndex = 0

        # Pop current cell from open list and add to closed list
        openList.pop(currentIndex)
        closedList.append(currentCell)

        # Check if we found the goal (success case)
        if currentCell.rowNum == start_row and currentCell.colNum == start_col:
            print("Start point found successfully!")
            path = []
            cur = currentCell
            while cur is not None:
                pos = [cur.rowNum, cur.colNum]
                path.append(pos)
                cur = cur.parent
            return path[::-1]

        # Generate children
        children = []
        if currentCell.rowNum > 0: #check if up child exists
            if cellsArray[currentCell.rowNum -1][currentCell.colNum].blocked == 0: # check if it's blocked
                # cellsArray[currentCell.rowNum -1][currentCell.colNum].parent = currentCell
                children.append(cellsArray[currentCell.rowNum -1][currentCell.colNum])

        if currentCell.colNum < totalCols -1: #check if right child exists
            if cellsArray[currentCell.rowNum][currentCell.colNum+1].blocked == 0: # check if it's blocked
                # cellsArray[currentCell.rowNum][currentCell.colNum+1].parent = currentCell
                children.append(cellsArray[currentCell.rowNum][currentCell.colNum+1])

        if currentCell.rowNum < totalRows -1: #check if down child exists
            if cellsArray[currentCell.rowNum +1][currentCell.colNum].blocked == 0: # check if it's blocked
                # cellsArray[currentCell.rowNum +1][currentCell.colNum].parent = currentCell
                children.append(cellsArray[currentCell.rowNum +1][currentCell.colNum])


        if currentCell.colNum > 0: #check if left child exists
            if cellsArray[currentCell.rowNum][currentCell.colNum-1].blocked == 0: # check if it's blocked
                # cellsArray[currentCell.rowNum][currentCell.colNum-1].parent = currentCell
                children.append(cellsArray[currentCell.rowNum][currentCell.colNum-1])

        # Loop through children
        for i in range(0, len(children)):

            # Set child to current index in children
            curChild = children[i]

            # Check if child on closed list
            isClosed = 0
            for closedChild in closedList:
                if curChild.rowNum == closedChild.rowNum and curChild.colNum == closedChild.colNum:
                    isClosed = 1
                    continue
            if not isClosed:
                curChild.parent = currentCell # Set child's parent to current cell

            # Create f, g, and h values
            curChild.g = currentCell.g + 1
            curChild.h = abs(curChild.rowNum - end_row) + abs(curChild.colNum - end_col) 
            curChild.f = curChild.g + curChild.h

            # Check if child on open list
            noPathCtr = 0
            for openCell in openList:
                noPathCtr = noPathCtr + 1
                if noPathCtr > 1000000:
                    return None
                if curChild.rowNum == openCell.rowNum and curChild.colNum == curChild.colNum == openCell.colNum and curChild.g > openCell.g:
                    continue

            # Finally, add child to open list
            openList.append(curChild)

def main():
    #First set all global vars
    global numUnblocked
    global start_row
    global start_col
    global end_row
    global end_col

    create_grid()

    # Generate all 50 mazes
    for j in range(50):
        #Reset all global variables to their initial values
        numUnblocked = 0
        start_row = -1
        start_col = -1
        end_row = -1
        end_col = -1

        generate_maze()

        # List containing all the unblocked cells
        unblockedCells = [cell() for i in range(numUnblocked)]

        set_start_and_end(unblockedCells)
        print_grid()

        # Reset all heuristics and parent in cells
        for k in range(totalRows):
            for l in range(totalCols):
                cellsArray[k][l].g = 0
                cellsArray[k][l].h = 0
                cellsArray[k][l].f = 0
                cellsArray[k][l].parent = None

        print("Computing Repeated Forward A* Path...")
        path1 = Astar_search()    
        if path1 is None:
            print("No paths found.")
        else:
            for i in range(len(path1)):
                print(path1[i])
        print("Length of path: "),
        print(len(path1))

        print_grid()

        # Reset all heuristics and parent in cells
        for k in range(totalRows):
            for l in range(totalCols):
                cellsArray[k][l].g = 0
                cellsArray[k][l].h = 0
                cellsArray[k][l].f = 0
                cellsArray[k][l].parent = None

        print("Computing Repeated Backward A* Path...")
        path2 = backwards_Astar()
        if path2 is None:
            print("No paths found.")
        else:
            for i in range(len(path2)):
                print(path2[i])
        print("Length of path: "),
        print(len(path2))





        


main()










            




