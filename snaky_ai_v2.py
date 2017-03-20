import random, pygame, sys
from pygame.locals import *

FPS = 80
##WINDOWWIDTH = 640
#WINDOWHEIGHT = 480
WINDOWWIDTH = 600
WINDOWHEIGHT = 480
CELLSIZE = 40
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
BGCOLOR = BLACK


apple = {'x':0,'y':0}

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

direction = UP
DIRECTION = [UP,DOWN,LEFT,RIGHT]

HEAD = 0 # syntactic sugar: index of the worm's head



distance = []

for y in range(CELLHEIGHT):
    distance.append([])
    for x in range(CELLWIDTH):
        distance[y].append(8888)

def into_queue((x, y), queue, visited, worm):
    if (x, y) == (apple['x'],apple['y']):
        return False
    elif x < 0 or x >= CELLWIDTH:
        return False
    elif y < 0 or y >= CELLHEIGHT:
        return False
    elif (x, y) in queue:
        return False
    elif (x, y) in visited:
        return False
    elif is_snake(x, y, worm):
        return False
    else:
        return True

def is_snake(x,y,worm):
    for body in worm:
        if body['x'] == x and body['y'] == y:
            return True
    return False


def cal_distance(worm):
    queue = [(apple['x'],apple['y'])]
    visited = []
    for y in range(CELLHEIGHT):
        for x in range(CELLWIDTH):
            distance[y][x] = 9999

    distance[apple['y']][apple['x']] = 0

    while len(queue) != 0:
        head = queue[0]
        visited.append(head)
        up_grid = head[0], head[1] - 1
        down_grid = head[0], head[1] + 1
        left_grid = head[0] - 1, head[1]
        right_grid = head[0] + 1, head[1]

        for grid in [up_grid, down_grid, left_grid, right_grid]:
            if into_queue(grid, queue, visited,worm):
                queue.append(grid)
                if distance[grid[1]][grid[0]] != 99999:
                    distance[grid[1]][grid[0]] = distance[head[1]][head[0]] + 1
        queue.pop(0)

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Snaky')

    showStartScreen()
    while True:
        runGame()
        showGameOverScreen()

def get_direction(head_, last_direction):
    if head_['x'] == 1:
        if head_['y'] == CELLHEIGHT - 1:
            return LEFT
        elif head_['y'] == 0:
            return RIGHT
        if last_direction == LEFT:
            return DOWN
        elif last_direction == DOWN:
            return RIGHT
    elif head_['x'] >= 1 and head_['x'] <= CELLWIDTH-2:
        if last_direction == RIGHT:
            return RIGHT
        elif last_direction == LEFT:
            return LEFT
    elif head_['x'] == (CELLWIDTH-1):
        if last_direction == RIGHT:
            return DOWN
        elif last_direction == DOWN:
            return LEFT
    elif head_['x'] == 0:
        if head_['y'] != 0:
            return UP
        else:
            return RIGHT

def can_move((x, y), worm):
    if x < 0 or x >= CELLWIDTH:
        return False
    elif y < 0 or y >= CELLHEIGHT:
        return False
    elif is_snake(x, y,worm):
        return False
    elif (x, y) == (worm[HEAD]['x'], worm[HEAD]['y']):
        return False
    else:
        return True

def test_not_ok(temp, worm):
    for body in worm:
        if temp['x'] == body['x'] and temp['y'] == body['y']:
            return True
    return False

def update_dirc(now, direc):
    loc = {'x':0,'y':0}
    if direc == UP:
        loc = {'x':now['x'],'y':now['y']-1}
    elif direc == DOWN:
        loc = {'x':now['x'],'y':now['y']+1}
    elif direc == RIGHT:
        loc = {'x':now['x']+1,'y':now['y']}
    elif direc == LEFT:
        loc = {'x':now['x']-1,'y':now['y']}
    return loc


