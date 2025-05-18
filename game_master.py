import time
import pygame
from dot import Dot
import numpy as np

class GameMaster:
    """
    This class is a Game Master which facilitates running Dot generations and reproduction.
    """

    def __init__(self, dot_start_x: float, dot_start_y: float, num_dots: int,
                 target_x: float, target_y: float) -> None:
        """
        Initializes a new GameMaster object given a starting x and y for each generation of Dots,
        the number of Dots in each generation, and the target x and y for each generation.
        :param dot_start_x: Starting x value for each generation of Dots.
        :param dot_start_y: Starting y value for each generation of Dots.
        :param num_dots: Number of Dots in each generation.
        :param target_x: Target x coordinate.
        :param target_y: Target y coordinate.
        :raises ValueError: if the number of dots is not at least 2.
        """
        if num_dots < 2:
            raise ValueError("Number of dots must be at least 2")
        self._num_dots = num_dots
        self._dot_start_x = dot_start_x
        self._dot_start_y = dot_start_y
        self._target_x = target_x
        self._target_y = target_y
        self._dots = []
        self._avg_brain = np.zeros((2, 2))
        for i in range(num_dots):
            self._dots.append(Dot(self._dot_start_x, self._dot_start_y,
                                  self._target_x, self._target_y))

    def update_dots(self, window: pygame.Surface, pause_time: float) -> None:
        """
        Given a window to display, and a time between velocity updates,
        runs a step for all Dots in Game Master.
        :param window: window for display.
        :param pause_time: time between velocity updates.
        """
        # Display updates
        frames = 10
        for i in range(frames):
            window.fill((255, 255, 255))
            pygame.draw.circle(window, (255, 0, 0),
                               (self._target_x, self._target_y), 5)
            pygame.draw.circle(window, (0, 255, 0),
                               (self._dot_start_x, self._dot_start_y), 5)
            for point in self._dots:
                pygame.draw.circle(window, (0, 0, 0), (point.x, point.y), 3)
                point.take_step(1 / frames)
                if (point.x < 0 or point.y < 0
                        or point.x > window.get_width() or point.y > window.get_height()):
                    point.die()
            pygame.draw.circle(window, (0, 0, 255), (self._dots[0].x, self._dots[0].y), 3)
            pygame.display.update()
            time.sleep(pause_time / frames)

        # updates point velocities
        for point in self._dots:
            point.chose_velocity()


    def update_end(self, target_x: float, target_y: float) -> None:
        """
        Given a new x and y coordinate for the target, updates all dots to
        be considering this new location.
        :param target_x: new x coordinate for dot target.
        :param target_y: new y coordinate for dot target.
        """
        self._target_x = target_x
        self._target_y = target_y
        for dot in self._dots:
            dot.update_end(target_x, target_y)

    def run_generation(self, window: pygame.Surface, step_num: int, pause_time: float) -> None:
        """
        Given a window for display, number of steps to take, and the time between velocity
        updates, runs the generation for the given number of steps.
        :param window: window for display.
        :param step_num: number of steps in generation.
        :param pause_time: time between velocity updates.
        """
        for i in range(step_num):
            self.update_dots(window, pause_time)

    def reproduce_dots(self):
        """
        Refreshes new generation of Dots based on the top fittest Dot.
        """
        self._dots.sort()
        self._avg_brain = (self._avg_brain + self._dots[0].get_brain()) / 2

        self._dots[0].update_mutation_randomness()
        self._dots[0].reset(self._dot_start_x, self._dot_start_y)

        self._dots[1].reset(self._dot_start_x, self._dot_start_y)
        self._dots[1].set_brain(self._avg_brain)
        for i in range(2, len(self._dots) - 1):
            dot = self._dots[i]
            dot.make_brain_copy(self._dots[0])
            dot.reset(self._dot_start_x, self._dot_start_y)
            dot.mutate()


