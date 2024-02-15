import random
import copy, math
"""
class Node:
    def __init__(self, cell):
        self.cell = cell
        self.parent = None
        self.g = 0  # Cost from the start node to current node
        self.h = 0  # Heuristic cost from current node to the goal node
        self.f = 0  # Total cost: f = g + h
    def __lt__(self, other):
        return self.f < other.f
"""
class Bot:
    def __init__(self, row, col):
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
        self.probabilityofleak = 0
        self.probabilityofbeep = 0.0
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
def step(grid, rob, row, col):
    grid[rob.r][rob.c].bot_there = False
    grid[rob.r][rob.c].status = 'o'
    rob.r = row
    rob.c = col
    grid[rob.r][rob.c].bot_there = True
    grid[rob.r][rob.c].status = 'Bot'
"""
def setbuffern(grid,N):
    for row in range(N):
        for col in range(N):
            listb = []
            for neighbor in grid[row][col].availablen:
                for n in neighbor.availablen:
                    if n.status != 'c' and n.fire == False:
                        listb.append(n)
            grid[row][col].buffern = listb
"""
def setavailablen(grid,N):
    for row in range(N):
        for col in range(N):
            lista = []
            for neighbor in grid[row][col].openneighbors:
                if neighbor.status == 'o':
                    lista.append(neighbor)
            grid[row][col].availablen = lista

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

# Modify BFS to use coordinates instead of Cell objects
def BFS(grid, start, goal):
    explored = set()
    queue = [[start]]

    if start == goal:
        print("success")
        return [start]

    while queue:
        path = queue.pop(0)
        row, col = path[-1]

        if (row, col) not in explored:
            for neighbor in grid[row][col].openneighbors:
                new_path = list(path)
                new_path.append((neighbor.r, neighbor.c))
                queue.append(new_path)

                if (neighbor.r, neighbor.c) == goal:
                    return len(new_path)

            explored.add((row, col))
    print("So sorry, but a connecting path doesn't exist :(")
    
def pathBFS(grid, start, goal):
    explored = set()
    queue = [[start]]

    if start == goal:
        return [start]

    while queue:
        path = queue.pop(0)
        row, col = path[-1]

        if (row, col) not in explored:
            for neighbor in grid[row][col].openneighbors:
                new_path = list(path)
                new_path.append((neighbor.r, neighbor.c))
                queue.append(new_path)

                if (neighbor.r, neighbor.c) == goal:
                    return new_path

            explored.add((row, col))
    print("So sorry, but a connecting path doesn't exist :(")
"""
def count_fire_neighbors(grid, row, col):
    count = 1
    for neighbor in grid[row][col].openneighbors:
        if neighbor.fire == True:
            count +=1
    return count
"""


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



