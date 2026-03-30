import random
import pygame


class Particle:
    """Individual particle for visual effects"""
    
    def __init__(self, x: float, y: float, vel_x: float, vel_y: float,
                 color: tuple, lifetime: int, size: int = 5):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = size
        self.gravity = 0.3
    
    def update(self):
        """Update particle position and lifetime"""
        self.x += self.vel_x
        self.y += self.vel_y
        self.vel_y += self.gravity
        self.lifetime -= 1
    
    def draw(self, screen: pygame.Surface):
        """Draw particle with fade effect"""
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        color = tuple(
            int(c * (self.lifetime / self.max_lifetime))
            for c in self.color
        )
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.size)
    
    def is_alive(self) -> bool:
        """Check if particle is still active"""
        return self.lifetime > 0


class ParticleSystem:
    """Manages particle effects"""
    
    def __init__(self):
        self.particles = []
    
    def emit_explosion(self, x: float, y: float, color: tuple = (255, 100, 0),
                      count: int = 15):
        """Create explosion effect"""
        for _ in range(count):
            angle = random.uniform(0, 2 * 3.14159)
            speed = random.uniform(1, 5)
            vel_x = speed * random.uniform(-1, 1)
            vel_y = speed * random.uniform(-2, 0)
            
            particle = Particle(
                x, y, vel_x, vel_y, color,
                lifetime=random.randint(20, 40),
                size=random.randint(2, 5)
            )
            self.particles.append(particle)
    
    def emit_score_popup(self, x: float, y: float, count: int = 8):
        """Create score gain effect"""
        for _ in range(count):
            vel_x = random.uniform(-2, 2)
            vel_y = random.uniform(-3, -1)
            
            particle = Particle(
                x, y, vel_x, vel_y, (255, 200, 0),
                lifetime=30, size=3
            )
            self.particles.append(particle)
    
    def emit_shield_hit(self, x: float, y: float):
        """Create shield activation effect"""
        for _ in range(20):
            angle = random.uniform(0, 2 * 3.14159)
            speed = random.uniform(2, 4)
            vel_x = speed * random.cos(angle)
            vel_y = speed * random.sin(angle)
            
            particle = Particle(
                x, y, vel_x, vel_y, (0, 150, 255),
                lifetime=25, size=3
            )
            self.particles.append(particle)
    
    def update(self):
        """Update all particles"""
        for particle in self.particles[:]:
            particle.update()
            if not particle.is_alive():
                self.particles.remove(particle)
    
    def draw(self, screen: pygame.Surface):
        """Draw all particles"""
        for particle in self.particles:
            particle.draw(screen)
    
    def clear(self):
        """Clear all particles"""
        self.particles.clear()


class ScreenShake:
    """Screen shake effect"""
    
    def __init__(self, intensity: int = 5, duration: int = 10):
        self.intensity = intensity
        self.duration = duration
        self.timer = 0
    
    def activate(self, intensity: int = 5, duration: int = 10):
        """Activate screen shake"""
        self.intensity = intensity
        self.duration = duration
        self.timer = duration
    
    def update(self):
        """Update shake timer"""
        if self.timer > 0:
            self.timer -= 1
    
    def get_offset(self) -> tuple:
        """Get current screen offset (dx, dy)"""
        if self.timer <= 0:
            return (0, 0)
        
        progress = self.timer / self.duration
        if progress > 0.5:
            return (random.randint(-self.intensity, self.intensity), 0)
        else:
            return (0, random.randint(-self.intensity // 2, self.intensity // 2))
    
    def is_active(self) -> bool:
        """Check if shake is active"""
        return self.timer > 0
