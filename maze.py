import random
import copy

class Cell:
    def __init__(self, i, j, walls=[True, True, True, True]):
        self.row = i
        self.col = j
        self.walls = copy.deepcopy(walls)

class Maze:
    def __init__(self, nrow: int, ncol: int):
        self.nrow = nrow
        self.ncol = ncol
        self.cells = [[Cell(i, j) for j in range(ncol)] for i in range(nrow)]

class MazeGenerator: 
    def __init__(self, maze: Maze, start=(0, 0)):
        self.maze = maze
        self.visited = [[False for j in range(maze.ncol)] for i in range(maze.nrow)]
        self.stack = []
        self.closed = []
        self.current = maze.cells[start[0]][start[1]]
        self.visited[start[0]][start[1]] = True
        self.stack.append(self.current)

    def get_neighbors(self, cell: Cell) -> list:
        neighbors = []
        if cell.row > 0 and not self.visited[cell.row-1][cell.col]:
            neighbors.append(self.maze.cells[cell.row-1][cell.col])
        if cell.col > 0 and not self.visited[cell.row][cell.col-1]:
            neighbors.append(self.maze.cells[cell.row][cell.col-1])
        if cell.row < self.maze.nrow-1 and not self.visited[cell.row+1][cell.col]:
            neighbors.append(self.maze.cells[cell.row+1][cell.col])
        if cell.col < self.maze.ncol-1 and not self.visited[cell.row][cell.col+1]:
            neighbors.append(self.maze.cells[cell.row][cell.col+1])
        return neighbors

    def remove_wall(self, cell1: Cell, cell2: Cell):
        if cell1.row == cell2.row:
            if cell1.col < cell2.col:
                cell1.walls[1] = False
                cell2.walls[3] = False
            else:
                cell1.walls[3] = False
                cell2.walls[1] = False
        else:
            if cell1.row < cell2.row:
                cell1.walls[2] = False
                cell2.walls[0] = False
            else:
                cell1.walls[0] = False
                cell2.walls[2] = False

    def generate(self):
        if self.stack:
            self.current = self.stack[-1]
            neighbors = self.get_neighbors(self.current)
            if neighbors:
                neighbor = random.choice(neighbors)
                self.remove_wall(self.current, neighbor)
                self.visited[neighbor.row][neighbor.col] = True
                self.stack.append(neighbor)
            else:
                self.closed.append(self.stack.pop())
