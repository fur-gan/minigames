import pygame
import time
from dataclasses import dataclass

def p2c(col, row):
    x = ((Coin.LEFT_GAP + Coin.DIAMETER) * col) - (Board.MARGIN_SIDE / 2)
    y = ((Coin.TOP_GAP + Coin.DIAMETER) * row) + (Board.MARGIN_TOP / 1.5)
    return x, y

def isDiagonalWin(slot):
    return False

def isVerticalWin(slot):
    if slot.coin.color == Color.WHITE:
        return False

    count = 1
    for row in range(slot.position.row + 1, Board.ROWS):
        if board.rows[row][slot.position.col].coin.color == slot.coin.color:
            count += 1
            if count == 4:
                return True
        else:
            break

    return False

def isHorizontalWin(slot):
    if slot.position.col + 4 >= Board.COLUMNS:
        return False
    
    if slot.coin.color == Color.WHITE:
        return False

    count = 1
    for row in board.rows:
        for col in range(slot.position.col, slot.position.col + 4):
            if slot.coin.color == row[col].coin.color:
                count += 1
                if count >= 4:
                    return True
            else:
                count = 1
                break
    return False

def isGameOver():
    for columns in board.rows:
        for slot in columns:
            if isHorizontalWin(slot) or isVerticalWin(slot) or isDiagonalWin(slot):
                return True
    return False

class Player:
    def __init__(self, color):
        self.color = color

    def putCoin(self, col):
        for row in range(Board.ROWS - 1, -1, -1):
            if board.rows[row][col].coin.color == Color.WHITE:
                board.rows[row][col].coin.color = self.color
                return True
        return False

@dataclass
class Position:
    row: int
    col: int

@dataclass
class Window:
    WIDTH = 900
    HEIGHT = 700
    FPS = 10

@dataclass
class Color:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    YELLOW = (255, 255, 0)

class Board:
    MARGIN_TOP = 100
    MARGIN_BOTTOM = 20
    MARGIN_SIDE = 20
    WIDTH = Window.WIDTH - (MARGIN_SIDE * 2)
    HEIGHT = Window.HEIGHT - MARGIN_TOP - MARGIN_BOTTOM
    COLOR = Color.BLUE

    ROWS = 6
    COLUMNS = 7

    def __init__(self):
        self.rows = []
        for row in range(Board.ROWS):
            self.rows.append([])
            for col in range(Board.COLUMNS):
                self.rows[row].append(Slot(Position(row, col), coin=Coin(col, row, Color.WHITE)))

    def draw(self):
        pygame.draw.rect(screen,
                        Color.BLUE,
                        (Board.MARGIN_SIDE,
                        Board.MARGIN_TOP,
                        Board.WIDTH,
                        Board.HEIGHT))

        for columns in self.rows:
            for slot in columns:
                slot.coin.draw()

@dataclass
class Coin:
    RADIUS = 30
    DIAMETER= RADIUS * 2

    TOP_GAP = int((Board.HEIGHT - (Board.ROWS * RADIUS  * 2)) / (Board.ROWS + 1))
    LEFT_GAP = int((Board.WIDTH - (Board.COLUMNS * RADIUS  * 2)) / (Board.COLUMNS + 1))

    def __init__(self, col, row, color):
        self.col = col + 1
        self.row = row + 1
        self.color = color

    def draw(self):
        pygame.draw.circle(screen,
                         self.color,
                         p2c(self.col, self.row),
                         self.RADIUS)
        pygame.draw.circle(screen,
                    Color.BLACK,
                    p2c(self.col, self.row),
                    self.RADIUS, 4)

@dataclass
class Slot:
    position: Position
    coin: Coin | None

class Cursor:
    HEIGHT = 30
    WIDTH = 55

    def __init__(self):
        self.col = 0
        self.x, _ = p2c(self.col, 0)
        self.y = Board.MARGIN_TOP - Cursor.HEIGHT

    def draw(self):
        pygame.draw.polygon(
            screen,
            players[0 if myTurn else 1].color,
            (
                (self.x + (Cursor.WIDTH / 2) + Coin.DIAMETER, self.y - Cursor.HEIGHT),
                (self.x + (Cursor.WIDTH * 1.5) + Coin.DIAMETER, self.y - Cursor.HEIGHT),
                (self.x + Cursor.WIDTH + Coin.DIAMETER, self.y)
            )
        )

        pygame.draw.polygon(
            screen,
            Color.BLACK,
            (
                (self.x + (Cursor.WIDTH / 2) + Coin.DIAMETER, self.y - Cursor.HEIGHT),
                (self.x + (Cursor.WIDTH * 1.5) + Coin.DIAMETER, self.y - Cursor.HEIGHT),
                (self.x + Cursor.WIDTH + Coin.DIAMETER, self.y)
            ),
            4
        )

    def left(self):
        self.col = self.col - 1 if self.col > 0 else 0
        self.x, _ = p2c(self.col, 0)

    def right(self):
        self.col = self.col + 1 if self.col < Board.COLUMNS - 1 else Board.COLUMNS - 1
        self.x, _ = p2c(self.col, 0)

if __name__ == '__main__':
    pygame.init()
    gameOver = False
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((Window.WIDTH, Window.HEIGHT))

    board = Board()
    cursor = Cursor()
    players = [Player(Color.RED), Player(Color.YELLOW)]
    myTurn = False

    FONT_SIZE = 180
    text_font = pygame.font.SysFont(None, FONT_SIZE)
    text_surface = text_font.render(f'{'RED' if myTurn else 'YELLOW'} wins', True, Color.BLACK, Color.WHITE)
    x = 30
    y = text_surface.get_height() + 100

    while not gameOver:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameOver = True
            elif event.type == pygame.KEYDOWN:
                if event.key == ord('a'):
                    cursor.left()
                elif event.key == ord('d'):
                    cursor.right()
                elif event.key == pygame.K_SPACE:
                    if players[0 if myTurn else 1].putCoin(cursor.col):
                        myTurn = not myTurn

        screen.fill(Color.WHITE)

        board.draw()
        cursor.draw()

        gameOver = isGameOver()

        pygame.display.flip()
        clock.tick(Window.FPS)

    screen.blit(text_surface, (x, y))
    pygame.display.flip()
    time.sleep(3)