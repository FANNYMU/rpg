
from core.particle import WaterParticle

class ParticleManager:
    def __init__(self):
        self.particles = []

    def create_splash(self, x, y, count=30):
        for _ in range(count):
            self.particles.append(WaterParticle(x, y))

    def update(self):
        particles_to_remove = []
        for i, particle in enumerate(self.particles):
            particle.update()
            if not particle.is_alive():
                particles_to_remove.append(i)

        for index in sorted(particles_to_remove, reverse=True):
            self.particles.pop(index)

    def draw(self):
        for particle in self.particles:
            particle.draw()
