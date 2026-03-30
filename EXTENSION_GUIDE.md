# 🚀 Hackathon Extension Guide

**Quick guide to extend FlapPyBird during a hackathon**

---

## 🎯 Most Impactful Additions (Priority Order)

### Tier 1: Low Effort, High Impact (15-30 min each)

#### 1. ⏸️ Add Pause Feature
```python
# In flappy.py play() loop
paused = False

for event in pygame.event.get():
    if event.key == pygame.K_p:
        paused = not paused
    elif is_tap_event(event) and not paused:
        self.player.flap()

if not paused:
    # Update physics
    # Draw everything
else:
    # Draw pause screen
    text = font.render("PAUSED", True, (255, 255, 255))
    # ... draw it
```

#### 2. 🔊 Add Sound Toggle
```python
# In flappy.py __init__
self.sound_enabled = True

# Create toggle button in menu
if key == pygame.K_S:
    self.sound_enabled = not self.sound_enabled

# When playing sounds
if self.sound_enabled:
    self.config.sounds.point.play()
```

#### 3. 👤 Add Player Name
```python
# Edit high_score.py
@dataclass
class ScoreData:
    player_name: str = "Player"
    high_score: int = 0
    # ... other fields

# In game_over_screen(), prompt for name
name = get_player_name_input()
self.high_score_manager.data.player_name = name
self.high_score_manager.save()
```

#### 4. 🎨 Add Custom Bird Color Selection
```python
# In difficulty_select() or new menu
bird_colors = ["Red", "Blue", "Yellow"]
selected_color = select_from_menu(bird_colors)
self.config.images.player_color = selected_color

# In entities/player.py, load appropriate sprite
```

#### 5. 🏅 Add Simple Achievements
```python
# Create achievements.py
class Achievement:
    def __init__(self, name, condition, reward):
        self.name = name
        self.unlocked = False
    
# In play() loop
if self.score.val > 100 and not achievements["century"].unlocked:
    achievements["century"].unlocked = True
    particle_system.emit_explosion(...)  # Celebration
```

---

### Tier 2: Medium Effort, Great Impact (30-60 min each)

#### 6. 📋 Add Leaderboard
```python
# Create leaderboard.py
class Leaderboard:
    def __init__(self, filepath="leaderboard.json"):
        self.filepath = filepath
        self.entries = self.load()
    
    def add_score(self, name, score, difficulty):
        self.entries.append({
            "name": name,
            "score": score,
            "difficulty": difficulty,
            "timestamp": time.time()
        })
        self.entries.sort(key=lambda x: x["score"], reverse=True)
        self.entries = self.entries[:10]  # Top 10
        self.save()
    
    def draw(self, screen, font):
        for i, entry in enumerate(self.entries):
            text = f"{i+1}. {entry['name']}: {entry['score']}"
            # ... render
```

#### 7. 🎯 Add Daily Challenge Mode
```python
# New game mode with:
# - Fixed difficulty
# - Time limit (30 seconds)
# - Special pipe configuration
# - Leaderboard for that day

class DailyChallenge:
    def __init__(self):
        self.seed = date.today().toordinal()
        random.seed(self.seed)
    
    def get_pipe_pattern(self):
        # Use seeded random for consistency
        return random.choice(pipe_patterns)
```

#### 8. 🎟️ Add Combo System
```python
# In play() loop
combo_counter = 0
consecutive_success = 0

for pipe in pipes.upper:
    if player.crossed(pipe):
        consecutive_success += 1
        if consecutive_success % 5 == 0:
            combo_counter += 1
            particle_system.emit_explosion(...)
            add_notification(f"Combo x{combo_counter}!")
```

#### 9. 🛡️ Add Additional Power-Up Types
```python
# In powerups.py, add to enum:
class PowerUpType(Enum):
    SHIELD = 1
    SLOW_MO = 2
    SCORE_BOOST = 3
    MAGNET = 4          # NEW: Attract pipes to center
    SPEED_UP = 5        # NEW: Bird moves faster
    INVINCIBLE = 6      # NEW: 3-second invincibility

# Configure each with unique behavior
```

#### 10. 📊 Add Shot/Stats Camera
```python
# Record game events
class GameRecorder:
    def __init__(self):
        self.events = []
    
    def record_event(self, event_type, data):
        self.events.append({
            "frame": self.frame_count,
            "type": event_type,  # "score", "powerup", "collision"
            "data": data
        })
    
    def save_replay(self):
        with open(f"replay_{timestamp}.json", "w") as f:
            json.dump(self.events, f)
```

---

### Tier 3: Complex Features (60min+ each)

#### 11. 👥 Local Multiplayer
```python
# Split screen or turn-based
# Two players alternate games
# Compete for high score
class MultiplayerMode:
    def __init__(self):
        self.player1_score = 0
        self.player2_score = 0
    
    async def play_turn(self, player_num):
        # Run one game for player
        # Return score
        pass
```