"""
def spreadFire(grid,N,q):
    grid2 = copy.deepcopy(grid)
    for row in range(N):
        for col in range(N):
            if grid2[row][col].fire == True:
                for neighbor in grid[row][col].openneighbors:
                    n = count_fire_neighbors(grid2,neighbor.r,neighbor.c)
                    #print(n)
                    fireProb = 1-(1-q)**n
                    #print(fireProb)
                    if grid2[row][col].fire == True:
                        if random.uniform(0,1)<=fireProb:
                            neighbor.fire = True
"""
def main():
    """
    BOT 7 IS BASICALLY BOT 3 BUT WITH TWO CELLS
    PROBABILITY UPDATES ARE SAME AS BOT 3
    BOT 7 LOCATES FIRST CELL AND PLUGS THE LEAK
    THE SECOND LEAK IS THEN FOUND FROM FIRST LEAK CELL LOCATION
    """
    N = 30
    grid = [[Cell() for _ in range(N)] for _ in range(N)]

    # SET NEIGHBOURS
    for row in range(N):
        for col in range(N):
            grid[row][col].r = row
            grid[row][col].c = col
            if row > 0:
                grid[row][col].n1 = grid[row-1][col]
            if row < N-1:
                grid[row][col].n2 = grid[row+1][col]
            if col > 0:
                grid[row][col].n3 = grid[row][col-1]
            if col < N-1:
                grid[row][col].n4 = grid[row][col+1]

    #OPEN RANDOM CELL
    start_row = random.randint(1, N - 2)
    start_col = random.randint(1, N - 2)
    grid[start_row][start_col].status = 'o'


    openCells = [grid[start_row][start_col]]

    # CREATE SHIP STUFF
    create_path(grid, N, openCells)
    dead_ends(grid, N)

    # SET OPEN NEIGHBORS
    set_open_neighbors(grid, N)

    
    """
    #PRINT OPENNEIGHBORS
    print("openneighbors:")
    for cell in grid[2][2].openneighbors:
        print(cell.status)
    """
    
    
    #WHERE TO PUT BOT
    botCell = random.choice(openCells)
    botCell.bot_there = True
    rob = Bot(botCell.r, botCell.c)
    grid[botCell.r][botCell.c].status = 'Bot'
    
    
    #WHERE THE FIRST LEAK IS LOCATED
    leakCella = random.choice(openCells)
    grid[leakCella.r][leakCella.c].status = 'Leak'
    #WHERE THE SECOND LEAK IS LOCATED
    leakCellb = random.choice(openCells)
    grid[leakCellb.r][leakCellb.c].status = 'Leak'
                
    
     
    #COUNTING HOW MANY CELLS INITIALLY OUTSIDE OF THE BOT CELL           
    count = 0
    for i in range(N):
        for j in range(N):
            if grid[i][j].status == 'o' or grid[i][j].status == 'Leak':
                count += 1
                
    #DECLARE ALPHA VALUE TO USE LATER IN CALCULATIONS
    total_actions = 0
    for i in range(N):
        for j in range(N):
            if grid[i][j].status == 'o' or grid[i][j].status == 'Leak':
                grid[i][j].probabilityofleak = 1/(count - 1)
            else:
                grid[i][j].probabilityofleak = 0
    
    #CREATING PROBABILITY MATRIX FOR ALL CELLS IN SHIP
    probabilitymatrix = [[float for _ in range(N)] for _ in range(N)]
    for i in range(N):
        for j in range(N):
            probabilitymatrix[i][j] = grid[i][j].probabilityofleak
    
    
    alpha = 0.3
    while grid[leakCella.r][leakCella.c].status != 'Bot':
        if grid[rob.r][rob.c].leak == False:
            probabilitymatrix[rob.r][rob.c] = 0
            beep = random.random()
            distance = BFS(grid, (rob.r, rob.c), (leakCella.r, leakCella.c)) - 1
            power = distance * alpha * (-1)
            probabilityofbeep = math.pow(math.e, power)
            probabilityofbeepini = 0
            total_actions += 1
            if probabilityofbeep > beep:
                for i in range(N):
                    for j in range(N):
                        if grid[i][j].status == 'o':
                            probabilityofbeepini += probabilitymatrix[i][j] * math.pow(math.e, (-1)*alpha*BFS(grid, (i, j), (rob.r, rob.c)))
                for i in range(N):
                    for j in range(N):
                        if grid[i][j].status == 'o':
                            probabilitymatrix[i][j] = (probabilitymatrix[i][j] * math.pow(math.e, (-1)*alpha*BFS(grid, (i, j), (rob.r, rob.c))))/probabilityofbeepini
            else:
                probabilityofbeepini = 1
                pnobeepini = 0
                for i in range(N):
                    for j in range(N):
                        if grid[i][j].status == 'o':
                            probabilityofbeepini -= probabilitymatrix[i][j] * math.pow(math.e, (-1)*alpha*BFS(grid, (i, j), (rob.r, rob.c)))
                            pnobeepini = probabilityofbeepini
                for i in range(N):
                    for j in range(N):
                        if grid[i][j].status == 'o':
                            probabilitymatrix[i][j] = probabilitymatrix[i][j] * (1-math.pow(math.e, (-1)*alpha*BFS(grid, (i, j), (rob.r, rob.c)))) / pnobeepini
        maxprob = 0
        for i in range(N):
            for j in range(N):
                if probabilitymatrix[i][j] > maxprob:
                    maxprob = probabilitymatrix[i][j]
                    rowtomoveto = i
                    coltomoveto = j
        steps = pathBFS(grid, (rob.r, rob.c), (rowtomoveto, coltomoveto))
        step(grid, rob, rowtomoveto, coltomoveto)
        for cell in steps:
            step(grid, rob, cell[0], cell[1])
            if grid[leakCella.r][leakCella.c].status == 'Bot':
                print(str(total_actions))
            else:
                total_actions += 1
                
    while grid[leakCellb.r][leakCellb.c].status != 'Bot':
        if grid[rob.r][rob.c].leak == False:
            probabilitymatrix[rob.r][rob.c] = 0
            beep = random.random()
            distance = BFS(grid, (rob.r, rob.c), (leakCellb.r, leakCellb.c)) - 1
            power = distance * alpha * (-1)
            probabilityofbeep = math.pow(math.e, power)
            probabilityofbeepini = 0
            total_actions += 1
            if probabilityofbeep > beep:
                for i in range(N):
                    for j in range(N):
                        if grid[i][j].status == 'o':
                            probabilityofbeepini += probabilitymatrix[i][j] * math.pow(math.e, (-1)*alpha*BFS(grid, (i, j), (rob.r, rob.c)))
                for i in range(N):
                    for j in range(N):
                        if grid[i][j].status == 'o':
                            probabilitymatrix[i][j] = (probabilitymatrix[i][j] * math.pow(math.e, (-1)*alpha*BFS(grid, (i, j), (rob.r, rob.c))))/probabilityofbeepini
            else:
                probabilityofbeepini = 1
                pnobeepini = 0
                for i in range(N):
                    for j in range(N):
                        if grid[i][j].status == 'o':
                            probabilityofbeepini -= probabilitymatrix[i][j] * math.pow(math.e, (-1)*alpha*BFS(grid, (i, j), (rob.r, rob.c)))
                            pnobeepini = probabilityofbeepini
                for i in range(N):
                    for j in range(N):
                        if grid[i][j].status == 'o':
                            probabilitymatrix[i][j] = probabilitymatrix[i][j] * (1-math.pow(math.e, (-1)*alpha*BFS(grid, (i, j), (rob.r, rob.c)))) / pnobeepini
        maxprob = 0
        for i in range(N):
            for j in range(N):
                if probabilitymatrix[i][j] > maxprob:
                    maxprob = probabilitymatrix[i][j]
                    rowtomoveto = i
                    coltomoveto = j
        steps = pathBFS(grid, (rob.r, rob.c), (rowtomoveto, coltomoveto))
        step(grid, rob, rowtomoveto, coltomoveto)
        for cell in steps:
            step(grid, rob, cell[0], cell[1])
            if grid[leakCellb.r][leakCellb.c].status == 'Bot':
                print(str(total_actions))
            else:
                total_actions += 1
                
    print(str(total_actions))


if __name__ == "__main__":
    main()