import random, pygame, sys
from pygame.locals import *

FPS = 100
##WINDOWWIDTH = 640
#WINDOWHEIGHT = 480
WINDOWWIDTH = 600
WINDOWHEIGHT = 480
CELLSIZE = 60
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

def into_queue((x, y), queue, visited, worm,apple):
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
    else:
        return True

def is_snake(x,y,worm):
    for body in worm:
        if body['x'] == x and body['y'] == y:
            return True
    return False


def cal_distance(worm,apple):
    queue = [(apple['x'],apple['y'])]
    visited = []
    found = False
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
            if into_queue(grid, queue, visited,worm,apple):
                if grid[0] == worm[HEAD]['x'] and grid[1] == worm[HEAD]['y']:
                    found = True
                if not is_snake(grid[0],grid[1],worm):
                    queue.append(grid)
                    distance[grid[1]][grid[0]] = distance[head[1]][head[0]] + 1
        queue.pop(0)
    return found

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

def virtual_run(wormCoords, apple,direction):
    wormCoords = list(wormCoords)
    food_eated = False
    while not food_eated:
        cal_distance(wormCoords,apple)
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
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['y'] == CELLHEIGHT:
            return # game over
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                return

        # move the worm by adding a segment in the direction it is moving
        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}
        if wormCoords[HEAD]['x'] != apple['x'] or wormCoords[HEAD]['y'] != apple['y']:
            food_eated = True
            wormCoords.insert(0, newHead)
        else:
            del wormCoords[-1] # remove worm's tail segment
            wormCoords.insert(0, newHead)
    result = cal_distance(wormCoords,wormCoords[-1])
    for i in range(4):
        temp = update_dirc(wormCoords[HEAD],DIRECTION[i])
        if temp['x'] == wormCoords[-1]['x'] and temp['y'] == wormCoords[-1]['y']:
            result = False
    return result

def distance_(x,y):
    return abs(x['x']-y['x']) + abs(x['y'] - x['y'])


def any_possible_move(worm,apple,direction):
    temp_direc = direction
    max_dis = 0
    for i in range(4):
        temp = update_dirc(worm[0],DIRECTION[i])
        if can_move((temp['x'],temp['y']),worm):
            if (distance_(temp, apple) > max_dis) and (examine_direction(DIRECTION[i], direction)):
                max_dis = distance_(temp, apple)
                temp_direc = DIRECTION[i]
    return temp_direc

def examine_direction(temp , direction):
    if direction == UP:
        if temp == DOWN:
            return False
    elif direction == RIGHT:
        if temp == LEFT:
            return False
    elif direction == LEFT:
        if temp == RIGHT:
            return False
    elif direction == DOWN:
        if temp == UP:
            return False
    return True

def check_head(worm,direction):
    for i in range(4):
        temp = update_dirc(worm[HEAD], DIRECTION[i])
        if can_move((temp['x'],temp['y']),worm) and examine_direction(DIRECTION[i],direction):
            if distance[temp['y']][temp['x']] < 9999:
                return True
    return False


