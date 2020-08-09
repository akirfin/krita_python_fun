import math
from random import random
from contextlib import contextmanager

from PyQt5.QtGui import QPainter, QVector2D, QColor

from .particle import Particle
from .spawner import Spawner


class Cloud(object):
    """
    Cloud of Particles, a particle cloud?
    Particle count should remain fixed. (some are just corpses...)
    """

    decay = 0.997  # some energy is lost
    gravity = QVector2D(0.0, 0.05)

    def __init__(self, max_particles=1000):
        self.spawners = [Spawner()]
        # self.forces = [Force()]  This is an exercise left to the reader
        self.particles = [Particle() for _ in range(max_particles)]
        self.alive_count = 0


    def simulate(self, delta_time):
        self.time_to_be_born(delta_time)
        self.time_to_live(delta_time)
        self.time_to_die(delta_time)


    def time_to_be_born(self, delta_time):
        for spawner in self.spawners:
            spawn_count = spawner.spawn(self.particles[self.alive_count:], delta_time)
            self.alive_count += spawn_count


    def time_to_live(self, delta_time):
        # for force in self.forces:
        for p in self.particles[:self.alive_count]:
            p.velocity += self.gravity * delta_time
            p.velocity *= self.decay ** delta_time
            p.position += p.velocity
            p.color.setAlphaF(0.2 * (p.lifespan / 500.0))  # nice alpha decay...
            p.lifespan -= delta_time


    def time_to_die(self, delta_time):
        """
        List size is kept same, dead particles
        are just swapped to backend of list.
        """
        cursor = 0
        pc = self.particles
        while cursor < self.alive_count:
            lc = self.alive_count
            p = pc[cursor]
            if p.lifespan <= 0.0:
                # a corpse, move to corpse pile, using swap
                pc[lc], pc[cursor] = pc[cursor], pc[lc]
                self.alive_count -= 1
                # keep cursor index!
            else:
                cursor += 1
