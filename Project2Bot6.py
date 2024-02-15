import random
import copy, math
import numpy as np
class Node:
    def __init__(self, cell):
        self.cell = cell
        self.parent = None
        self.g = 0  # Cost from the start node to current node
        self.h = 0  # Heuristic cost from current node to the goal node
        self.f = 0  # Total cost: f = g + h
    def __lt__(self, other):
        return self.f < other.f

class Bot:
    def __init__(self, row, col):
        self.dead = False
        self.r = row
        self.c = col
class Cell:

    def __init__(self):
        self.status = 'C'
        self.r = None
        self.c = None
        self.n1 = None
        self.n2 = None
        self.n3 = None
        self.n4 = None
        self.neighbors = [self.n1,self.n2,self.n3,self.n4]
        self.openneighbors = []
        self.leak = False
        self.bot_there = False
        self.button = False
        self.availablen = []
        self.visited = False
        self.buffern = []
        self.closedn = []
        self.g_score = 0
        self.h_score = 0
        self.f_score = 0
        self.came_from = None
        self.probabilityofleak = True
    """
    def __lt__(self, other):
        return self.f_score < other.f_score
    """
    def __deepcopy__(self, memo):
        # Create a new instance of the Cell class
        new_cell = Cell()

        # Copy simple attributes
        new_cell.status = copy.deepcopy(self.status, memo)
        new_cell.r = copy.deepcopy(self.r, memo)
        new_cell.c = copy.deepcopy(self.c, memo)
        new_cell.leak = copy.deepcopy(self.leak, memo)
        new_cell.bot_there = copy.deepcopy(self.bot_there, memo)
        new_cell.button = copy.deepcopy(self.button, memo)
        new_cell.visited = copy.deepcopy(self.visited, memo)

        # Handle neighbors to avoid circular references
        new_cell.n1 = None if self.n1 is None else new_cell
        new_cell.n2 = None if self.n2 is None else new_cell
        new_cell.n3 = None if self.n3 is None else new_cell
        new_cell.n4 = None if self.n4 is None else new_cell

        # ... (copy other attributes as needed)

        return new_cell
    

def makeGraph(grid,N):
    graph = {}
    for row in range(N):
        for col in range(N):
            graph.update({grid[row][col]:grid[row][col].availablen})
    return graph



def set_open_neighbors(grid,N):
        
        for row in range(N):
            for col in range(N):
                on = []
                if grid[row][col].n1!= None:
                    if grid[row][col].n1.status != 'C':
                        on.append(grid[row][col].n1)
                if grid[row][col].n2 != None:
                    if grid[row][col].n2.status != 'C':
                        on.append(grid[row][col].n2)
                if grid[row][col].n3 != None:
                    if grid[row][col].n3.status != 'C':
                        on.append(grid[row][col].n3)
                if grid[row][col].n4 != None:
                    if grid[row][col].n4.status != 'C':
                        on.append(grid[row][col].n4)
                grid[row][col].openneighbors = on

def setClosedn(grid,N):
    for row in range(N):
        for col in range(N):
            cn = []
            if grid[row][col].n1!= None:
                if grid[row][col].n1.status == 'C':
                    cn.append(grid[row][col].n1)
            if grid[row][col].n2 != None:
                if grid[row][col].n2.status == 'C':
                    cn.append(grid[row][col].n2)
            if grid[row][col].n3 != None:
                if grid[row][col].n3.status == 'C':
                    cn.append(grid[row][col].n3)
            if grid[row][col].n4 != None:
                if grid[row][col].n4.status == 'C':
                    cn.append(grid[row][col].n4)
            grid[row][col].closedn = cn                

def count_open_neighbors(grid, row, col):
    count = 0
    if grid[row][col].n1 != None:
        if grid[row][col].n1.status == "o":
            count +=1
    if grid[row][col].n2 != None:
        if grid[row][col].n2.status == "o":
            count +=1
    if grid[row][col].n3 != None:
        if grid[row][col].n3.status == "o":
            count +=1
    if grid[row][col].n4 != None:
        if grid[row][col].n4.status == "o":
            count +=1
    return count



def create_path(grid, N, openCells):
    while True:
        changed = False
        for row in range(N):
            for col in range(N):
                if grid[row][col].status == 'C' and count_open_neighbors(grid, row, col) == 1:
                    grid[row][col].status = 'o'
                    openCells.append(grid[row][col]) #put a list of cells that are open
                    changed = True
        if changed==False:
            break

