# Might replace with a layer to keep consistency
class ParticleSystem():
    """Container for all particles."""
    def __init__(self):
        self.emitters = []

    def update(self, delta_time):
        """Calls update on all the emitters currently active."""
        for i, emitter in sorted(enumerate(self.emitters), reverse=True):
            emitter.update(delta_time)

            if emitter.duration < 0:
                self.emitters.pop(i)

    def draw(self, surface, camera):
        """Draws all particles to the screen"""
        for emitter in self.emitters:
            emitter.draw(surface, camera)
