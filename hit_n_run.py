import os
import curses
import time

class Game:
    def __init__(self, stdscr, trm_col, trm_row):
        self.stdscr = stdscr
        self.trm_col = trm_col
        self.trm_row = trm_row
        self.player = Player(3, self.trm_row - 3)

    def drawFloor(self):
        floorTiles = self.trm_col * '_'
        self.stdscr.addstr(floorTiles)

    def drawPlayer(self):
        self.stdscr.addstr(self.player.y, self.player.x, self.player.get_frame())

    def walkPlayer(self, dx):
        if dx > 0 and self.player.x < self.trm_col or dx < 0 and self.player.x > 0:
            self.player.walk(dx)

    def jumpPlayer(self, dy):
        if dy > 0 and self.player.y < 0:
            self.player.jump(dy)

    def idlePlayer(self):
        if self.player.y == self.trm_row - 3:
            # On floor
            self.player.walk(0)
        else:
            self.player.jump(-1)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.frames_index = 0
        self.frames_idle = ['🧍🏻‍♂️']
        self.frames_walk_r = ['🚶🏻‍♂️‍➡️', '🏃🏻‍♂️‍➡️']
        self.frames_walk_l = ['🚶🏻‍♂️', '🏃🏻‍♂️']
        self.frames_current = self.frames_idle

    def get_frame(self):
        return self.frames_current[self.frames_index]

    def next_frame(self):
        if self.frames_index >= len(self.frames_current) - 1:
            self.frames_index = 0
        else:
            self.frames_index += 1

    def walk(self, dx):
        self.x += dx

        if dx > 0:
            self.frames_current = self.frames_walk_r
        elif dx < 0:
            self.frames_current = self.frames_walk_l
        else:
            self.frames_current = self.frames_idle

        self.next_frame()

    def jump(self, dy):
        self.y -= dy

        if self.frames_current == self.frames_idle:
            self.frames_current = self.frames_walk_r
        self.frames_index = 1

def main(stdscr):

    trm_col, trm_row = os.get_terminal_size()

    curses.curs_set(0)          # Hide cursor
    stdscr.nodelay(True)        # Non-blocking input
    stdscr.timeout(10)          # Refresh every 50 ms (~20 FPS)

    game = Game(stdscr, trm_col, trm_row)

    while True:
        key = stdscr.getch()

        if key == ord('q'):
            break
        elif key == ord('a'):
            game.walkPlayer(-1)
        elif key == ord('d'):
            game.walkPlayer(1)
        elif key == ord('w'):
            game.player.jump(1)
        else: # idle
            game.idlePlayer()


        stdscr.clear()

        game.drawFloor()
        game.drawPlayer()
        # stdscr.addstr(y, x, "@")   # Player
        stdscr.addstr(0, 0, "Press Q to quit")
        stdscr.refresh()

        time.sleep(0.02)

curses.wrapper(main)
