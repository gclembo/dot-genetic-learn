from typing import Any

import numpy as np
from numpy import floating


class Dot:
    """
    This class represents a dot with a location, velocity, and target location to get to.
    """

    def __init__(self, x: float, y: float, target_x: float, target_y: float) -> None:
        """
        Initializes a Dot object with given x and y coordinates and given target x and y
        coordinates for the Dot to get to.
        :param x: initial x coordinate.
        :param y: initial y coordinate.
        :param target_x: target x coordinate.
        :param target_y: target y coordinate.
        """
        self._x = x  # x coordinate
        self._y = y  # y coordinate
        self._dx = 0  # x velocity
        self._dy = 0  # y velocity
        self._target_x = target_x  # target x
        self._target_y = target_y  # target y
        self._is_alive = True  # if Dot is alive
        self._mutation_randomness = 0.1  # amount of randomness in mutation
        self._brain = (np.random.rand(2, 2) - 0.5) * self._mutation_randomness  # Dot brain weights

    @property
    def x(self) -> float:
        """
        :return: x coordinate of this Dot.
        """
        return self._x

    @property
    def y(self) -> float:
        """
        :return: y coordinate of this Dot.
        """
        return self._y

    @property
    def is_alive(self) -> bool:
        """
        :return: If this Dot is alive.
        """
        return self._is_alive

    def get_brain(self) -> np.array:
        """
        :return: Returns the matrix representing the dot brain.
        """
        return self._brain

    def set_brain(self, brain: np.array) -> None:
        """
        Given a 2 by 2 numpy array representing a dot brain, sets
        the matrix to the dot brain.
        :param brain: Numpy array representing dot brain.
        """
        self._brain = brain

    def update_end(self, target_x: float, target_y: float):
        """
        Given a new x and y coordinate for the target, target
        location for the dot.
        :param target_x: new x coordinate for dot target.
        :param target_y: new y coordinate for dot target.
        """
        self._target_x = target_x
        self._target_y = target_y

    def reset(self, x: float, y: float) -> None:
        """
        Resets Dot and moves it to a given x and y coordinate.
        :param x: new x coordinate.
        :param y: new y coordinate.
        """
        self._x = x
        self._y = y
        self._dx = 0
        self._dy = 0
        self._is_alive = True

    def die(self) -> None:
        """
        Sets Dot to no longer alive.
        """
        self._is_alive = False

    def take_step(self, step_size: float) -> None:
        """
        Given a step size, if this Dot is alive, takes step in direction
        of velocity scaled by the step size.
        :param step_size: the size of the step.
        """
        if self.is_alive:
            self._x += self._dx * step_size
            self._y += self._dy * step_size

    def _get_fitness(self) -> floating[Any] | int:
        """
        Calculates and returns Dot fitness.
        :return: fitness of the dot.
        """
        target_dist = self._dist_to_target()
        if self.is_alive:
            return target_dist
        else:
            return target_dist * 2


    def chose_velocity(self) -> None:
        """
        Calculates what the Dot's current velocity should be based on brain weights.
        """
        dx, dy = np.dot(self._brain, [self._target_x - self._x, self._target_y - self._y])

        length = np.linalg.norm([dx, dy])
        speed = 15
        if length > 0.1:
            self._dx, self._dy = speed * dx / length, speed * dy / length
        # elif length > 0.05:
        #     self._dx, self._dy = dx, dy
        else:
            self._dx, self._dy = 0, 0


    def _dist_to_target(self) -> floating[Any]:
        """
        Calculates and returns the distance from this Dot to its target coordinates.
        :return: Distance from this Dot to its target coordinates.
        """
        return np.linalg.norm([self._x - self._target_x, self._y - self._target_y])

    def update_mutation_randomness(self) -> None:
        """
        Updates mutation randomness based on how fit the Dot is.
        """
        self._mutation_randomness = self._get_fitness() / 1000  # arbitrary

    def make_brain_copy(self, other: 'Dot') -> None:
        """
        Given another Dot, makes a copy of its brain and replaces this brain with other brain.
        :param other: Other Dot to copy brain from
        """
        self._brain = np.copy(other._brain)
        self._mutation_randomness = other._mutation_randomness

    def __lt__(self, other: 'Dot') -> bool:
        """
        Given another Dot to compare to returns if this Dot is less than the other Dot
        based on whether this Dot has lower fitness. Returns true if this is less than
        other, otherwise, false is returned.
        :param other: Other Dot to compare to.
        :return: If this Dot is less than the other Dot.
        """
        return self._get_fitness() < other._get_fitness()

    def mutate(self) -> None:
        """
        Mutates Dot brain.
        """
        self._brain += (np.random.rand(2, 2) - 0.5) * self._mutation_randomness
