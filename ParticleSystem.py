class ParticleSystem():
    def __init__(self):
        self.emitters = []

    def update(self, delta_time):
        for i, emitter in sorted(enumerate(self.emitters), reverse=True):
            emitter.update(delta_time)

            if emitter.duration < 0:
                self.emitters.pop(i)

    def draw(self, surface, camera):
        for emitter in self.emitters:
            emitter.draw(surface, camera)
