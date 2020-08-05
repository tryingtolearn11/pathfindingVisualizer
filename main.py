import pygame
SCREENWIDTH = 800
SCREENHEIGHT = 800
BORDERWIDTH = 600
BORDERHEIGHT = 600
CELLSIZE = 40
ROWS = BORDERWIDTH // CELLSIZE
COLS = BORDERHEIGHT // CELLSIZE
print("ROWS: ", ROWS, "COLS: ", COLS)

XMARGIN = int((SCREENWIDTH - (CELLSIZE * ROWS + (COLS - 1))) / 2)
YMARGIN = int((SCREENHEIGHT - (CELLSIZE * COLS + (ROWS - 1))) / 2)


BLUE = (0, 100, 200)
Black = (0, 0, 0)
White = (255, 255, 255)


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.wall = False

    def drawNODE(self, surface):
        i = self.x * CELLSIZE + XMARGIN
        j = self.y * CELLSIZE + YMARGIN
        if self.wall:
            pygame.draw.rect(surface, Black, (i, j, CELLSIZE, CELLSIZE))
        else:
            pygame.draw.rect(surface, White, (i, j, CELLSIZE, CELLSIZE))


class Board:
    def __init__(self, ROWS, COLS):
        self.rows = ROWS
        self.cols = COLS
        self.grid = []

    def drawGRID(self, surface):
        for i in range(self.rows):
            self.column = []
            for j in range(self.cols):
                node = Node(i, j)
                self.column.append(node)
            self.grid.append(self.column)


def display(surface):
    surface.fill(BLUE)


def main():
    pygame.init()
    myWindow = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption("Visualizer")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        display(myWindow)


if __name__ == '__main__':
    main()
