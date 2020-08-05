import pygame
SCREENWIDTH = 1000
SCREENHEIGHT = 1000
BORDERWIDTH = 800
BORDERHEIGHT = 800
CELLSIZE = 30
ROWS = BORDERWIDTH // CELLSIZE
COLS = BORDERHEIGHT // CELLSIZE
print("ROWS: ", ROWS, "COLS: ", COLS)

XMARGIN = int((SCREENWIDTH - (CELLSIZE * ROWS + (COLS - 1)))/2)
YMARGIN = int((SCREENHEIGHT - (CELLSIZE * COLS + (ROWS - 1))) / 2)


BLUE = (0, 100, 200)
Black = (0, 0, 0)
White = (255, 255, 255)
Green = (0, 200, 100)
Red = (200, 50, 50)


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        i = self.x * CELLSIZE + XMARGIN
        j = self.y * CELLSIZE + YMARGIN
        self.wall = False
        self.body = pygame.Rect(i, j, CELLSIZE, CELLSIZE)
        self.currentStart = False
        self.currentEnd = False

    def drawNODE(self, surface):
        if self.wall:
            pygame.draw.rect(surface, Black, self.body)
        elif not self.wall:
            pygame.draw.rect(surface, White, self.body)
        if self.currentStart:
            pygame.draw.rect(surface, Green, self.body)
        if self.currentEnd:
            pygame.draw.rect(surface, Red, self.body)


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
    pygame.draw.rect(surface, BLUE, (left-4, top-4, width+10, height+10), 5)
    drawGRID(surface)
    surface.blit(STARTNODE_SURF, STARTNODE_RECT)
    surface.blit(ENDNODE_SURF, ENDNODE_RECT)


def getMouseClick(surface, xpos, ypos):
    global grid
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            left, top = leftTopofTile(xpos, ypos)
            tileSelector = pygame.Rect(left, top, CELLSIZE, CELLSIZE)
            if tileSelector.collidepoint(xpos, ypos):
                return(xpos, ypos)
    return (None, None)


def makeButton(text, color, bgcolor, top, left):
    textSurface = BASICFONT.render(text, True, color, bgcolor)
    textRect = textSurface.get_rect()
    textRect.topleft = (top, left)
    return (textSurface, textRect)


def main():
    global grid, STARTNODE_SURF, STARTNODE_RECT, ENDNODE_SURF, ENDNODE_RECT, BASICFONT, markStartPos, markEndPos, STARTPOSITION, ENDPOSITION
    pygame.init()
    markStartPos = False
    markEndPos = False
    myWindow = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption("Visualizer")
    BASICFONT = pygame.font.SysFont('arial', 20)
    STARTNODE_SURF, STARTNODE_RECT = makeButton('Start Node', Black, Green, SCREENWIDTH - 900, SCREENHEIGHT - 950)
    ENDNODE_SURF, ENDNODE_RECT = makeButton('End Node', Black, Red, SCREENWIDTH - 200, SCREENHEIGHT - 950)
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
                            if markStartPos:
                                grid[x][y].currentStart = True
                                STARTPOSITION = grid[x][y]
                                markStartPos = False
                            if markEndPos:
                                grid[x][y].currentEnd = True
                                ENDPOSITION = grid[x][y]
                                markEndPos = False
                if STARTNODE_RECT.collidepoint(event.pos):
                    markStartPos = True
                    for x in range(len(grid)):
                        for y in range(len(grid[x])):
                            if grid[x][y].currentStart:
                                grid[x][y].currentStart = False
                                grid[x][y].wall = False

                if ENDNODE_RECT.collidepoint(event.pos):
                    markEndPos = True
                    for x in range(len(grid)):
                        for y in range(len(grid[x])):
                            if grid[x][y].currentEnd:
                                grid[x][y].currentEnd = False
                                grid[x][y].wall = False


        display(myWindow)
        pygame.display.update()


if __name__ == '__main__':
    main()
