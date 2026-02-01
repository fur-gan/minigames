import os
import sys
import curses
import time
import random
from dataclasses import dataclass

def getRandomVehicle():
    VEHICLE_IMGS = ['🚌','🚐','🚑','🚕','🚜','🚛','🚚','🚙','🚗']
    return VEHICLE_IMGS[random.randint(0, len(VEHICLE_IMGS) - 1)]

def getRandomTree():
    TREE_IMGS = ['🌲', '🌳', '🌴', '🎄']
    return TREE_IMGS[random.randint(0, len(TREE_IMGS) - 1)]

@dataclass
class Object:
    x: int
    y: int

@dataclass
class Player(Object):
    img: str = '🏍️'

@dataclass
class Vehicle(Object):
    img: str
    
@dataclass
class Tree(Object):
    img: str

@dataclass
class LaneLine(Object):
    img: str = '___'

def main(stdscr):
    WIDTH = 50
    HEIGHT = 50
    WIDTH, HEIGHT = os.get_terminal_size()

    if WIDTH < WIDTH and HEIGHT < HEIGHT:
        print(f'Window too small - Required size at least {WIDTH}x{HEIGHT}')
        sys.exit(1)

    def updateVehicles(randomizer):
        nonlocal vehicles
        if random.random() < randomizer:
            x = 2
            lane = random.randrange(SIDEWALK_OFFSET, HEIGHT - SIDEWALK_OFFSET + 1, 2)
            vehicles.append(Vehicle(x, lane, getRandomVehicle()))

    def initTrees():
        TREE_OFFSET = 5
        yTop = TREE_OFFSET - 3
        yBot = HEIGHT - TREE_OFFSET + 3
        trees = []

        for i in range(round(WIDTH / TREE_OFFSET)):
            x = TREE_OFFSET * i
            trees.append(Tree(x, yTop, getRandomTree()))
            trees.append(Tree(x, yBot, getRandomTree()))
        return trees

    def initLaneLines():
        laneLines = []
        LANE_LINE_OFFSET = 7
        for y in range(3, HEIGHT - 3, 2):
            for x in range(round(WIDTH / LANE_LINE_OFFSET)):
                laneLines.append(LaneLine(x * LANE_LINE_OFFSET, y))
        return laneLines

    def drawPlayer():
        stdscr.addstr(player.y, player.x, player.img)

    def drawSidewalk():
        stdscr.addstr(SIDEWALK_OFFSET - 1, 0, '_' * WIDTH)
        stdscr.addstr(HEIGHT - SIDEWALK_OFFSET + 1, 0, '_' * WIDTH)

    def drawTree():
        nonlocal trees
        for tree in trees:
            stdscr.addstr(tree.y, tree.x, tree.img)

    def drawLaneLine():
        nonlocal laneLines
        for laneLine in laneLines:
            stdscr.addstr(laneLine.y, laneLine.x, laneLine.img)

    def drawVehicle():
        nonlocal vehicles
        for vehicle in vehicles:
            stdscr.addstr(vehicle.y, vehicle.x, vehicle.img)

    def passTime():
        nonlocal distance
        nonlocal trees
        nonlocal laneLines
        nonlocal vehicles

        distance += 1

        for tree in trees:
            tree.x = tree.x + 1 if tree.x < WIDTH - 1 else 0

        for laneLine in laneLines:
            laneLine.x = laneLine.x + 1 if laneLine.x < WIDTH - 1 else 0

        tmp = []
        for vehicle in vehicles:
            if vehicle.x < WIDTH - 1:
                vehicle.x += 1
                tmp.append(vehicle)
        vehicles = tmp

    def checkCollision():
        nonlocal gameOver

        for vehicle in vehicles:
            if vehicle.x == player.x and vehicle.y == player.y:
                player.img = '💥'
                gameOver = True

    def switchLane(direction):
        if direction == UP and player.y > SIDEWALK_OFFSET or direction == DOWN and player.y < HEIGHT - SIDEWALK_OFFSET:
            player.y += direction

    curses.curs_set(0)          # Hide cursor
    stdscr.nodelay(True)        # Non-blocking input
    stdscr.timeout(10)          # Refresh every 50 ms (~20 FPS)

    UP = -2
    DOWN = 2
    SIDEWALK_OFFSET = 4

    gameOver = False
    playerY = round(HEIGHT / 2)
    player = Player(WIDTH - SIDEWALK_OFFSET - 10, playerY if playerY % 2 == 0 else playerY + 1)
    distance = 0
    timeout = 0.02

    vehicles = []
    trees = initTrees()
    laneLines = initLaneLines()

    while not gameOver:
        key = stdscr.getch()

        if key == ord('q'):
            break
        elif key == ord('w'):
            switchLane(UP)
        elif key == ord('s'):
            switchLane(DOWN)

        stdscr.clear()

        drawSidewalk()
        drawTree()
        drawLaneLine()
        drawVehicle()
        checkCollision()
        drawPlayer()
        updateVehicles(0.1)
        passTime()

        stdscr.addstr(0, 0, 'Press Q to quit')
        stdscr.addstr(1, 0, f'Distance: {distance}')
        stdscr.refresh()

        if gameOver:
            time.sleep(2)
        else:
            timeout -= 0.0001
            if timeout < 0:
                timeout = 0
            time.sleep(timeout)


if __name__ == '__main__':
    curses.wrapper(main)
