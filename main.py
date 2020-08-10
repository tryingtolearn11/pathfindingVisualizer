import pygame
import queue

SCREENWIDTH = 1000
SCREENHEIGHT = 1000
BORDERWIDTH = 800
BORDERHEIGHT = 800
CELLSIZE = 30
ROWS = BORDERWIDTH // CELLSIZE
COLS = BORDERHEIGHT // CELLSIZE
print("ROWS: ", ROWS, "COLS: ", COLS)
FPS = 30

XMARGIN = int((SCREENWIDTH - (CELLSIZE * ROWS + (COLS - 1)))/2)
YMARGIN = int((SCREENHEIGHT - (CELLSIZE * COLS + (ROWS - 1))) / 2)


BLUE = (0, 100, 200)
Black = (0, 0, 0)
White = (255, 255, 255)
Green = (0, 200, 100)
Red = (200, 50, 50)
Yellow = (255, 255, 0)


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
        self.reached = False
        self.path = False

    # Comparison operator defined
    def __lt__(ob1, ob2):
        return (ob1.x, ob1.y) < (ob2.x, ob2.y)

    def resetNodes(self):
        self.wall = False
        self.currentStart = False
        self.currentEnd = False
        self.reached = False
        self.path = False

    def drawNODE(self, surface):
        if self.wall:
            pygame.draw.rect(surface, Black, self.body)
        elif not self.wall:
            pygame.draw.rect(surface, White, self.body)
        if self.currentStart:
            pygame.draw.rect(surface, Green, self.body)
        if self.currentEnd:
            pygame.draw.rect(surface, Red, self.body)
        if self.reached:
            if not self.currentStart and not self.currentEnd and not self.path:
                pygame.draw.rect(surface, BLUE, self.body)
            elif self.path and not self.currentEnd:
                pygame.draw.rect(surface, Yellow, self.body)

    # Counts all neighbors including adjacent
    def getNeighbors(self, grid):
        self.neighbors = []
        if not self.wall:
            if self.y > 0:
                top = grid[self.x][self.y - 1]
            else:
                top = None
            if self.x < len(grid) - 1:
                right = grid[self.x + 1][self.y]
            else:
                right = None
            if self.y < len(grid[i]) - 1:
                bottom = grid[self.x][self.y + 1]
            else:
                bottom = None
            if self.x > 0:
                left = grid[self.x - 1][self.y]
            else:
                left = None
            if self.y > 0 and self.x > 0:
                topleft = grid[self.x - 1][self.y - 1]
            else:
                topleft = None
            if self.y > 0 and self.x < len(grid) - 1:
                topright = grid[self.x + 1][self.y - 1]
            else:
                topright = None
            if self.y < len(grid[i]) - 1 and self.x > 0:
                bottomleft = grid[self.x - 1][self.y + 1]
            else:
                bottomleft = None
            if self.y < len(grid[i]) - 1 and self.x < len(grid[i]) - 1:
                bottomright = grid[self.x + 1][self.y + 1]
            else:
                bottomright = None

            if top and not top.wall:
                self.neighbors.append(top)
            if right and not right.wall:
                self.neighbors.append(right)
            if bottom and not bottom.wall:
                self.neighbors.append(bottom)
            if left and not left.wall:
                self.neighbors.append(left)
            if topleft and not topleft.wall:
                self.neighbors.append(topleft)
            if topright and not topright.wall:
                self.neighbors.append(topright)
            if bottomleft and not bottomleft.wall:
                self.neighbors.append(bottomleft)
            if bottomright and not bottomright.wall:
                self.neighbors.append(bottomright)


grid = []
for i in range(ROWS):
    column = []
    for j in range(COLS):
        node = Node(i, j)
        column.append(node)
    grid.append(column)

# Lets add weights to the graph
weights = {}


# Cost = 1 between two neighbors
def cost(grid, current, next):
    return weights.get(next, 1)