def runGame():
    global running_,apple,DIRECTION
    # Set a random start point.
    startx = random.randint(0, CELLWIDTH -1)
    starty = random.randint(0, CELLHEIGHT -1)
    wormCoords = [{'x': startx,     'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]
    direction = RIGHT
    running_ = True
    # Start the apple in a random place.
    apple = getRandomLocation(wormCoords)
    cal_distance(wormCoords)
    while True: # main game loop
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
        four_dis = [99999, 99999, 99999, 99999]
        if can_move((wormCoords[HEAD]['x'], wormCoords[HEAD]['y'] - 1), wormCoords):
            four_dis[0] = distance[wormCoords[HEAD]['y'] - 1][wormCoords[HEAD]['x']]

        if can_move((wormCoords[HEAD]['x'] + 1, wormCoords[HEAD]['y']), wormCoords):
            four_dis[1] = distance[wormCoords[HEAD]['y']][wormCoords[HEAD]['x'] + 1]

        if can_move((wormCoords[HEAD]['x'], wormCoords[HEAD]['y'] + 1), wormCoords):
            four_dis[2] = distance[wormCoords[HEAD]['y'] + 1][wormCoords[HEAD]['x']]

        if can_move((wormCoords[HEAD]['x'] - 1, wormCoords[HEAD]['y']), wormCoords):
            four_dis[3] = distance[wormCoords[HEAD]['y']][wormCoords[HEAD]['x'] - 1]

        min_num = min(four_dis)

        if four_dis[0] < 99999 and distance[wormCoords[HEAD]['y'] - 1][wormCoords[HEAD]['x']] == min_num and direction != DOWN:
            direction = UP

        elif four_dis[1] < 99999 and distance[wormCoords[HEAD]['y']][wormCoords[HEAD]['x'] + 1] == min_num and direction != "LEFT":
            direction = RIGHT

        elif four_dis[2] < 99999 and distance[wormCoords[HEAD]['y'] + 1][wormCoords[HEAD]['x']] == min_num and direction != "UP":
            direction = DOWN

        elif four_dis[3] < 99999 and distance[wormCoords[HEAD]['y']][wormCoords[HEAD]['x'] - 1] == min_num and direction != RIGHT:
            direction = LEFT

        else:
            print direction
            index_ = 0
            for i in range(4):
                temp = update_dirc(wormCoords[HEAD],DIRECTION[i])
                if can_move(temp,wormCoords):
                    index_ = i
                    break
            direction_new = DIRECTION[index_]
            if direction == UP:
                if direction_new != DOWN:
                    direction = direction_new
            elif direction == DOWN:
                if direction_new != UP:
                    direction = direction_new
            elif direction == RIGHT:
                if direction_new != LEFT:
                    direction = direction_new            
            elif direction == LEFT:
                if direction_new != RIGHT:
                    direction = direction_new
            print direction
        # check if the worm has hit itself or the edge
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['y'] == CELLHEIGHT:
            return # game over
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                return # game over

        # check if worm has eaten an apply
        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
            # don't remove worm's tail segment
            apple = getRandomLocation(wormCoords) # set a new apple somewhere
        else:
            del wormCoords[-1] # remove worm's tail segment

        # move the worm by adding a segment in the direction it is moving
        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}
        wormCoords.insert(0, newHead)
        cal_distance(wormCoords)
        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawWorm(wormCoords)
        drawApple(apple)
        drawScore(len(wormCoords) - 3)
        pygame.display.update()
        #FPSCLOCK.tick(FPS)

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('Snaky!', True, WHITE, DARKGREEN)
    titleSurf2 = titleFont.render('Snaky!', True, GREEN)

    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
        pygame.display.update()
        #FPSCLOCK.tick(FPS)
        degrees1 += 3 # rotate by 3 degrees each frame
        degrees2 += 7 # rotate by 7 degrees each frame


def terminate():
    pygame.quit()
    sys.exit()

def getRandomLocation(worm):
    temp = {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}
    while test_not_ok(temp, worm):
        temp = {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}
    return temp


def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress() # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return

def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


def drawWorm(wormCoords):
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARKGREEN, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, GREEN, wormInnerSegmentRect)


def drawApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, appleRect)


def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))

running_ = True

if __name__ == '__main__':
    main()