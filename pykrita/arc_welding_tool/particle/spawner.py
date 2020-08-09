import math
from random import random
from contextlib import contextmanager

class Spawner(object):
    """
    Spawns new particles to cloud.

    New particles are NOT created, instead corpses
    of dead particles are reanimated. (trying to be GC friendly)
    """
    spawn_rate = 2.0  #  particles / msec
    spawn_position = QVector2D()
    spawn_velocity = QVector2D()
    spawn_scatter = 17.0  # strength of random
    spawn_lifespan = 500.0  # msec
    spawn_color = (255, 230, 150, 255)  # RGBA
    _spawn_accumulate = 0.0  # accumulate partial particles

    def spawn(self, corpses, delta_time):
        """
        Corpses are needed for spawning new life!
        """
        self._spawn_accumulate += self.spawn_rate * delta_time
        spawn_count = math.floor(self._spawn_accumulate)  # only full particles can spawn
        self._spawn_accumulate -= spawn_count
        for corpse, _ in zip(corpses, range(spawn_count)):
            phi = random() * math.tau
            power = random() * self.spawn_scatter
            scatter = QVector2D(power * math.cos(phi), power * math.sin(phi))
            corpse.velocity = QVector2D(self.spawn_velocity + scatter)
            corpse.position = QVector2D(self.spawn_position) + random() * corpse.velocity
            corpse.color = QColor(*self.spawn_color)
            corpse.lifespan = self.spawn_lifespan - random() * delta_time
        return spawn_count
