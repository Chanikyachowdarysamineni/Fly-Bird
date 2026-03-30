import pygame
from typing import Optional, Callable


class Button:
    """UI Button"""
    
    def __init__(self, x: float, y: float, width: float, height: float,
                 text: str, callback: Optional[Callable] = None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.hovered = False
        self.color = (100, 100, 100)
        self.hover_color = (150, 150, 150)
    
    def update(self, mouse_pos):
        """Update button hover state"""
        self.hovered = self.rect.collidepoint(mouse_pos)
    
    def click(self):
        """Handle button click"""
        if self.callback:
            self.callback()
    
    def draw(self, screen: pygame.Surface, font: pygame.font.Font):
        """Draw button"""
        color = self.hover_color if self.hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
        
        text_surf = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
    
    def is_clicked(self, mouse_pos, clicked: bool) -> bool:
        """Check if button was clicked"""
        return clicked and self.rect.collidepoint(mouse_pos)


class MenuItem:
    """Menu item option"""
    
    def __init__(self, x: float, y: float, text: str, callback: Optional[Callable] = None):
        self.x = x
        self.y = y
        self.text = text
        self.callback = callback
        self.hovered = False
        self.width = 200
        self.height = 50
    
    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x - self.width // 2, self.y - self.height // 2,
                          self.width, self.height)
    
    def update(self, mouse_pos):
        """Update hover state"""
        self.hovered = self.get_rect().collidepoint(mouse_pos)
    
    def click(self):
        """Handle click"""
        if self.callback:
            self.callback()
    
    def draw(self, screen: pygame.Surface, font: pygame.font.Font):
        """Draw menu item"""
        rect = self.get_rect()
        color = (255, 150, 0) if self.hovered else (100, 150, 200)
        
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, (255, 255, 255), rect, 2)
        
        text_surf = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)


class HUD:
    """Heads-up display for game information"""
    
    def __init__(self, window_width: int, window_height: int):
        self.width = window_width
        self.height = window_height
        self.small_font = pygame.font.Font(None, 24)
        self.medium_font = pygame.font.Font(None, 32)
        self.large_font = pygame.font.Font(None, 48)
    
    def draw_score(self, screen: pygame.Surface, score: int, x: int = 10, y: int = 10):
        """Draw current score"""
        text = self.medium_font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(text, (x, y))
    
    def draw_hiscore(self, screen: pygame.Surface, hiscore: int, x: int = None,
                     y: int = 10):
        """Draw high score"""
        if x is None:
            text = self.small_font.render(f"Best: {hiscore}", True, (200, 200, 0))
            x = self.width - text.get_width() - 10
        else:
            text = self.small_font.render(f"Best: {hiscore}", True, (200, 200, 0))
        
        screen.blit(text, (x, y))
    
    def draw_difficulty(self, screen: pygame.Surface, difficulty_name: str,
                       color: tuple, x: int = 10, y: int = 50):
        """Draw difficulty indicator"""
        text = self.small_font.render(f"Difficulty: {difficulty_name}", True, color)
        screen.blit(text, (x, y))
    
    def draw_lives(self, screen: pygame.Surface, lives: int, x: int = 10, y: int = 90):
        """Draw lives/shields remaining"""
        text = self.small_font.render(f"Lives: {lives}", True, (0, 200, 255))
        screen.blit(text, (x, y))
    
    def draw_powerup_status(self, screen: pygame.Surface, active_powerups: dict,
                           x: int = 10, y: int = 130):
        """Draw active power-ups"""
        y_offset = 0
        for putype, remaining_time in active_powerups.items():
            seconds = max(1, remaining_time // 30)
            text = self.small_font.render(f"{putype.name}: {seconds}s", True, (255, 200, 0))
            screen.blit(text, (x, y + y_offset))
            y_offset += 25
    
    def draw_center_text(self, screen: pygame.Surface, text: str,
                        font_size: str = "large", color: tuple = (255, 255, 255),
                        y_offset: int = 0):
        """Draw text centered on screen"""
        fonts = {
            "small": self.small_font,
            "medium": self.medium_font,
            "large": self.large_font,
        }
        font = fonts.get(font_size, self.medium_font)
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect(center=(self.width // 2, self.height // 2 + y_offset))
        screen.blit(text_surf, text_rect)
    
    def draw_stats(self, screen: pygame.Surface, stats: dict, x: int = 20, y: int = 60):
        """Draw game statistics"""
        y_offset = 0
        for key, value in stats.items():
            text = self.small_font.render(f"{key}: {value}", True, (200, 200, 200))
            screen.blit(text, (x, y + y_offset))
            y_offset += 30


class Notification:
    """Temporary notification message"""
    
    def __init__(self, text: str, duration: int = 120, color: tuple = (255, 255, 255)):
        self.text = text
        self.duration = duration
        self.max_duration = duration
        self.color = color
        self.font = pygame.font.Font(None, 36)
    
    def update(self):
        """Update notification lifetime"""
        self.duration -= 1
    
    def draw(self, screen: pygame.Surface, x: int, y: int):
        """Draw notification with fade effect"""
        alpha = int(255 * (self.duration / self.max_duration))
        color = tuple(int(c * (self.duration / self.max_duration)) for c in self.color)
        
        text_surf = self.font.render(self.text, True, color)
        screen.blit(text_surf, (x, y))
    
    def is_active(self) -> bool:
        """Check if notification is still visible"""
        return self.duration > 0