def dead_ends(grid, N):
    deadends = []
    for row in range(N):
        for col in range(N):
            if grid[row][col].status == 'o' and count_open_neighbors(grid,row,col) == 1:
                deadends.append(grid[row][col])
    random.shuffle(deadends)
    deadends = deadends[:len(deadends)//2]
    for deadend in deadends:
        if deadends != None:
            if len(deadend.closedn) > 0:
                tobeopened = random.choice(deadend.closedn)
                tobeopened.status = 'o'
    return


def step(grid, rob, row, col):
    grid[rob.r][rob.c].bot_there = False
    grid[rob.r][rob.c].status = 'o'
    rob.r = row
    rob.c = col
    grid[rob.r][rob.c].bot_there = True
    grid[rob.r][rob.c].status = 'Bot'


def main():
    N = 30
    grid = [[Cell() for _ in range(N)] for _ in range(N)]

    for row in range(N):
        for col in range(N):
            if row > 0:
                 grid[row][col].n1 = grid[row-1][col]
            if row <N-1:
                grid[row][col].n2 = grid[row+1][col]
            if col > 0:
                grid[row][col].n3 = grid[row][col-1]
            if col < N-1:
                grid[row][col].n4 = grid[row][col+1]
            grid[row][col].r = row
            grid[row][col].c = row

    #OPEN RANDOM CELL
    start_row = random.randint(1, N - 2)
    start_col = random.randint(1, N - 2)
    grid[start_row][start_col].status = 'o'


    #CREATE PATH
    openCells = []
    create_path(grid, N, openCells)

    dead_ends(grid, N)




    # SET OPEN NEIGHBORS
    set_open_neighbors(grid, N)

    #SET CLOSED NEIGHBORS
    setClosedn(grid,N)
    
    #DEFINE K
    k = 1
    
    #WHERE TO PUT BOT
    botCell = random.choice(openCells)
    botCell.bot_there = True
    for i in range(N):
        for j in range(N):
            if grid[i][j].bot_there == True:
                grid[i][j].status = 'Bot'
                botCell.r = i 
                botCell.c = j
                break
    rob = Bot(botCell.r, botCell.c)
    
    
    
    
    
    #WHERE THE LEAK IS LOCATED
    leakCell = random.choice(openCells)
    leakCell.leak = True
    leakrow = 0
    leakcol = 0
    for row in range(N):
        for col in range(N):
            if grid[row][col].leak == True:
                grid[row][col].status = 'Leak'
                leakrow = row
                leakcol = col
    
    #MAKE SURE LEAK CELL IS NOT WITHIN DETECTION SQUARE OF BOT
    while abs(leakrow - rob.r) < k and abs(leakcol - rob.c) < k:
        leakCell = random.choice(openCells)
        leakrow = leakCell.r
        leakcol = leakCell.c
        
    
    #SECOND LEAK
    #WHERE THE LEAK IS LOCATED
    leakCell2 = random.choice(openCells)
    leakCell2.leak = True
    leakrow2 = 0
    leakcol2 = 0
    for row in range(N):
        for col in range(N):
            if grid[row][col].leak == True:
                grid[row][col].status = 'Leak'
                leakrow2 = row
                leakcol2 = col
    
    #MAKE SURE LEAK CELL IS NOT WITHIN DETECTION SQUARE OF BOT
    while abs(leakrow2 - rob.r) < k and abs(leakcol2 - rob.c) < k:
        leakCell2 = random.choice(openCells)
        leakrow2 = leakCell.r
        leakcol2 = leakCell.c
    
    for row in grid:
        print(" ".join(cell.status for cell in row))
    
    #Initialize may contain leak to have all open cells
    may_contain_leak = []
    for i in range(N):
        for j in range(N):
            if grid[i][j].status == 'o' or grid[i][j].status == 'Leak':
                may_contain_leak.append([i, j])
    
    
    total_actions = 0            
    while grid[leakrow][leakcol].status != 'Bot':
        detection = False
        #Creating 2k+1 * 2k+1 detection square to run on bot
        #Making sure detection square does not go out of bounds
        maxX = max(0, min(rob.r + k, 50))
        minX = max(0, min(rob.r - k, 50))
        maxY = max(0, min(rob.c + k, 50))
        minY = max(0, min(rob.c - k, 50))
        opencellsinsquare = []
        for i in range(minX, maxX):
            for j in range(minY, maxY):
                if grid[i][j].status == 'o' and grid[i][j].leak == False:
                    opencellsinsquare.append([i, j])
                if grid[i][j].leak == True:
                    detection = True
                    opencellsinsquare.append([i, j])
        total_actions += 1
        if detection == False:
            may_contain_leak = [i for i in may_contain_leak if i not in opencellsinsquare]
        if detection == True:
            may_contain_leak = opencellsinsquare
        num = random.randint(0, len(may_contain_leak))
        grid[rob.r][rob.c].bot_there = False
        grid[rob.r][rob.c].status = 'C'
        i = rob.r
        j = rob.c
        rob.r = may_contain_leak[num][0]
        rob.c = may_contain_leak[num][1]
        grid[rob.r][rob.c].status = 'Bot'
        grid[rob.r][rob.c].bot_there = True
        total_actions += math.sqrt(math.pow(rob.r-i, 2) + math.pow(rob.c-j, 2))
        
        
        
        
    while grid[leakrow2][leakcol2].status != 'Bot':
        detection = False
        #Creating 2k+1 * 2k+1 detection square to run on bot
        #Making sure detection square does not go out of bounds
        maxX = max(0, min(rob.r + k, 50))
        minX = max(0, min(rob.r - k, 50))
        maxY = max(0, min(rob.c + k, 50))
        minY = max(0, min(rob.c - k, 50))
        opencellsinsquare = []
        for i in range(minX, maxX):
            for j in range(minY, maxY):
                if grid[i][j].status == 'o' and grid[i][j].leak == False:
                    opencellsinsquare.append([i, j])
                if grid[i][j].leak == True:
                    detection = True
                    opencellsinsquare.append([i, j])
        total_actions += 1
        if detection == False:
            may_contain_leak = [i for i in may_contain_leak if i not in opencellsinsquare]
        if detection == True:
            may_contain_leak = opencellsinsquare
        num = random.randint(0, len(may_contain_leak))
        grid[rob.r][rob.c].bot_there = False
        grid[rob.r][rob.c].status = 'C'
        i = rob.r
        j = rob.c
        rob.r = may_contain_leak[num][0]
        rob.c = may_contain_leak[num][1]
        grid[rob.r][rob.c].status = 'Bot'
        grid[rob.r][rob.c].bot_there = True
        total_actions += math.sqrt(math.pow(rob.r-i, 2) + math.pow(rob.c-j, 2))
        
        
    print(str(total_actions))          
    print("The bot reached the leak")
    
        
                
                      
    print()
                       
    
    


if __name__ == "__main__":
    main()