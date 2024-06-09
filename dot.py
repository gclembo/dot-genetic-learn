import numpy as np


# This class is a dot that moves and tries to get to a target
class Dot:

    def __init__(self, x, y, target_x, target_y):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.target_x = target_x
        self.target_y = target_y
        self.is_alive = True
        self.brain = self._Brain()


    def reset(self, x, y):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.is_alive = True

    def die(self):
        self.is_alive = False

    # Takes step in direction of velocity
    def take_step(self):
        if (self.is_alive):
            self.x += self.dx
            self.y += self.dy

    def get_fitness(self):
        target_dist = self.dist_to_target()
        if self.is_alive:
            return target_dist
        else:
            return target_dist * 2

    # Choses and updates best velocity of dot
    def chose_velocity(self):
        [self.dx, self.dy] = self.brain.make_choice([self.x, self.y, self.dx, self.dy, self.target_x, self.target_y])

    def dist_to_target(self):
        return np.linalg.norm([self.x - self.target_x, self.y - self.target_y])

    def update_learning_rate(self):
        self.brain.learning_rate = self.get_fitness() / 1000 # arbitrary

    # given another dot, makes a copy of its brain and replaces this brain with other brain
    def make_brain_copy(self, other):
        self.brain.weights = np.copy(other.brain.weights)
        self.brain.learning_rate = other.brain.learning_rate

    def __lt__(self, other):
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
