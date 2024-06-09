import time
import pygame
import dot

# this class handles running the dot generations
class GameMaster:
    def __init__(self, dot_start_x, dot_start_y, num_dots, target_x, target_y):
        self.dots = [None] * num_dots
        self.num_dots = num_dots
        self.dot_start_x = dot_start_x
        self.dot_start_y = dot_start_y
        self.target_x = target_x
        self.target_y = target_y

        for i in range(num_dots):
            self.dots[i] = dot.Dot(dot_start_x, dot_start_y, target_x, target_y)

    def update_dots(self, window):
        window.fill((255, 255, 255))
        pygame.draw.circle(window, (255, 0, 0),
                           (self.target_x, self.target_y), 5)
        pygame.draw.circle(window, (0, 255, 0),
                           (self.dot_start_x, self.dot_start_y), 5)

        for point in self.dots:
            pygame.draw.circle(window, (0, 0, 0), (point.x, point.y), 3)
            point.take_step()
            point.chose_velocity()
            if (point.x < 0 or point.y < 0
                    or point.x > window.get_width() or point.y > window.get_height()):
                point.die()
        pygame.display.update()


    def run_generation(self, window, step_num, pause_time):
        for i in range(step_num):
            self.update_dots(window)
            time.sleep(pause_time)

    def reproduce_dots(self):

        self.dots.sort()

        self.dots[0].update_learning_rate()
        self.dots[0].reset(self.dot_start_x, self.dot_start_y)
        self.dots[1].update_learning_rate()
        self.dots[1].reset(self.dot_start_x, self.dot_start_y)


        for i in range(2, len(self.dots) - 1):
            point = self.dots[i]
            point.make_brain_copy(self.dots[i % 2])
            point.reset(self.dot_start_x, self.dot_start_y)
            point.brain.mutate()
            self.dots[i] = point


