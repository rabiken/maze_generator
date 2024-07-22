import pygame as pg
from maze import *

# Initialize Pygame
pg.init()

# Set the width and height of the window
WIDTH = 1200
HEIGHT = 800
SIDE_LEN = 12
WALL_WEIGHT = SIDE_LEN // 2
WALL_LEN = SIDE_LEN + WALL_WEIGHT*2

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
CELL_COLOR = (0xf2, 0xa4, 0x7d)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Create the window
window = pg.display.set_mode((WIDTH, HEIGHT))

# Set the title of the window
pg.display.set_caption("MAZE GENERATOR")

def draw_square(x, y, size, color=(255,255,255)):
    pg.draw.rect(window, color, (x, y, size, size))

def draw_cell(x, y, walls, color=CELL_COLOR):
    draw_square(x - WALL_WEIGHT, y - WALL_WEIGHT, WALL_LEN, color)
    if walls[0]:
        pg.draw.rect(window, BLACK, (x - WALL_WEIGHT, y - WALL_WEIGHT, WALL_LEN, WALL_WEIGHT))
    if walls[1]:
        pg.draw.rect(window, BLACK, (x + SIDE_LEN, y - WALL_WEIGHT, WALL_WEIGHT, WALL_LEN))
    if walls[2]:
        pg.draw.rect(window, BLACK, (x - WALL_WEIGHT, y + SIDE_LEN, WALL_LEN, WALL_WEIGHT))
    if walls[3]:
        pg.draw.rect(window, BLACK, (x - WALL_WEIGHT, y - WALL_WEIGHT, WALL_WEIGHT, WALL_LEN))

    # pg.draw.circle(window, RED, (x-WALL_WEIGHT, y-WALL_WEIGHT), 1)
    # pg.draw.circle(window, RED, (x-WALL_WEIGHT, y+ SIDE_LEN+WALL_WEIGHT), 1)
    # pg.draw.circle(window, RED, (x+ SIDE_LEN+WALL_WEIGHT, y-WALL_WEIGHT), 1)
    # pg.draw.circle(window, RED, (x+ SIDE_LEN+WALL_WEIGHT, y+ SIDE_LEN+WALL_WEIGHT), 1)

def get_maze_size(maze: Maze) -> tuple:
    return maze.nrow * WALL_LEN, maze.ncol * WALL_LEN

def draw_maze(maze: Maze):
    offset_x = (WIDTH - get_maze_size(maze)[1]) // 2
    offset_y = (HEIGHT - get_maze_size(maze)[0]) // 2
    for i in range(maze.nrow):
        for j in range(maze.ncol):
            cell = maze.cells[i][j]
            x = j * WALL_LEN + offset_x
            y = i * WALL_LEN + offset_y
            draw_cell(x, y, cell.walls)

def draw_generating_process(gen: MazeGenerator):
    offset_x = (WIDTH - get_maze_size(gen.maze)[1]) // 2
    offset_y = (HEIGHT - get_maze_size(gen.maze)[0]) // 2
    for i in range(gen.maze.nrow):
        for j in range(gen.maze.ncol):
            color = BLACK
            if gen.closed.count(gen.maze.cells[i][j]):
                color = CELL_COLOR
            elif gen.current.row == i and gen.current.col == j:
                color = RED
            elif gen.visited[i][j]:
                color = GREEN
            cell = gen.maze.cells[i][j]
            x = j * WALL_LEN + offset_x
            y = i * WALL_LEN + offset_y
            draw_cell(x, y, cell.walls, color)


# Main game loop

running = True
clock = pg.time.Clock()
fps = 60

while True:
    try:
        nrow = int(input("Enter the number of rows: "))
        ncol = int(input("Enter the number of columns: "))
        break
    except ValueError:
        print("Please enter a valid integer.")

maze = Maze(nrow, ncol)
generator = MazeGenerator(maze, (random.randint(0, nrow-1), random.randint(0, ncol-1)))

while running:
    # Handle events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:  # Check if a key is pressed
            if event.key == pg.K_ESCAPE:  # Check if the key is the Escape key
                running = False

    # Update game logic
    generator.generate()
    # Render graphics

    window.fill(GRAY)
    # draw_maze(generator.maze)
    draw_generating_process(generator)

    # Update the display
    pg.display.update()

    clock.tick(fps)
# Quit Pygame
pg.quit()