def dijkstra(grid, STARTPOSITION, ENDPOSITION):
    q = queue.PriorityQueue()
    q.put(STARTPOSITION, 0)
    parentCell = {}
    costOfPath = {}
    parentCell[STARTPOSITION] = None
    costOfPath[STARTPOSITION] = 0
    print("ENDPOSITION", ENDPOSITION)

    while not q.empty():
        current = q.get()

        if current == ENDPOSITION:
            print("FOUND END")
            break

        current.getNeighbors(grid)
        for next in current.neighbors:
            # Update the cost for the path
            newCost = costOfPath[current] + cost(grid, current, next)
            if next not in costOfPath or newCost < costOfPath[next]:
                costOfPath[next] = newCost
                priority = newCost
                q.put(next, priority)
                #print("priority", priority)
                #print("newCost", newCost)
                #print("COST OF PATH[CURRENT]", costOfPath[current])
                #print("COST", cost(grid, current, next))
                parentCell[next] = current
                next.reached = True

    return parentCell


def reconstructPath(parentCell, STARTPOSITION, ENDPOSITION):
    current = ENDPOSITION
    path = []
    while current != STARTPOSITION:
        path.append(current)
        current.path = True
        current = parentCell[current]
    path.append(STARTPOSITION)
    path.reverse()

    return path


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
    pygame.draw.rect(surface, Red, (left-4, top-4, width+10, height+10), 5)
    drawGRID(surface)
    # BUTTONS
    surface.blit(STARTNODE_SURF, STARTNODE_RECT)
    surface.blit(ENDNODE_SURF, ENDNODE_RECT)
    surface.blit(BEGIN_SURF, BEGIN_RECT)
    surface.blit(RESET_SURF, RESET_RECT)


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


def reset(surface):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            grid[i][j].resetNodes()


def main():
    global grid, FPS, STARTNODE_SURF, STARTNODE_RECT, ENDNODE_SURF, ENDNODE_RECT, BASICFONT, markStartPos, markEndPos, STARTPOSITION, ENDPOSITION
    global BEGIN_SURF, BEGIN_RECT, RESET_SURF, RESET_RECT
    pygame.init()
    markStartPos = False
    markEndPos = False
    myWindow = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption("Visualizer")
    FPSclock = pygame.time.Clock()
    BASICFONT = pygame.font.SysFont('arial', 20)
    STARTNODE_SURF, STARTNODE_RECT = makeButton('Start Node', Black, Green, SCREENWIDTH - 900, SCREENHEIGHT - 950)
    ENDNODE_SURF, ENDNODE_RECT = makeButton('End Node', Black, Red, SCREENWIDTH - 200, SCREENHEIGHT - 950)
    BEGIN_SURF, BEGIN_RECT = makeButton('BEGIN SEARCH', Black, BLUE, SCREENWIDTH - 900, SCREENWIDTH - 90)
    RESET_SURF, RESET_RECT = makeButton('Reset', Black, White, SCREENWIDTH - 200, SCREENWIDTH - 90)
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
                            # print("Grid :", x, y)
                            grid[x][y].wall = True
                            grid[x][y].currentStart = False
                            grid[x][y].currentEnd = False
                            if markStartPos:
                                grid[x][y].currentStart = True
                                STARTPOSITION = grid[x][y]
                                grid[x][y].wall = False
                                grid[x][y].currentEnd = False
                                markStartPos = False
                            if markEndPos:
                                grid[x][y].currentEnd = True
                                grid[x][y].currentStart = False
                                ENDPOSITION = grid[x][y]
                                grid[x][y].wall = False
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

                if BEGIN_RECT.collidepoint(event.pos):
                    parentCell = dijkstra(grid, STARTPOSITION, ENDPOSITION)
                    reconstructPath(parentCell, STARTPOSITION, ENDPOSITION)

                if RESET_RECT.collidepoint(event.pos):
                    reset(myWindow)

        FPSclock.tick(FPS)
        display(myWindow)
        pygame.display.update()


if __name__ == '__main__':
    main()
