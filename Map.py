from Vector2D import Vector2D
import pygame
from math import inf

class Map:

    def __init__(self, filename, cell_width, cell_height, screen_width, screen_height):
        self.filename = filename
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.rects = []
        self.score = [[] for i in range(screen_height + 1)]
        self.diry = [[] for i in range(screen_height + 1)]
        self.dirx = [[] for i in range(screen_height + 1)]
        self.screen_width = screen_width
        self.screen_height = screen_height

        for i in range(screen_height + 1):
            for j in range(screen_width + 1):
                self.score[i].append(-inf)
                self.diry[i].append(0)
                self.dirx[i].append(0)

    def read(self):
        self.rects.clear()
        cur_height = 0
        cur_width = 0

        with open(self.filename, 'r+') as file:
            for line in file:
                line = line.split(",")
                print(line)
                for cell in line:
                    if 'x' in cell:
                        self.rects.append((cur_width, cur_height))
                    else:
                        score_code = cell[1::]
                        last_index = len(score_code) - 1
                        dir = score_code[last_index]

                        base_score = int(score_code[0:last_index])
                        
                        for i in range(self.cell_width):
                            for j in range(self.cell_height):
                                #print(cur_height + j, cur_width + i)
                                self.score[cur_height + j][cur_width + i] = base_score
                                
                                if dir == 'D':
                                    self.score[cur_height + j][cur_width + i] += j / self.cell_height
                                    self.diry[cur_height + j][cur_width + i] = 1
                                elif dir == 'U':
                                    self.score[cur_height + j][cur_width + i] += (1 - j / self.cell_height)
                                    self.diry[cur_height + j][cur_width + i] = -1
                                elif dir == 'L':
                                    self.score[cur_height + j][cur_width + i] += (1 - i / self.cell_width)
                                    self.dirx[cur_height + j][cur_width + i] = -1
                                elif dir == 'R':
                                    self.score[cur_height + j][cur_width + i] += i / self.cell_width
                                    self.dirx[cur_height + j][cur_width + i] = 1




                    cur_width += self.cell_width


                cur_width = 0
                cur_height += self.cell_height
        
        print(self.rects)

    def draw(self, WINDOW):
        for rect in self.rects:
            pygame.draw.rect(WINDOW, [0, 0, 0], [rect[0], rect[1], self.cell_width, self.cell_height])

    # Very slow...
    def cast_collision_ray(self, start: Vector2D, dir: Vector2D, WINDOW=None, color=[255,0,0]):
        dir = dir.normalized()

        check_pos = Vector2D(start.x, start.y)

        last_check = Vector2D(-1, -1)
        while check_pos.x < self.screen_width and check_pos.y < self.screen_height and check_pos.x > 0 and check_pos.y > 0:
            # Do check
            #print(check_pos.x, check_pos.y, len(self.score[0]), len(self.score))
            if int(check_pos.x) < 0 or int(check_pos.x) >= len(self.score[0]) - 1 or int(check_pos.y) < 0 or int(check_pos.y) >= len(self.score) - 1:
                collision =  Vector2D(check_pos.x, check_pos.y)
                return collision.dist(start)
            elif self.score[int(check_pos.y)][int(check_pos.x)] == -inf:
                collision =  Vector2D(check_pos.x, check_pos.y)
                if WINDOW != None:
                    pygame.draw.line(WINDOW, color, (start.x, start.y), (check_pos.x, check_pos.y))

                return collision.dist(start)

            last_check = Vector2D(check_pos.x, check_pos.y)

            # Increment
            while int(check_pos.x) == int(last_check.x) and int(check_pos.y) == int(last_check.y):
                check_pos.x += dir.x
                check_pos.y += dir.y

        if WINDOW != None:
            pygame.draw.line(WINDOW, color, (start.x, start.y), (check_pos.x, check_pos.y))
        
        return start.dist(check_pos)