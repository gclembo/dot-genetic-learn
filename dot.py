import numpy as np


class Dot:
    """
    This class represents a dot.
    """

    def __init__(self, x: float, y: float, target_x: float, target_y: float) -> None:
        """
        Initializes a Dot object with given x and y coordinates and given target x and y
        coordinates for the Dot to get to.
        :param x: initial x coordinate
        :param y: initial y coordinate
        :param target_x: target x coordinate
        :param target_y: target y coordinate
        """
        self._x = x
        self._y = y
        self._dx = 0
        self._dy = 0
        self._target_x = target_x
        self._target_y = target_y
        self._is_alive = True
        self._brain = self._Brain()

    def get_x(self) -> float:
        """
        :return: x coordinate of this Dot
        """
        return self._x

    def get_y(self) -> float:
        """
        :return: y coordinate of this Dot
        """
        return self._y

    def is_alive(self) -> bool:
        """
        :return: If this dot is alive
        """
        return self._is_alive

    def reset(self, x: float, y: float) -> None:
        """
        Resets Dot and moves it to a given x and y coordinate.
        :param x: new x coordinate
        :param y: new y coordinate
        """
        self._x = x
        self._y = y
        self._dx = 0
        self._dy = 0
        self._is_alive = True

    def die(self) -> None:
        """
        Makes Dot no longer alive.
        """
        self._is_alive = False

    def take_step(self) -> None:
        """
        If this Dot is alive, it takes a step in the direction it is moving.
        """
        if (self._is_alive):
            self._x += self._dx
            self._y += self._dy

    def get_fitness(self) -> float:
        """
        Calculates and returns Dot fitness.
        :return: fitness of the dot
        """
        target_dist = self.dist_to_target()
        if self._is_alive:
            return target_dist
        else:
            return target_dist * 2

    def chose_velocity(self) -> None:
        """
        Decides what the Dot's current velocity should be
        """
        [self._dx, self._dy] = self._brain.make_choice([self._x, self._y, self._dx, self._dy,
                                                        self._target_x, self._target_y])

    def dist_to_target(self) -> float:
        """
        Calculates and returns the distance from this Dot to its target coordinates.
        :return: Distance from this Dot to its target coordinates
        """
        return np.linalg.norm([self._x - self._target_x, self._y - self._target_y])

    def update_learning_rate(self) -> None:
        """
        Updates learning rate based on how successful the Dot is
        """
        self._brain.learning_rate = self.get_fitness() / 1000  # arbitrary

    def make_brain_copy(self, other: 'Dot') -> None:
        """
        Given another dot, makes a copy of its brain and replaces this brain with other brain.
        :param other: Other Dot to copy brain from
        """
        self._brain.weights = np.copy(other._brain.weights)
        self._brain.learning_rate = other._brain.learning_rate

    def __lt__(self, other: 'Dot') -> bool:
        """
        Given another Dot to compare to returns if this Dot is less than the other
        based on whether this Dot has lower fitness.
        :param other: Other Dot to compare to.
        :return: If this Dot is less than the other Dot.
        """
        return self.get_fitness() < other.get_fitness()

    # This class is a brain for a point which controls how points make decisions
    class _Brain:
        # Initializes a new brain and sets brain weights
        def __init__(self):
            self.weights = (np.random.rand(2, 6) - 0.5)
            self.learning_rate = 0.1

        # given an input vector, evaluates it and returns output vector
        def make_choice(self, condition):
            return np.dot(self.weights, condition)

        def mutate(self):
            self.weights += (np.random.rand(2, 6) - 0.5) * self.learning_rate