#### 12. 🤖 AI Player
```python
# Simple ML-based or rule-based
class AIPlayer:
    def decide_flap(self, player_pos, next_pipe):
        # Simple rules:
        # - If player too high, don't flap
        # - If gap ahead, flap to reach it
        # - Predict where player will be
        gap_center = (pipe.upper_y + pipe.lower_y) / 2
        if player_pos < gap_center - threshold:
            return True
        return False
```

#### 13. 🎮 Level Editor
```python
# Create custom pipe patterns
class LevelEditor:
    def __init__(self):
        self.pipes = []
        self.is_editing = True
    
    async def edit(self):
        while self.is_editing:
            # Listen for mouse clicks
            # Add/remove/modify pipes
            # Preview gameplay
            # Save to file
```

#### 14. 🌐 Online Leaderboard
```python
# Connect to API (Firebase, custom backend)
class OnlineLeaderboard:
    def __init__(self, api_url):
        self.api_url = api_url
    
    def submit_score(self, name, score):
        response = requests.post(
            f"{self.api_url}/scores",
            json={"name": name, "score": score}
        )
        return response.ok
    
    def fetch_top_scores(self):
        response = requests.get(f"{self.api_url}/scores/top10")
        return response.json()
```

#### 15. 🎵 Music System
```python
# Background music + SFX
class AudioManager:
    def __init__(self):
        self.background_music = pygame.mixer.music
        self.sfx_volume = 0.7
        self.music_volume = 0.5
    
    def play_background(self, track):
        self.background_music.load(f"assets/music/{track}.ogg")
        self.background_music.play(-1)  # Loop
    
    def set_volumes(self, sfx_vol, music_vol):
        pygame.mixer.music.set_volume(music_vol)
        self.sfx_volume = sfx_vol
```

---

## 🔧 Quick Implementation Templates

### Add a New Menu Screen
```python
async def settings_menu(self):
    """Settings screen template"""
    while True:
        for event in pygame.event.get():
            self.check_quit_event(event)
            if key == pygame.K_ESCAPE:
                return
        
        # Draw menu
        self.config.screen.fill((0, 0, 0))
        self.hud.draw_center_text(self.config.screen, "SETTINGS", "large", 
                                  (255, 200, 0), -50)
        
        # Draw options
        # Handle input
        
        pygame.display.update()
        await asyncio.sleep(0)
```

### Add Game Statistics
```python
# In high_score.py, add to ScoreData
@dataclass
class ScoreData:
    # ... existing fields
    longest_play_time: int = 0
    best_difficulty: str = "MEDIUM"
    total_power_ups_collected: int = 0
    times_hit_new_record: int = 0
```

### Add Visual Polish
```python
# Particle effect templates
def create_rain_effect(self, x, y):
    for _ in range(30):
        self.particle_system.particles.append(
            Particle(x + random.randint(-50, 50), y,
                    vel_x=0, vel_y=random.uniform(2, 5),
                    color=(100, 150, 255), lifetime=60)
        )

def create_glow_effect(self, x, y):
    # Glowing circle that pulses
    pass
```

---

## 🚦 Implementation Checklist

When adding a feature:

- [ ] Create/modify necessary files
- [ ] Add to imports in `__init__.py`
- [ ] Create docstrings
- [ ] Add type hints
- [ ] Test thoroughly
- [ ] Handle edge cases
- [ ] Add notification/feedback
- [ ] Update documentation
- [ ] Commit/save progress

---

## 🎯 Judging-Winning Combinations

### "Best features" submission:
1. Base game ✓
2. 3 difficulty levels ✓
3. Power-ups ✓  
4. High scores ✓
5. **+ Add**: Pause feature
6. **+ Add**: Statistics display
7. **+ Add**: Achievements

### "Best technical" submission:
1. All above
2. **+ Add**: Modular AI
3. **+ Add**: Custom config system
4. **+ Add**: Replay system
5. **+ Add**: Performance metrics

### "Most fun" submission:
1. All above
2. **+ Add**: More power-up types
3. **+ Add**: Multiplayer mode
4. **+ Add**: Daily challenges
5. **+ Add**: Sound system

---

## ⏰ Time Management Tips

- **0-30 min**: Polish menus, add pause
- **30-60 min**: Add achievements or combo system
- **60-90 min**: Add leaderboard
- **90-120 min**: Add AI or multiplayer
- **Last 10 min**: Commit code, prepare demo

---

## 🎉 Demo Script

Before presenting to judges:

1. **Show Main Menu** (5 sec)
   - "See the clean design and statistics tracking"

2. **Select Difficulty** (5 sec)
   - "3 tuned difficulty levels with different physics"

3. **Play & Collect Power-Ups** (30 sec)
   - "Show all three power-up types"
   - "Notice the particle effects and notifications"

4. **Reach Game Over** (5 sec)
   - "Show statistics and high score saving"

5. **Show Code** (30 sec)
   - "5 modular systems for extensibility"
   - "Show high_score.py, powerups.py"

6. **Explain Architecture** (30 sec)
   - "Separated concerns for easy extension"
   - "Show how to add new power-up type"

---

**Good luck extending! You've got a solid foundation! 🚀**