def runGame():
    global running_,DIRECTION
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
    count = 0
    while True: # main game loop
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
        new_direction = None
        #print distance[wormCoords[HEAD]['y']][wormCoords[HEAD]['x']]
        if cal_distance(wormCoords,apple):
            #print "Test"
            if virtual_run(wormCoords, apple, direction):
                cal_distance(wormCoords,apple)
                four_dis = [99999] * 4
                if can_move((wormCoords[HEAD]['x'], wormCoords[HEAD]['y'] - 1), wormCoords):
                    four_dis[0] = distance[wormCoords[HEAD]['y'] - 1][wormCoords[HEAD]['x']]

                if can_move((wormCoords[HEAD]['x'] + 1, wormCoords[HEAD]['y']), wormCoords):
                    four_dis[1] = distance[wormCoords[HEAD]['y']][wormCoords[HEAD]['x'] + 1]

                if can_move((wormCoords[HEAD]['x'], wormCoords[HEAD]['y'] + 1), wormCoords):
                    four_dis[2] = distance[wormCoords[HEAD]['y'] + 1][wormCoords[HEAD]['x']]

                if can_move((wormCoords[HEAD]['x'] - 1, wormCoords[HEAD]['y']), wormCoords):
                    four_dis[3] = distance[wormCoords[HEAD]['y']][wormCoords[HEAD]['x'] - 1]

                max_num = min(four_dis)

                if four_dis[0] < 99999 and distance[wormCoords[HEAD]['y'] - 1][wormCoords[HEAD]['x']] == max_num and direction != DOWN:
                    new_direction = UP

                elif four_dis[1] < 99999 and distance[wormCoords[HEAD]['y']][wormCoords[HEAD]['x'] + 1] == max_num and direction != LEFT:
                    new_direction = RIGHT

                elif four_dis[2] < 99999 and distance[wormCoords[HEAD]['y'] + 1][wormCoords[HEAD]['x']] == max_num and direction != UP:
                    new_direction = DOWN

                elif four_dis[3] < 99999 and distance[wormCoords[HEAD]['y']][wormCoords[HEAD]['x'] - 1] == max_num and direction != RIGHT:
                    new_direction = LEFT
            else:
                count += 1
                print count
                four_dis = [-1] * 4
                cal_distance(wormCoords, wormCoords[-1])
                if can_move((wormCoords[HEAD]['x'], wormCoords[HEAD]['y'] - 1), wormCoords):
                    four_dis[0] = distance[wormCoords[HEAD]['y'] - 1][wormCoords[HEAD]['x']]

                if can_move((wormCoords[HEAD]['x'] + 1, wormCoords[HEAD]['y']), wormCoords):
                    four_dis[1] = distance[wormCoords[HEAD]['y']][wormCoords[HEAD]['x'] + 1]

                if can_move((wormCoords[HEAD]['x'], wormCoords[HEAD]['y'] + 1), wormCoords):
                    four_dis[2] = distance[wormCoords[HEAD]['y'] + 1][wormCoords[HEAD]['x']]

                if can_move((wormCoords[HEAD]['x'] - 1, wormCoords[HEAD]['y']), wormCoords):
                    four_dis[3] = distance[wormCoords[HEAD]['y']][wormCoords[HEAD]['x'] - 1]

                max_num = 0
                for i in four_dis:
                    if i != 9999:
                        if i > max_num:
                            max_num = i

                if four_dis[0] > -1 and distance[wormCoords[HEAD]['y'] - 1][wormCoords[HEAD]['x']] == max_num and direction != DOWN:
                    new_direction = UP

                elif four_dis[1] > -1 and distance[wormCoords[HEAD]['y']][wormCoords[HEAD]['x'] + 1] == max_num and direction != LEFT:
                    new_direction = RIGHT

                elif four_dis[2] > -1 and distance[wormCoords[HEAD]['y'] + 1][wormCoords[HEAD]['x']] == max_num and direction != UP:
                    new_direction = DOWN

                elif four_dis[3] > -1 and distance[wormCoords[HEAD]['y']][wormCoords[HEAD]['x'] - 1] == max_num and direction != RIGHT:
                    new_direction = LEFT
                if count == 10:
                    new_direction = any_possible_move(wormCoords, apple, direction)
                    count = 0
        else:
            four_dis = [-1] * 4
            cal_distance(wormCoords, wormCoords[-1])
            if can_move((wormCoords[HEAD]['x'], wormCoords[HEAD]['y'] - 1), wormCoords):
                four_dis[0] = distance[wormCoords[HEAD]['y'] - 1][wormCoords[HEAD]['x']]

            if can_move((wormCoords[HEAD]['x'] + 1, wormCoords[HEAD]['y']), wormCoords):
                four_dis[1] = distance[wormCoords[HEAD]['y']][wormCoords[HEAD]['x'] + 1]

            if can_move((wormCoords[HEAD]['x'], wormCoords[HEAD]['y'] + 1), wormCoords):
                four_dis[2] = distance[wormCoords[HEAD]['y'] + 1][wormCoords[HEAD]['x']]

            if can_move((wormCoords[HEAD]['x'] - 1, wormCoords[HEAD]['y']), wormCoords):
                four_dis[3] = distance[wormCoords[HEAD]['y']][wormCoords[HEAD]['x'] - 1]

            max_num = 0
            for i in four_dis:
                if i != 9999:
                    if i > max_num:
                        max_num = i

            if four_dis[0] > -1 and distance[wormCoords[HEAD]['y'] - 1][wormCoords[HEAD]['x']] == max_num and direction != DOWN:
                new_direction = UP

            elif four_dis[1] > -1 and distance[wormCoords[HEAD]['y']][wormCoords[HEAD]['x'] + 1] == max_num and direction != LEFT:
                new_direction = RIGHT

            elif four_dis[2] > -1 and distance[wormCoords[HEAD]['y'] + 1][wormCoords[HEAD]['x']] == max_num and direction != UP:
                new_direction = DOWN

            elif four_dis[3] > -1 and distance[wormCoords[HEAD]['y']][wormCoords[HEAD]['x'] - 1] == max_num and direction != RIGHT:
                new_direction = LEFT
        if new_direction == None:
            direction = any_possible_move(wormCoords, apple, direction)
        else:
            direction = new_direction
        #temp_ = update_dirc(wormCoords[HEAD],direction)
        #while not can_move((temp_['x'],temp_['y']), wormCoords):
            #direction = any_possible_move(wormCoords, apple, direction)
        # check if the worm has hit itself or the edge
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['y'] == CELLHEIGHT:
            return # game over
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                return # game over

        # check if worm has eaten an apply
        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
            # don't remove worm's tail 
            apple = getRandomLocation(wormCoords)
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
        wormCoords.insert(0, newHead) # set a new apple somewhere
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
        FPSCLOCK.tick(FPS)
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

def test_not_ok(temp, worm):
    for body in worm:
        if temp['x'] == body['x'] and temp['y'] == body['y']:
            return True
    return False


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