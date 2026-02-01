import random
import pygame
import sys

MARGIN_LEFT = 50  # px
MARGIN_TOP = 50   # px
LINE_WIDTH = 5    # px
FONT_SIZE = 20
FPS = 30

BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

class Horizontal:
    def __init__(self, game, vertical_left, vertical_right, y):
        self.__game = game
        self.__vertical_left = vertical_left
        self.__vertical_right = vertical_right

        self.__start_pos = (self.__vertical_left.start_pos[0], y)
        self.__end_pos = (self.__vertical_right.start_pos[0], y)

    @property
    def start_pos(self):
        return self.__start_pos

    @property
    def end_pos(self):
        return self.__end_pos

    def get_next_vertical(self, current_vertical):
        return self.__vertical_right if current_vertical == self.__vertical_left else self.__vertical_left

    def draw(self):
        pygame.draw.line(self.__game.window, BLACK, self.__start_pos, self.__end_pos, LINE_WIDTH)

class Vertical:
    def __init__(self, game, name, result, index, start=False, end=False):
        self.__game = game
        self.__name = name
        self.__result = result
        self.__horizontals = {}
        self.__start = start
        self.__end = end

        self.__start_pos = (MARGIN_LEFT * index, MARGIN_TOP)
        self.__end_pos = (MARGIN_LEFT * index, MARGIN_TOP + self.__game.height)

    @property
    def name(self):
        return self.__name

    @property
    def result(self):
        return self.__result

    @property
    def horizontals(self):
        return self.__horizontals

    @property
    def start_pos(self):
        return self.__start_pos

    @property
    def end_pos(self):
        return self.__end_pos

    def get_horizontal(self, y):
        return self.__horizontals.get(y)

    def set_horizontal(self, y, horizontal):
        self.__horizontals[y] = horizontal

    def set_start(self):
        self.__start = True

    def set_end(self):
        self.__end = True

    def __write_name(self):
        text_surface = self.__game.label_font.render(self.__name, True, RED if self.__start else BLACK)
        text_width = text_surface.get_width()
        text_height = text_surface.get_height()
        self.__game.window.blit(text_surface, (self.__start_pos[0] - (text_width / 2), (self.__start_pos[1] + FONT_SIZE) - (text_height * 3)))

    def __write_result(self):
        text_surface = self.__game.label_font.render(self.__result, True, RED if self.__end else BLACK)
        text_width = text_surface.get_width()
        text_height = text_surface.get_height()
        self.__game.window.blit(text_surface, (self.__end_pos[0] - (text_width / 2), (self.__end_pos[1] + FONT_SIZE) - (text_height / 2)))

    def draw(self):
        pygame.draw.line(self.__game.window, BLACK, self.__start_pos, self.__end_pos, LINE_WIDTH)
        self.__write_name()
        self.__write_result()

class Game:
    def __init__(self):
        self.__results = sys.argv[1:len(sys.argv) - 1]
        self.__results_len = len(self.__results)
        self.__height = int(sys.argv[-1])

        self.__verticals = [
            Vertical(self, chr(ord('A') + i), result, i + 1)
            for i, result in enumerate(self.__results)
        ]

        self.__label_font = pygame.font.SysFont(None, FONT_SIZE)
        self.__window_width = self.__results_len * (MARGIN_LEFT * 2)
        self.__window_height = self.__height + (MARGIN_TOP * 3)
        self.__window = pygame.display.set_mode((self.__window_width, self.__window_height))

        self.__vertical_index = random.randint(0, self.__results_len - 1)
        self.__traversed = []  # will store the trail lines

    @property
    def window(self):
        return self.__window

    @property
    def height(self):
        return self.__height

    @property
    def label_font(self):
        return self.__label_font

    def start(self):
        self.__prepare()

        current_vertical = self.__verticals[self.__vertical_index]
        current_vertical.set_start()
        y = 0

        pos_x = current_vertical.start_pos[0]
        pos_y = MARGIN_TOP + y
        prev_pos = (pos_x, pos_y)

        clock = pygame.time.Clock()
        running = True

        while running or y < self.__height:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.__window.fill(WHITE)

            # draw verticals and horizontals
            drawn = set()
            for v in self.__verticals:
                v.draw()
                for h in v.horizontals.values():
                    if h not in drawn:
                        h.draw()
                        drawn.add(h)

            if y < self.__height:
                pos_x = current_vertical.start_pos[0]
                pos_y = MARGIN_TOP + y
            else:
                current_vertical.set_end()

            # check horizontal at this step
            current_horizontal = current_vertical.get_horizontal(y)
            if current_horizontal:
                next_vertical = current_horizontal.get_next_vertical(current_vertical)
                # add horizontal segment to trail
                self.__traversed.append(((pos_x, pos_y), (next_vertical.start_pos[0], pos_y)))
                current_vertical = next_vertical
                pos_x = current_vertical.start_pos[0]  # update x after jump

            # add vertical segment to trail
            self.__traversed.append((prev_pos, (pos_x, pos_y)))
            prev_pos = (pos_x, pos_y)

            # draw the trail
            for line in self.__traversed:
                pygame.draw.line(self.__window, RED, line[0], line[1], 3)

            # draw current circle
            pygame.draw.circle(self.__window, RED, (pos_x, pos_y), 5)

            self.__cover(pos_y)

            y += 1
            pygame.display.flip()
            clock.tick(FPS)

    def __prepare(self):
        y = LINE_WIDTH
        while y < (self.__height - LINE_WIDTH):
            i = 0
            while i < self.__results_len - 1:
                if random.random() < 0.3:
                    left = self.__verticals[i]
                    right = self.__verticals[i + 1]

                    if left.get_horizontal(y) is None and right.get_horizontal(y) is None:
                        horizontal = Horizontal(self, left, right, MARGIN_TOP + y)
                        left.set_horizontal(y, horizontal)
                        right.set_horizontal(y, horizontal)
                        i += 2
                        y += (LINE_WIDTH * 2)
                        continue
                i += 1
            y += 1

    def __cover(self, current_y):
        rect_top = (MARGIN_TOP / 6) + current_y
        rect_height = self.__height + MARGIN_TOP - rect_top
        pygame.draw.rect(self.__window, BLACK, (0, rect_top, self.__window_width, rect_height))

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('ERROR: Not enough arguments!')
        print('Usage: python amidakuji.py <result1> <result2> [<result3> ...] <height_px>')
        sys.exit(1)

    pygame.init()
    game = Game()
    game.start()
    sys.exit(0)
