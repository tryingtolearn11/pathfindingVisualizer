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
        i = self.x * CELLSIZE + XMARGIN
        j = self.y * CELLSIZE + YMARGIN
        self.body = pygame.Rect(i, j, CELLSIZE, CELLSIZE)

    def drawNODE(self, surface):
        #i = self.x * CELLSIZE + XMARGIN
        #j = self.y * CELLSIZE + YMARGIN
        if self.wall:
            pygame.draw.rect(surface, Black, self.body)
        elif not self.wall:
            pygame.draw.rect(surface, White, self.body)


grid = []
for i in range(ROWS):
    column = []
    for j in range(COLS):
        node = Node(i, j)
        column.append(node)
    grid.append(column)

    def drawGRID(surface):
        for i in range(ROWS):
            for j in range(COLS):
                grid[i][j].drawNODE(surface)

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
    drawGRID(surface)


def getMouseClick(surface, xpos, ypos):
    global grid
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            left, top = leftTopofTile(xpos, ypos)
            tileSelector = pygame.Rect(left, top, CELLSIZE, CELLSIZE)
            if tileSelector.collidepoint(xpos, ypos):
                return(xpos, ypos)
    return (None, None)


def main():
    global grid
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
                for x in range(len(grid)):
                    for y in range(len(grid[x])):
                        if grid[x][y].body.collidepoint(event.pos):
                            print("Grid :", x, y)
                            grid[x][y].wall = True

        display(myWindow)
        pygame.display.update()


if __name__ == '__main__':
    main()
