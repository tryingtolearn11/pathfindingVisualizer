import pygame
SCREENWIDTH = 1000
SCREENHEIGHT = 1000
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
        self.body = pygame.Rect(self.x, self.y, CELLSIZE, CELLSIZE)

    def drawNODE(self, surface):
        i = self.x * CELLSIZE + XMARGIN
        j = self.y * CELLSIZE + YMARGIN
        if self.wall:
            pygame.draw.rect(surface, Black, (i, j, CELLSIZE, CELLSIZE))
        elif not self.wall:
            pygame.draw.rect(surface, White, (i, j, CELLSIZE, CELLSIZE))


class Board:
    def __init__(self, ROWS, COLS):
        self.rows = ROWS
        self.cols = COLS
        self.grid = []
        for i in range(self.rows):
            self.column = []
            for j in range(self.cols):
                node = Node(i, j)
                self.column.append(node)
            self.grid.append(self.column)

    def drawGRID(self, surface):
        for i in range(self.rows):
            for j in range(self.cols):
                self.grid[i][j].drawNODE(surface)

        for x in range(XMARGIN, SCREENWIDTH, CELLSIZE):
            pygame.draw.line(surface, Black, (x, 0), (x, SCREENWIDTH))
        for y in range(YMARGIN, SCREENHEIGHT, CELLSIZE):
            pygame.draw.line(surface, Black, (0, y), (SCREENWIDTH, y))


def leftTopofTile(a, b):
    left = XMARGIN + (a * CELLSIZE) + (a - 1)
    top = YMARGIN + (b * CELLSIZE) + (b - 1)
    return(left, top)


def display(surface):
    surface.fill(Black)
    left, top = leftTopofTile(0, 0)
    width = COLS * CELLSIZE
    height = ROWS * CELLSIZE
    pygame.draw.rect(surface, BLUE, (left - 5, top - 5, width + 11, height + 10), 5)
    grid = Board(ROWS, COLS)
    grid.drawGRID(surface)


def getMouseClick(surface, xpos, ypos):
    global grid
    for i in range(SCREENWIDTH):
        for j in range(SCREENHEIGHT):
            left, top = leftTopofTile(xpos, ypos)
            tileSelector = pygame.Rect(left, top, CELLSIZE, CELLSIZE)
            if tileSelector.collidepoint(xpos, ypos):
                return(xpos, ypos)
    return (None, None)


def main():
    grid = Board(ROWS, COLS)
    pygame.init()
    myWindow = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption("Visualizer")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                xpos, ypos = getMouseClick(myWindow, event.pos[0], event.pos[1])
                for i in range(grid.rows):
                    for j in range(grid.cols):
                        if grid.grid[i][j].body.collidepoint(event.pos):
                            print(grid.grid[i][j])
                            grid.grid[i][j].wall = True





        display(myWindow)
        pygame.display.update()


if __name__ == '__main__':
    main()
