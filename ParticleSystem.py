# Might replace with a layer to keep consistency
class ParticleSystem():
    """Container for all particles."""
    def __init__(self):
        self.particles = []
        self.emitters = []

    def update(self, delta_time):
        """Calls update on all the emitters currently active."""
        for i, particle in sorted(enumerate(self.particles), reverse=True):
            particle.update(delta_time)
            
            if not particle.alive:
                self.particles.pop(i)
        
        for i, emitter in sorted(enumerate(self.emitters), reverse=True):
            emitter.update(self, delta_time)

            if emitter.duration < 0:
                self.emitters.pop(i)
            

    def draw(self, surface, camera):
        """Draws all particles to the screen"""
        for i, particle in enumerate(self.particles):
            particle.draw(surface, camera)
            
            if not particle.alive:
                self.particles.pop(i)
