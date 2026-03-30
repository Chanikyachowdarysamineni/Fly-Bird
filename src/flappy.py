import asyncio
import sys
import random
import math

import pygame
from pygame.locals import K_ESCAPE, K_SPACE, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_TAB, K_p, K_s, KEYDOWN, QUIT, MOUSEBUTTONDOWN

from .entities import (
    Background,
    Floor,
    GameOver,
    Pipes,
    Player,
    PlayerMode,
    Score,
    WelcomeMessage,
)
from .utils import (
    GameConfig, Images, Sounds, Window,
    HighScoreManager, GameDifficulty, DIFFICULTY_CONFIGS,
    ParticleSystem, ScreenShake, PowerUpManager, PowerUpType,
    HUD, MenuItem, Notification, AchievementManager
)
from .utils.game_progression import (
    GameProgressionMode, PROGRESSION_CONFIGS, GameProgressionSystem
)
from .utils.tutorial import TutorialScreen, GameStats
from .utils.colors import COLORS, UI, EFFECTS, MenuTheme, GameplayTheme


class Flappy:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("🎮 Flappy Bird - Hackathon Edition 🎮")
        window = Window(288, 512)
        screen = pygame.display.set_mode((window.width, window.height))
        images = Images()

        self.config = GameConfig(
            screen=screen,
            clock=pygame.time.Clock(),
            fps=30,
            window=window,
            images=images,
            sounds=Sounds(),
        )
        
        # New hackathon features
        self.high_score_manager = HighScoreManager()
        self.particle_system = ParticleSystem()
        self.screen_shake = ScreenShake()
        self.powerup_manager = PowerUpManager()
        self.achievements = AchievementManager()
        self.hud = HUD(window.width, window.height)
        self.current_difficulty = GameDifficulty.MEDIUM
        self.current_score = 0
        self.notifications = []
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        
        # Tier 1 features
        self.sound_enabled = True  # Sound toggle
        self.current_bird_color = None  # Bird color selection (None = random)
        self.player_name = "Player"  # Player name
        
        # Game progression system - Tier 2 features
        self.current_game_mode = GameProgressionMode.ARCADE  # Default mode
        self.game_progression = None  # Will be initialized when play() starts
        
        # Tutorial and stats
        self.tutorial = TutorialScreen(window.width, window.height)
        self.game_stats = GameStats(window.width, window.height)
        self.show_tutorial_on_start = self.high_score_manager.data.total_plays == 0  # First time players

    def draw_button(self, text: str, x: int, y: int, width: int = 150, height: int = 40, 
                   background_color=(50, 50, 50), text_color=(255, 255, 255), border_color=(100, 200, 255)):
        """Draw a visible button on screen and return rect for collision detection"""
        # Draw button background
        pygame.draw.rect(self.config.screen, background_color, (x, y, width, height))
        # Draw button border
        pygame.draw.rect(self.config.screen, border_color, (x, y, width, height), 2)
        # Draw button text
        text_surface = self.font_small.render(text, True, text_color)
        text_x = x + (width - text_surface.get_width()) // 2
        text_y = y + (height - text_surface.get_height()) // 2
        self.config.screen.blit(text_surface, (text_x, text_y))
        # Return button rect for collision detection
        return pygame.Rect(x, y, width, height)
    
    def is_button_clicked(self, button_rect, event):
        """Check if a button was clicked"""
        if event.type == MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            return button_rect.collidepoint(mouse_pos)
        return False
    
    def draw_back_button(self):
        """Draw a back button in bottom left corner and return rect"""
        return self.draw_button("◄ BACK", 5, self.config.window.height - 45, 
                        width=100, height=40, 
                        background_color=(100, 50, 50),
                        border_color=(255, 100, 100))


    async def start(self):
        """Main game loop"""
        # Show tutorial for first-time players
        if self.show_tutorial_on_start:
            await self.show_tutorial()
        
        while True:
            await self.main_menu()
            await self.game_mode_select()  # New: Select game progression mode
            await self.bird_color_select()
            await self.player_name_input()
            await self.difficulty_select()
            await self.splash()
            await self.play()
            await self.game_over_screen()

    async def show_tutorial(self):
        """Display interactive tutorial for new players"""
        background = Background(self.config)
        floor = Floor(self.config)
        
        while True:
            events = pygame.event.get()
            
            for event in events:
                self.check_quit_event(event)
                if event.type == KEYDOWN:
                    if event.key == K_LEFT or event.key == pygame.K_a:
                        self.tutorial.prev_slide()
                        if self.sound_enabled:
                            self.config.sounds.wing.play()
                    elif event.key == K_RIGHT or event.key == pygame.K_d:
                        if not self.tutorial.next_slide():
                            # Tutorial finished
                            return
                        if self.sound_enabled:
                            self.config.sounds.wing.play()
                    elif event.key == K_SPACE:
                        # Skip tutorial
                        return
                elif self.is_tap_event(event):
                    # Advance slide on tap
                    if not self.tutorial.next_slide():
                        return
                    if self.sound_enabled:
                        self.config.sounds.wing.play()
            
            background.tick()
            floor.tick()
            
            self.config.screen.fill(MenuTheme.MENU_BG)
            background.draw()
            floor.draw()
            self.tutorial.draw(self.config.screen)
            
            pygame.display.update()
            await asyncio.sleep(0)
            self.config.tick()

    async def main_menu(self):
        """Main menu screen"""
        background = Background(self.config)
        floor = Floor(self.config)
        player = Player(self.config)
        player.set_mode(PlayerMode.SHM)
        
        while True:
            # Collect all events once per frame
            events = pygame.event.get()
            
            # Process events
            for event in events:
                self.check_quit_event(event)
                if event.type == KEYDOWN and event.key == pygame.K_o:
                    await self.settings_menu()
                    # Recreate background and floor with new window size
                    background = Background(self.config)
                    floor = Floor(self.config)
                if self.is_tap_event(event):
                    return
            
            background.tick()
            floor.tick()
            player.tick()
            
            # Draw main menu UI
            self.config.screen.fill(MenuTheme.MENU_BG)
            background.draw()
            floor.draw()
            player.draw()
            
            self.hud.draw_center_text(self.config.screen, "FLAPPY BIRD", "large", MenuTheme.TITLE_COLOR, -100)
            self.hud.draw_center_text(self.config.screen, "Tap to Start", "medium", MenuTheme.OPTION_COLOR, 50)
            
            # Display stats
            stats = self.high_score_manager.get_stats()
            y_offset = 150
            for key, value in stats.items():
                text = self.font_small.render(f"{key}: {value}", True, MenuTheme.STAT_VALUE_COLOR)
                x = (self.config.window.width - text.get_width()) // 2
                self.config.screen.blit(text, (x, y_offset))
                y_offset += 25
            
            # Draw START button
            start_btn = self.draw_button("▶ START", 
                           (self.config.window.width - 130) // 2, 
                           self.config.window.height - 95,
                           width=130, height=40,
                           background_color=(50, 100, 50),
                           border_color=(100, 255, 100))
            
            # Draw SETTINGS button
            settings_btn = self.draw_button("⚙ SETTINGS", 
                           (self.config.window.width - 120) // 2, 
                           self.config.window.height - 45,
                           width=120, height=40,
                           background_color=(50, 75, 100),
                           border_color=(100, 150, 255))
            
            # Check button clicks
            for event in events:
                if event.type == MOUSEBUTTONDOWN:
                    if start_btn.collidepoint(event.pos):
                        return
                    if settings_btn.collidepoint(event.pos):
                        await self.settings_menu()
            
            pygame.display.update()
            await asyncio.sleep(0)
            self.config.tick()

    async def game_mode_select(self):
        """Game mode selection menu - Choose gameplay progression style"""
        background = Background(self.config)
        floor = Floor(self.config)
        
        mode_list = [
            (GameProgressionMode.ARCADE, "🎮 ARCADE", "Endless scoring"),
            (GameProgressionMode.STORY, "📖 STORY", "Story mode (200pts)"),
            (GameProgressionMode.SURVIVAL, "💪 SURVIVAL", "1 life hardcore"),
            (GameProgressionMode.SANDBOX, "🏖️ SANDBOX", "Relaxed play"),
        ]
        
        selected = 0
        
        while True:
            events = pygame.event.get()
            
            for event in events:
                self.check_quit_event(event)
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        selected = (selected - 1) % len(mode_list)
                        self.config.sounds.wing.play()
                    elif event.key == K_DOWN:
                        selected = (selected + 1) % len(mode_list)
                        self.config.sounds.wing.play()
                    elif event.key == K_SPACE:
                        self.current_game_mode = mode_list[selected][0]
                        return
                    elif event.key == K_ESCAPE:
                        return
                elif self.is_tap_event(event):
                    self.current_game_mode = mode_list[selected][0]
                    return
            
            background.tick()
            floor.tick()
            
            self.config.screen.fill(MenuTheme.MENU_BG)
            background.draw()
            floor.draw()
            
            self.hud.draw_center_text(self.config.screen, "GAME MODE", "large", 
                                     MenuTheme.TITLE_COLOR, -100)
            
            y = self.config.window.height // 2 - 80
            for i, (mode, title, description) in enumerate(mode_list):
                if i == selected:
                    # Draw selected mode with highlight
                    title_text = self.font_large.render(title, True, COLORS.HIGHLIGHT)
                    self.config.screen.blit(title_text, 
                        ((self.config.window.width - title_text.get_width()) // 2, y))
                    
                    # Draw description in smaller text
                    desc_text = self.font_small.render(description, True, (200, 200, 200))
                    self.config.screen.blit(desc_text,
                        ((self.config.window.width - desc_text.get_width()) // 2, y + 40))
                    
                    # Draw progression config details
                    config = PROGRESSION_CONFIGS[mode]
                    lives_text = self.font_small.render(
                        f"Lives: {config.starting_lives} | Goal: {config.max_score_goal or '∞'}", 
                        True, (150, 200, 255))
                    self.config.screen.blit(lives_text,
                        ((self.config.window.width - lives_text.get_width()) // 2, y + 65))
                else:
                    title_text = self.font_medium.render(title, True, MenuTheme.STAT_LABEL_COLOR)
                    self.config.screen.blit(title_text,
                        ((self.config.window.width - title_text.get_width()) // 2, y))
                
                y += 95
            
            # Draw buttons
            confirm_btn = self.draw_button("SELECT",
                           (self.config.window.width - 120) // 2,
                           self.config.window.height - 65,
                           width=120, height=35,
                           background_color=(50, 100, 50),
                           border_color=(100, 255, 100))
            
            back_btn = self.draw_back_button()
            
            # Draw helpful tip
            tip_text = self.font_small.render("Use ▲▼ to select, SPACE to confirm, ESC to back", True, MenuTheme.STAT_LABEL_COLOR)
            x = (self.config.window.width - tip_text.get_width()) // 2
            self.config.screen.blit(tip_text, (x, 10))
            
            # Check button clicks
            for event in events:
                if event.type == MOUSEBUTTONDOWN:
                    if confirm_btn.collidepoint(event.pos):
                        self.current_game_mode = mode_list[selected][0]
                        return
                    if back_btn.collidepoint(event.pos):
                        return
            
            pygame.display.update()
            await asyncio.sleep(0)
            self.config.tick()

    async def difficulty_select(self):
        """Difficulty selection menu with smooth animations"""
        background = Background(self.config)
        floor = Floor(self.config)
        
        selected = 0
        difficulties = [GameDifficulty.EASY, GameDifficulty.MEDIUM, GameDifficulty.HARD]
        animation_timer = 0
        
        while True:
            # Collect events once per frame
            events = pygame.event.get()
            
            for event in events:
                self.check_quit_event(event)
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        selected = (selected - 1) % len(difficulties)
                        self.config.sounds.wing.play()  # Sound feedback
                        animation_timer = 0
                    elif event.key == K_DOWN:
                        selected = (selected + 1) % len(difficulties)
                        self.config.sounds.wing.play()  # Sound feedback
                        animation_timer = 0
                    elif event.key == K_SPACE:
                        self.current_difficulty = difficulties[selected]
                        return
                    elif event.key == K_ESCAPE:
                        return
                elif self.is_tap_event(event):
                    self.current_difficulty = difficulties[selected]
                    return
            
            background.tick()
            floor.tick()
            animation_timer += 1
            
            # Draw difficulty selection with smooth animations
            self.config.screen.fill(MenuTheme.MENU_BG)
            background.draw()
            floor.draw()
            
            self.hud.draw_center_text(self.config.screen, "SELECT DIFFICULTY", "large", MenuTheme.TITLE_COLOR, -80)
            
            y = self.config.window.height // 2 - 60
            for i, difficulty in enumerate(difficulties):
                config = DIFFICULTY_CONFIGS[difficulty]
                if i == selected:
                    # Animated glow for selected item
                    text = self.font_large.render(config.name, True, config.color)
                    # Draw selection indicator
                    indicator = self.font_medium.render("► ", True, COLORS.HIGHLIGHT)
                    self.config.screen.blit(indicator, (self.config.window.width // 2 - 100, y))
                else:
                    text = self.font_medium.render(config.name, True, MenuTheme.STAT_LABEL_COLOR)
                
                x = (self.config.window.width - text.get_width()) // 2
                self.config.screen.blit(text, (x, y))
                y += 70
            
            # Draw buttons
            start_btn = self.draw_button("START", 
                           (self.config.window.width - 120) // 2, 
                           self.config.window.height - 65,
                           width=120, height=35,
                           background_color=(50, 100, 50),
                           border_color=(100, 255, 100))
            
            back_btn = self.draw_back_button()
            
            # Draw helpful tip
            tip_text = self.font_small.render("Use ▲▼ to select, SPACE to confirm, ESC to back", True, MenuTheme.STAT_LABEL_COLOR)
            x = (self.config.window.width - tip_text.get_width()) // 2
            self.config.screen.blit(tip_text, (x, 10))
            
            # Check button clicks
            for event in events:
                if event.type == MOUSEBUTTONDOWN:
                    if start_btn.collidepoint(event.pos):
                        self.current_difficulty = difficulties[selected]
                        return
                    if back_btn.collidepoint(event.pos):
                        return

            pygame.display.update()
            await asyncio.sleep(0)
            self.config.tick()

    async def settings_menu(self):
        """Settings menu for independent width and height adjustment"""
        background = Background(self.config)
        floor = Floor(self.config)
        
        # Start with current dimensions
        new_width = self.config.window.width
        new_height = self.config.window.height
        
        # Size constraints for playability
        MIN_WIDTH = 200
        MAX_WIDTH = 640
        MIN_HEIGHT = 300
        MAX_HEIGHT = 800
        
        # Selection state: 0 = width, 1 = height
        selected = 0
        
        while True:
            # Collect events once per frame
            events = pygame.event.get()
            
            for event in events:
                self.check_quit_event(event)
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        if selected == 1:  # Height selected
                            new_height = min(new_height + 20, MAX_HEIGHT)
                            if self.sound_enabled:
                                self.config.sounds.wing.play()
                    elif event.key == K_DOWN:
                        if selected == 1:  # Height selected
                            new_height = max(new_height - 20, MIN_HEIGHT)
                            if self.sound_enabled:
                                self.config.sounds.wing.play()
                    elif event.key == K_LEFT:
                        if selected == 0:  # Width selected
                            new_width = max(new_width - 20, MIN_WIDTH)
                            if self.sound_enabled:
                                self.config.sounds.wing.play()
                    elif event.key == K_RIGHT:
                        if selected == 0:  # Width selected
                            new_width = min(new_width + 20, MAX_WIDTH)
                            if self.sound_enabled:
                                self.config.sounds.wing.play()
                    elif event.key == K_TAB:
                        # Switch between width and height selection
                        selected = (selected + 1) % 2
                        if self.sound_enabled:
                            self.config.sounds.wing.play()
                    elif event.key == K_SPACE:
                        # Apply changes and return
                        self.config.window.resize(new_width, new_height)
                        self.config.screen = pygame.display.set_mode((new_width, new_height))
                        return
                    elif event.key == K_ESCAPE:
                        return
            
            background.tick()
            floor.tick()
            
            self.config.screen.fill(MenuTheme.MENU_BG)
            background.draw()
            floor.draw()
            
            self.hud.draw_center_text(self.config.screen, "SETTINGS", "large", 
                                     MenuTheme.TITLE_COLOR, -100)
            
            self.hud.draw_center_text(self.config.screen, "ADJUST WINDOW SIZE", "medium", 
                                     MenuTheme.STAT_LABEL_COLOR, -40)
            
            # Draw width adjustment
            y = self.config.window.height // 2 - 40
            width_color = COLORS.HIGHLIGHT if selected == 0 else MenuTheme.STAT_LABEL_COLOR
            width_text = self.font_large.render(f"Width: {new_width}", True, width_color)
            x = (self.config.window.width - width_text.get_width()) // 2
            self.config.screen.blit(width_text, (x, y))
            
            if selected == 0:
                info_text = self.font_small.render("◄ / ► to adjust", True, COLORS.HIGHLIGHT)
                x = (self.config.window.width - info_text.get_width()) // 2
                self.config.screen.blit(info_text, (x, y + 45))
            
            # Draw height adjustment
            y += 100
            height_color = COLORS.HIGHLIGHT if selected == 1 else MenuTheme.STAT_LABEL_COLOR
            height_text = self.font_large.render(f"Height: {new_height}", True, height_color)
            x = (self.config.window.width - height_text.get_width()) // 2
            self.config.screen.blit(height_text, (x, y))
            
            if selected == 1:
                info_text = self.font_small.render("▲ / ▼ to adjust", True, COLORS.HIGHLIGHT)
                x = (self.config.window.width - info_text.get_width()) // 2
                self.config.screen.blit(info_text, (x, y + 45))
            
            # Draw dimensions preview
            y += 100
            preview_text = self.font_medium.render(f"Preview: {new_width} × {new_height}", True, 
                                                   MenuTheme.STAT_VALUE_COLOR)
            x = (self.config.window.width - preview_text.get_width()) // 2
            self.config.screen.blit(preview_text, (x, y))
            
            # Draw sound toggle option
            y += 60
            sound_status = "ON" if self.sound_enabled else "OFF"
            sound_text = self.font_small.render(f"Sound: {sound_status} (Press S to toggle)", True, 
                                               (200, 200, 200))
            x = (self.config.window.width - sound_text.get_width()) // 2
            self.config.screen.blit(sound_text, (x, y))
            
            # Draw buttons
            confirm_btn = self.draw_button("APPLY", 
                           (self.config.window.width - 120) // 2, 
                           self.config.window.height - 65,
                           width=120, height=35,
                           background_color=(50, 100, 50),
                           border_color=(100, 255, 100))
            
            back_btn = self.draw_back_button()
            
            # Draw helpful tip
            tip_text = self.font_small.render("TAB to switch, SPACE to apply, ESC to back", True, 
                                             MenuTheme.STAT_LABEL_COLOR)
            x = (self.config.window.width - tip_text.get_width()) // 2
            self.config.screen.blit(tip_text, (x, 10))
            
            # Check button clicks
            for event in events:
                if event.type == MOUSEBUTTONDOWN:
                    if confirm_btn.collidepoint(event.pos):
                        self.config.window.resize(new_width, new_height)
                        self.config.screen = pygame.display.set_mode((new_width, new_height))
                        return
                    if back_btn.collidepoint(event.pos):
                        return
            
            pygame.display.update()
            await asyncio.sleep(0)
            self.config.tick()

    async def bird_color_select(self):
        """Bird color selection menu"""
        background = Background(self.config)
        floor = Floor(self.config)
        
        BIRD_COLORS = ["Red", "Blue", "Yellow"]
        selected = 1  # Default to Blue
        
        while True:
            # Collect events once per frame
            events = pygame.event.get()
            
            for event in events:
                self.check_quit_event(event)
                if event.type == KEYDOWN:
                    if event.key == K_LEFT:
                        selected = (selected - 1) % len(BIRD_COLORS)
                        self.config.sounds.wing.play()
                    elif event.key == K_RIGHT:
                        selected = (selected + 1) % len(BIRD_COLORS)
                        self.config.sounds.wing.play()
                    elif event.key == K_SPACE:
                        self.current_bird_color = selected
                        return
                    elif event.key == K_ESCAPE:
                        return
                elif self.is_tap_event(event):
                    self.current_bird_color = selected
                    return
            
            background.tick()
            floor.tick()
            
            self.config.screen.fill(MenuTheme.MENU_BG)
            background.draw()
            floor.draw()
            
            self.hud.draw_center_text(self.config.screen, "SELECT BIRD COLOR", "large", 
                                     MenuTheme.TITLE_COLOR, -80)
            
            # Draw bird color options
            y = self.config.window.height // 2 - 40
            for i, color in enumerate(BIRD_COLORS):
                if i == selected:
                    text = self.font_large.render(f"● {color}", True, COLORS.HIGHLIGHT)
                    indicator = self.font_medium.render("► ", True, COLORS.HIGHLIGHT)
                    self.config.screen.blit(indicator, (self.config.window.width // 2 - 120, y))
                else:
                    text = self.font_medium.render(f"○ {color}", True, MenuTheme.STAT_LABEL_COLOR)
                
                x = (self.config.window.width - text.get_width()) // 2
                self.config.screen.blit(text, (x, y))
                y += 60
            
            # Draw buttons
            confirm_btn = self.draw_button("CONFIRM", 
                           (self.config.window.width - 120) // 2, 
                           self.config.window.height - 65,
                           width=120, height=35,
                           background_color=(50, 100, 50),
                           border_color=(100, 255, 100))
            
            back_btn = self.draw_back_button()
            
            tip_text = self.font_small.render("Use ◄► to select, SPACE to confirm, ESC to back", True, MenuTheme.STAT_LABEL_COLOR)
            x = (self.config.window.width - tip_text.get_width()) // 2
            self.config.screen.blit(tip_text, (x, 10))
            
            # Check button clicks
            for event in events:
                if event.type == MOUSEBUTTONDOWN:
                    if confirm_btn.collidepoint(event.pos):
                        self.current_bird_color = selected
                        return
                    if back_btn.collidepoint(event.pos):
                        return
            
            pygame.display.update()
            await asyncio.sleep(0)
            self.config.tick()

    async def player_name_input(self):
        """Player name input screen"""
        background = Background(self.config)
        floor = Floor(self.config)
        
        player_name_input = self.high_score_manager.data.player_name or "Player"
        cursor_visible = True
        cursor_timer = 0
        
        while True:
            # Collect events once per frame
            events = pygame.event.get()
            
            for event in events:
                self.check_quit_event(event)
                if event.type == KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        player_name_input = player_name_input[:-1]
                        self.config.sounds.wing.play()
                    elif event.key == pygame.K_RETURN:
                        self.player_name = player_name_input or "Player"
                        self.high_score_manager.data.player_name = self.player_name
                        self.high_score_manager.save()
                        return
                    elif event.key == K_ESCAPE:
                        return
                    elif event.unicode.isalnum() or event.unicode == " ":
                        if len(player_name_input) < 16:
                            player_name_input += event.unicode
                            self.config.sounds.wing.play()
            
            background.tick()
            floor.tick()
            cursor_timer += 1
            if cursor_timer % 30 == 0:
                cursor_visible = not cursor_visible
            
            self.config.screen.fill(MenuTheme.MENU_BG)
            background.draw()
            floor.draw()
            
            self.hud.draw_center_text(self.config.screen, "ENTER YOUR NAME", "large",
                                     MenuTheme.TITLE_COLOR, -80)
            
            # Draw name input box
            box_width = 200
            box_height = 50
            box_x = (self.config.window.width - box_width) // 2
            box_y = self.config.window.height // 2 - 40
            pygame.draw.rect(self.config.screen, MenuTheme.STAT_LABEL_COLOR, 
                           (box_x, box_y, box_width, box_height), 2)
            
            display_name = player_name_input + ("_" if cursor_visible else "")
            name_text = self.font_medium.render(display_name, True, MenuTheme.STAT_VALUE_COLOR)
            text_x = box_x + (box_width - name_text.get_width()) // 2
            text_y = box_y + (box_height - name_text.get_height()) // 2
            self.config.screen.blit(name_text, (text_x, text_y))
            
            # Draw buttons
            confirm_btn = self.draw_button("CONFIRM", 
                           (self.config.window.width - 120) // 2, 
                           self.config.window.height - 65,
                           width=120, height=35,
                           background_color=(50, 100, 50),
                           border_color=(100, 255, 100))
            
            back_btn = self.draw_back_button()
            
            tip_text = self.font_small.render("Type name, ENTER to confirm, ESC to back", True, MenuTheme.STAT_LABEL_COLOR)
            x = (self.config.window.width - tip_text.get_width()) // 2
            self.config.screen.blit(tip_text, (x, 10))
            
            # Check button clicks
            for event in events:
                if event.type == MOUSEBUTTONDOWN:
                    if confirm_btn.collidepoint(event.pos):
                        self.player_name = player_name_input or "Player"
                        self.high_score_manager.data.player_name = self.player_name
                        self.high_score_manager.save()
                        return
                    if back_btn.collidepoint(event.pos):
                        return
            
            pygame.display.update()
            await asyncio.sleep(0)
            self.config.tick()

    async def splash(self):
        """Shows welcome splash screen animation of flappy bird"""
        # Apply bird color selection if chosen
        if self.current_bird_color is not None:
            self.config.images.set_player_color(self.current_bird_color)
        
        self.background = Background(self.config)
        self.floor = Floor(self.config)
        self.player = Player(self.config)
        self.welcome_message = WelcomeMessage(self.config)
        
        self.player.set_mode(PlayerMode.SHM)

        while True:
            for event in pygame.event.get():
                self.check_quit_event(event)
                if self.is_tap_event(event):
                    return

            self.background.tick()
            self.floor.tick()
            self.player.tick()
            self.welcome_message.tick()
            
            # Apply screen shake effects
            offset_x, offset_y = self.screen_shake.get_offset()
            
            # Draw with offset
            self.config.screen.fill(GameplayTheme.HUD_BG)
            self.background.draw()
            self.floor.draw()
            self.player.draw()
            self.welcome_message.draw()
            
            # Show difficulty
            difficulty_config = DIFFICULTY_CONFIGS[self.current_difficulty]
            text = self.font_small.render(f"Difficulty: {difficulty_config.name}", 
                                         True, difficulty_config.color)
            self.config.screen.blit(text, (10, 10))

            pygame.display.update()
            await asyncio.sleep(0)
            self.config.tick()

    def check_quit_event(self, event):
        if event.type == QUIT or (
            event.type == KEYDOWN and event.key == K_ESCAPE
        ):
            pygame.quit()
            sys.exit()

    def is_tap_event(self, event):
        m_left, _, _ = pygame.mouse.get_pressed()
        space_pressed = event.type == KEYDOWN and event.key == K_SPACE
        screen_tap = event.type == pygame.FINGERDOWN
        return m_left or space_pressed or screen_tap

    async def play(self):
        """Main game loop with smooth, realistic gameplay"""
        self.game_over_message = GameOver(self.config)
        self.pipes = Pipes(self.config)
        self.score = Score(self.config)
        
        # Configure difficulty
        diff_config = DIFFICULTY_CONFIGS[self.current_difficulty]
        self.pipes.pipe_gap = diff_config.pipe_gap
        for pipe in self.pipes.upper + self.pipes.lower:
            pipe.vel_x = -diff_config.pipe_speed
        
        self.score.reset()
        self.player.set_mode(PlayerMode.NORMAL)
        self.player.vel_y = diff_config.player_vel_y
        self.powerup_manager.clear()
        self.particle_system.clear()
        self.notifications.clear()
        
        # Update player physics based on difficulty
        Player.GRAVITY = diff_config.gravity
        
        lives = 3  # 3 lives for the game
        frame_count = 0
        paused = False
        powerups_collected = 0
        collision_invulnerable_frames = 0  # Invincibility timer after collision
        INVULNERABILITY_DURATION = 120  # 4 seconds at 30 FPS
        
        # Progressive difficulty tuning
        base_pipe_speed = diff_config.pipe_speed
        current_pipe_speed = base_pipe_speed
        score_last_checkpoint = 0
        current_level = 1  # Track current difficulty level within game
        
        # Achievement tracking
        first_point_achieved = False
        score_10_achieved = False
        score_50_achieved = False
        score_100_achieved = False
        difficulty_milestone_25 = False
        difficulty_milestone_main = False
        
        while lives > 0:
            frame_count += 1
            
            # Decrement invulnerability timer
            if collision_invulnerable_frames > 0:
                collision_invulnerable_frames -= 1
            
            # Progressive difficulty: Increase speed every 10 points (smoothly)
            if self.current_score > score_last_checkpoint:
                if (self.current_score // 10) > (score_last_checkpoint // 10):
                    score_checkpoint_delta = self.current_score // 10 - score_last_checkpoint // 10
                    current_pipe_speed = base_pipe_speed * (1 + score_checkpoint_delta * 0.15)  # 15% increase per checkpoint
                    current_level = 1 + (self.current_score // 10)
                    # Notify player of difficulty increase
                    if score_checkpoint_delta > 0:
                        self.add_notification(f"⚡ Level {current_level}!", color=COLORS.HIGHLIGHT)
                    score_last_checkpoint = (self.current_score // 10) * 10
            
            # Check collision with pipes ONLY if not invulnerable
            if collision_invulnerable_frames == 0 and self.player.collided(self.pipes, self.floor):
                if self.powerup_manager.is_active(PowerUpType.SHIELD):
                    # Shield blocks collision
                    self.particle_system.emit_shield_hit(self.player.x, self.player.y)
                    self.powerup_manager.deactivate_powerup(PowerUpType.SHIELD)
                    if self.sound_enabled:
                        self.config.sounds.hit.play()  # Shield impact sound
                    self.screen_shake.activate(intensity=3, duration=8)
                    self.add_notification("🛡️ Shield Blocked!", color=COLORS.INFO_PURPLE)
                    collision_invulnerable_frames = 60  # Temporary safety frames
                else:
                    # Take damage - lose a life
                    lives -= 1
                    if self.sound_enabled:
                        self.config.sounds.hit.play()
                    self.screen_shake.activate(intensity=5, duration=12)
                    self.particle_system.emit_explosion(self.player.x, self.player.y, color=COLORS.HIGHLIGHT, count=20)
                    
                    if lives <= 0:
                        # Game over
                        return
                    else:
                        # Player respawns - give feedback
                        self.add_notification(f"💥 Hit! {lives} Lives Left!", color=COLORS.HIGHLIGHT)
                        # Reset player position for respawn
                        self.player.x = 72
                        self.player.y = int(self.config.window.height * 0.2)
                        self.player.vel_y = 0
                        collision_invulnerable_frames = INVULNERABILITY_DURATION  # Invulnerable for 4 seconds

            
            # Score points when crossing pipes
            for i, pipe in enumerate(self.pipes.upper):
                if self.player.crossed(pipe):
                    base_points = 1
                    multiplier = self.powerup_manager.get_remaining_time(PowerUpType.SCORE_BOOST)
                    points = base_points * (2 if multiplier > 0 else 1)
                    self.score.add()
                    self.current_score = self.score.score
                    self.particle_system.emit_score_popup(self.player.x, self.player.y)
                    if self.sound_enabled:
                        self.config.sounds.point.play()
                    # Slight screen shake on score
                    self.screen_shake.activate(intensity=2, duration=4)
                    self.add_notification(f"+{points} Points!", color=COLORS.HIGHLIGHT)
                    
                    # Achievement: First point
                    if not first_point_achieved:
                        first_point_achieved = True
                        self.achievements.unlock("first_point")
                        self.add_notification("🏆 First Score!", color=COLORS.HIGHLIGHT)
                    
                    # Achievement: Score milestones
                    if self.current_score >= 10 and not score_10_achieved:
                        score_10_achieved = True
                        self.achievements.unlock("ten_points")
                        self.add_notification("🏆 Getting Started!", color=COLORS.HIGHLIGHT)
                    
                    if self.current_score >= 50 and not score_50_achieved:
                        score_50_achieved = True
                        self.achievements.unlock("fifty_points")
                        self.add_notification("🏆 Bird Master!", color=COLORS.HIGHLIGHT)
                    
                    if self.current_score >= 100 and not score_100_achieved:
                        score_100_achieved = True
                        self.achievements.unlock("hundred_points")
                        self.add_notification("🏆 Century!", color=COLORS.HIGHLIGHT)
                    
                    # Difficulty-specific achievements
                    difficulty_name = diff_config.name.upper()
                    if difficulty_name == "EASY" and self.current_score >= 20 and not difficulty_milestone_main:
                        difficulty_milestone_main = True
                        self.achievements.unlock("easy_clear")
                        self.add_notification("🏆 Easy Mode!", color=COLORS.HIGHLIGHT)
                    
                    if difficulty_name == "MEDIUM" and self.current_score >= 30 and not difficulty_milestone_main:
                        difficulty_milestone_main = True
                        self.achievements.unlock("medium_clear")
                        self.add_notification("🏆 Medium Challenge!", color=COLORS.HIGHLIGHT)
                    
                    if difficulty_name == "HARD" and self.current_score >= 50 and not difficulty_milestone_main:
                        difficulty_milestone_main = True
                        self.achievements.unlock("hard_clear")
                        self.add_notification("🏆 Hard Mode Master!", color=COLORS.HIGHLIGHT)
            
            # Check power-up collection
            player_rect = pygame.Rect(self.player.x, self.player.y, 
                                     self.player.w, self.player.h)
            collected_powerups = self.powerup_manager.check_collision(player_rect)
            for pu_type in collected_powerups:
                self.particle_system.emit_explosion(self.player.x, self.player.y, 
                                                   color=UI.get_powerup_color(pu_type), count=15)
                if self.sound_enabled:
                    self.config.sounds.point.play()  # Power-up sound
                self.add_notification(f"✨ {pu_type.name}!", color=UI.get_powerup_color(pu_type))
                powerups_collected += 1
                
                # Power-up achievements
                if pu_type == PowerUpType.SHIELD and powerups_collected >= 5:
                    self.achievements.unlock("shield_collector")
                    self.add_notification("🏆 Shield Collector!", color=COLORS.HIGHLIGHT)
                elif pu_type == PowerUpType.SLOW_MO and powerups_collected >= 5:
                    self.achievements.unlock("slow_mo_user")
                    self.add_notification("🏆 Slow Motion Expert!", color=COLORS.HIGHLIGHT)
                
                if powerups_collected >= 20:
                    self.achievements.unlock("powerup_master")
                    self.add_notification("🏆 Power-Up Master!", color=COLORS.HIGHLIGHT)
            
            # Handle input - responsive flapping
            for event in pygame.event.get():
                self.check_quit_event(event)
                if event.type == KEYDOWN:
                    if event.key == K_p:
                        # Toggle pause
                        paused = not paused
                        if self.sound_enabled:
                            self.config.sounds.wing.play()
                    elif event.key == K_s:
                        # Toggle sound
                        self.sound_enabled = not self.sound_enabled
                        self.config.sounds.wing.play()  # Always play this one
                        self.add_notification(f"🔊 Sound: {'ON' if self.sound_enabled else 'OFF'}", 
                                            color=COLORS.INFO_PURPLE)
                    elif self.is_tap_event(event) and not paused:
                        self.player.flap()
                        if self.sound_enabled:
                            self.config.sounds.wing.play()  # Flap sound
                elif self.is_tap_event(event) and not paused:
                    self.player.flap()
                    if self.sound_enabled:
                        self.config.sounds.wing.play()  # Flap sound
            
            # Update game state - smooth animations (skip if paused)
            if not paused:
                self.background.tick()
                self.floor.tick()
                self.pipes.tick()
                self.score.tick()
                self.player.tick()
                self.powerup_manager.update()
                self.particle_system.update()
                self.screen_shake.update()
                
                # Spawn random power-ups less frequently for realism
                if frame_count % 100 == 0:  # Every ~3 seconds at 30 FPS
                    for pipe in self.pipes.upper:
                        if random.random() < 0.15:  # 15% chance per check
                            self.powerup_manager.spawn_random_powerup(pipe.x, pipe.y - 50)
            
            # Apply slow-motion if active
            if self.powerup_manager.is_active(PowerUpType.SLOW_MO):
                for pipe in self.pipes.upper + self.pipes.lower:
                    pipe.vel_x = -current_pipe_speed * 0.5
            else:
                for pipe in self.pipes.upper + self.pipes.lower:
                    pipe.vel_x = -current_pipe_speed
            
            # Draw game - smooth rendering
            self.config.screen.fill(GameplayTheme.HUD_BG)
            
            # Get screen shake offset
            offset_x, offset_y = self.screen_shake.get_offset()
            
            self.background.draw()
            self.floor.draw()
            self.pipes.draw()
            self.score.draw()
            self.player.draw()
            
            # Draw particle effects
            self.particle_system.draw(self.config.screen)
            
            # Draw power-ups
            self.powerup_manager.draw(self.config.screen, self.font_small)
            
            # Draw HUD - professional layout
            difficulty_config = DIFFICULTY_CONFIGS[self.current_difficulty]
            self.hud.draw_difficulty(self.config.screen, difficulty_config.name,
                                    difficulty_config.color, 10, 50)
            
            # Draw shields remaining - visual feedback
            lives_color = GameplayTheme.LIVES_FULL if lives > 2 else (GameplayTheme.LIVES_WARNING if lives > 1 else GameplayTheme.LIVES_CRITICAL)
            text = self.font_small.render(f"❤️ Lives: {lives}", True, lives_color)
            self.config.screen.blit(text, (10, 80))
            
            # Draw invulnerability indicator if active
            if collision_invulnerable_frames > 0:
                inv_text = self.font_small.render(f"Shield: {collision_invulnerable_frames // 30}s", True, COLORS.INFO_PURPLE)
                self.config.screen.blit(inv_text, (10, 110))
            
            # Draw active power-ups status - clear visibility
            if self.powerup_manager.active_powerups:
                y_off = 140 if collision_invulnerable_frames > 0 else 110
                for putype, remaining in self.powerup_manager.active_powerups.items():
                    seconds = max(1, remaining // 30)
                    pu_color = UI.get_powerup_color(putype)
                    text = self.font_small.render(f"{putype.name}: {seconds}s", 
                                                 True, pu_color)
                    self.config.screen.blit(text, (10, y_off))
                    y_off += 25
            
            # Draw notifications - fade out smoothly
            for notif in self.notifications[:]:
                notif.update()
                if notif.is_active():
                    notif.draw(self.config.screen, self.config.window.width // 2 - 50, 150)
                else:
                    self.notifications.remove(notif)
            
            # Draw pause screen overlay
            if paused:
                pause_overlay = pygame.Surface((self.config.window.width, self.config.window.height))
                pause_overlay.set_alpha(180)
                pause_overlay.fill((0, 0, 0))
                self.config.screen.blit(pause_overlay, (0, 0))
                
                pause_text = self.font_large.render("PAUSED", True, COLORS.HIGHLIGHT)
                x = (self.config.window.width - pause_text.get_width()) // 2
                self.config.screen.blit(pause_text, (x, 100))
                
                resume_text = self.font_small.render("Press P to Resume", True, (200, 200, 200))
                x = (self.config.window.width - resume_text.get_width()) // 2
                self.config.screen.blit(resume_text, (x, 180))
            
            # Draw control hints at bottom
            controls_text = self.font_small.render("P:Pause  S:Sound", True, (150, 150, 150))
            self.config.screen.blit(controls_text, (5, self.config.window.height - 25))
            
            pygame.display.update()
            await asyncio.sleep(0)
            self.config.tick()

    async def game_over_screen(self):
        """Enhanced game over screen with statistics"""
        self.player.set_mode(PlayerMode.CRASH)
        self.pipes.stop()
        self.floor.stop()
        
        # Update high score
        is_new_record = self.high_score_manager.update_score(self.current_score)
        
        # Track number of games played achievement
        if self.high_score_manager.data.total_plays >= 10:
            self.achievements.unlock("ten_games")
        
        while True:
            for event in pygame.event.get():
                self.check_quit_event(event)
                if self.is_tap_event(event):
                    if self.player.y + self.player.h >= self.floor.y - 1:
                        return

            self.background.tick()
            self.floor.tick()
            self.pipes.tick()
            self.score.tick()
            self.player.tick()
            self.game_over_message.tick()
            self.particle_system.update()

            # Draw game state
            self.config.screen.fill(GameplayTheme.HUD_BG)
            self.background.draw()
            self.floor.draw()
            self.pipes.draw()
            self.score.draw()
            self.player.draw()
            self.game_over_message.draw()
            self.particle_system.draw(self.config.screen)
            
            # Draw game over info
            if is_new_record:
                text = self.font_large.render("NEW RECORD!", True, COLORS.HIGHLIGHT)
                x = (self.config.window.width - text.get_width()) // 2
                self.config.screen.blit(text, (x, 100))
                self.particle_system.emit_explosion(self.config.window.width // 2, 100, 
                                                  color=COLORS.PRIMARY_ACCENT, count=30)
            
            # Draw statistics
            stats = self.high_score_manager.get_stats()
            y = 150 if is_new_record else 100
            for key, value in stats.items():
                text = self.font_small.render(f"{key}: {value}", True, MenuTheme.STAT_VALUE_COLOR)
                x = (self.config.window.width - text.get_width()) // 2
                self.config.screen.blit(text, (x, y))
                y += 35
            
            # Draw achievements progress
            total_unlocked = self.achievements.get_total_unlocked()
            total_achievements = self.achievements.get_total_achievements()
            ach_text = self.font_small.render(f"🏆 {total_unlocked}/{total_achievements}", True, COLORS.PRIMARY_ACCENT)
            x = (self.config.window.width - ach_text.get_width()) // 2
            self.config.screen.blit(ach_text, (x, y))
            
            self.hud.draw_center_text(self.config.screen, "Tap to Continue", 
                                     "small", COLORS.SUCCESS_GREEN, y + 60)

            self.config.tick()
            pygame.display.update()
            await asyncio.sleep(0)

    async def game_over(self):
        """Deprecated: use game_over_screen instead"""
        await self.game_over_screen()
    
    def add_notification(self, text: str, color: tuple = (255, 255, 255)):
        """Add a temporary notification"""
        notif = Notification(text, duration=120, color=color)
        self.notifications.append(notif)
