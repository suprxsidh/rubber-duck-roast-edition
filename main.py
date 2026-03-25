import pygame
import random
import sys
import math

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rubber Duck Debugging: The Roast Edition")
clock = pygame.time.Clock()

# Enhanced color scheme
WHITE = (255, 255, 255)
BLACK = (10, 10, 20)
YELLOW = (255, 223, 0)
GOLD = (255, 215, 0)
RED = (220, 50, 50)
DARK_RED = (150, 30, 30)
GREEN = (50, 220, 80)
DARK_GREEN = (30, 100, 50)
BLUE = (60, 130, 255)
CYAN = (0, 200, 220)
PURPLE = (180, 80, 220)
PINK = (255, 100, 150)
ORANGE = (255, 150, 50)

GRAY = (100, 100, 120)
DARK_GRAY = (40, 40, 55)
LIGHT_GRAY = (150, 150, 170)

# Background gradient colors
BG_TOP = (15, 15, 35)
BG_BOTTOM = (30, 20, 50)

# Try to use a better font, fallback gracefully
try:
    font_emoji = pygame.font.Font("/System/Library/Fonts/Apple Color Emoji.ttc", 48)
except:
    font_emoji = pygame.font.Font(None, 48)

font_title = pygame.font.Font(None, 56)
font_large = pygame.font.Font(None, 40)
font_medium = pygame.font.Font(None, 28)
font_small = pygame.font.Font(None, 22)
font_tiny = pygame.font.Font(None, 18)


# Visual effects system
class VisualEffects:
    def __init__(self):
        self.screen_flash = None
        self.particles = []
        self.floating_text = []
        self.shake_offset = [0, 0]
        self.shake_duration = 0
    
    def add_screen_flash(self, color, duration=10):
        self.screen_flash = {"color": color, "duration": duration, "alpha": 180}
    
    def add_particle(self, x, y, color, size, velocity, lifetime=30):
        self.particles.append({
            "x": x, "y": y, "color": color, "size": size,
            "vx": velocity[0], "vy": velocity[1],
            "lifetime": lifetime, "max_lifetime": lifetime
        })
    
    def add_floating_text(self, x, y, text, color, lifetime=40):
        self.floating_text.append({
            "x": x, "y": y, "text": text, "color": color,
            "lifetime": lifetime, "max_lifetime": lifetime
        })
    
    def add_shake(self, intensity=10, duration=15):
        self.shake_duration = duration
        self.shake_intensity = intensity
    
    def update(self):
        # Update screen flash
        if self.screen_flash:
            self.screen_flash["duration"] -= 1
            self.screen_flash["alpha"] = max(0, int(180 * (self.screen_flash["duration"] / 10)))
            if self.screen_flash["duration"] <= 0:
                self.screen_flash = None
        
        # Update particles
        for p in self.particles[:]:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["vy"] += 0.1  # gravity
            p["lifetime"] -= 1
            if p["lifetime"] <= 0:
                self.particles.remove(p)
        
        # Update floating text
        for t in self.floating_text[:]:
            t["y"] -= 1.5
            t["lifetime"] -= 1
            if t["lifetime"] <= 0:
                self.floating_text.remove(t)
        
        # Update shake
        if self.shake_duration > 0:
            self.shake_duration -= 1
            self.shake_offset[0] = random.randint(-self.shake_intensity, self.shake_intensity)
            self.shake_offset[1] = random.randint(-self.shake_intensity, self.shake_intensity)
        else:
            self.shake_offset = [0, 0]
    
    def draw(self, surface):
        # Draw particles
        for p in self.particles:
            alpha = int(255 * (p["lifetime"] / p["max_lifetime"]))
            s = pygame.Surface((p["size"]*2, p["size"]*2), pygame.SRCALPHA)
            color = (*p["color"], alpha)
            pygame.draw.circle(s, color, (p["size"], p["size"]), p["size"])
            surface.blit(s, (p["x"] - p["size"], p["y"] - p["size"]))
        
        # Draw floating text
        for t in self.floating_text:
            alpha = int(255 * (t["lifetime"] / t["max_lifetime"]))
            font = font_small if len(t["text"]) < 15 else font_tiny
            text = font.render(t["text"], True, t["color"])
            text.set_alpha(alpha)
            surface.blit(text, (t["x"] - text.get_width()//2, t["y"]))
        
        # Draw screen flash
        if self.screen_flash and self.screen_flash["color"]:
            color = self.screen_flash["color"]
            alpha = self.screen_flash["alpha"]
            if len(color) == 3:
                flash_color = (color[0], color[1], color[2], alpha)
            else:
                flash_color = (*color[:3], alpha)
            flash = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            flash.fill(flash_color)
            surface.blit(flash, (0, 0))
    
    def get_shake_offset(self):
        return self.shake_offset


effects = VisualEffects()


# ASCII art and sprite definitions
DUCK_SPRITE = r"""
    _>
   ( )>
  __"_"___
  _/ \_   \__
 /  o  \     \_
|    __|______)
 \  o/        
  \/
"""

ENEMY_SPRITES = {
    "Syntax Error": r"""
  _____
 |  X  |
 |_____|""",
    "Null Pointer": r"""
  _____
 |NULL |
 |_____|""",
    "Infinite Loop": r"""
 |~~~~~|
 |     |
 |_____|
 |~~~~~|
 |     |""",
    "Memory Leak": r"""
  _____
 |  ~  |
 |~~~~~|
 |_____|""",
    "Race Condition": r"""
  /---\
  |>>>|
  \___/""",
    "Legacy Code Boss": r"""
  _______________
 |   LEGACY     |
 |    BOSS      |
 |_____________|
 |   (O_O)     |
 |_____________|"""
}


def draw_gradient_background(surface):
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(BG_TOP[0] + (BG_BOTTOM[0] - BG_TOP[0]) * ratio)
        g = int(BG_TOP[1] + (BG_BOTTOM[1] - BG_TOP[1]) * ratio)
        b = int(BG_TOP[2] + (BG_BOTTOM[2] - BG_TOP[2]) * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (WIDTH, y))



class RoastEngine:
    def __init__(self):
        self.personalities = ["socratic", "existential", "corporate"]
        self.current_personality = random.choice(self.personalities)
        self.turn_count = 0
        self.mistakes = 0
        self.damage_dealt = 0
        self.damage_taken = 0
        self.victories = 0
        
    def new_game(self):
        self.current_personality = random.choice(self.personalities)
        self.turn_count = 0
        self.mistakes = 0
        self.damage_dealt = 0
        self.damage_taken = 0
        self.victories = 0
    
    def get_roast(self, event_type, context=None):
        self.turn_count += 1
        
        if event_type == "attack":
            return self._roast_attack(context)
        elif event_type == "damage_taken":
            self.damage_taken += context.get("damage", 0)
            return self._roast_damage(context)
        elif event_type == "victory":
            self.victories += 1
            return self._roast_victory(context)
        elif event_type == "defeat":
            return self._roast_defeat(context)
        elif event_type == "mistake":
            self.mistakes += 1
            return self._roast_mistake(context)
        elif event_type == "turn_start":
            return self._roast_turn_start()
        elif event_type == "upgrade":
            return self._roast_upgrade(context)
        elif event_type == "boss_fight":
            return self._roast_boss()
        else:
            return "The duck stares at you in confusion. Even the roast engine is confused."
    
    def _roast_attack(self, context):
        attack_name = context.get("attack", "quack")
        enemy_hp = context.get("enemy_hp", 0)
        
        roasts = {
            "socratic": [
                f"Do you really think {attack_name} is going to solve anything?",
                "Violence isn't the answer, but it certainly feels like one.",
                f"Ah yes, attacking a {enemy_hp} HP enemy with {attack_name}. Revolutionary strategy.",
                "I've seen more creative solutions in a Hello World program.",
                "Is this your first time playing a game? Oh wait, it might be."
            ],
            "existential": [
                f"You attack with {attack_name}. But at what cost?",
                "The bugs aren't the problem. You are.",
                f"In the grand tapestry of code, your {attack_name} means nothing.",
                "You're not fighting bugs. You're fighting your own inadequacy.",
                f"{attack_name}? More like {attack_name[:-2]} of despair."
            ],
            "corporate": [
                f"Let's circle back to why you chose {attack_name}.",
                "I've scheduled a meeting to discuss your combat choices.",
                "Have you considered leveraging a different attack vector?",
                f"{attack_name} is so last sprint. Let's pivot.",
                "The stakeholders have concerns about your {attack_name} selection."
            ]
        }
        return random.choice(roasts[self.current_personality])
    
    def _roast_damage(self, context):
        damage = context.get("damage", 0)
        attacker = context.get("attacker", "bug")
        
        roasts = {
            "socratic": [
                f"Ouch. {damage} damage from a {attacker}. Do you feel good about yourself?",
                "Did you just stand there and take that? Remarkable incompetence.",
                f"The {attacker} is judging you. And honestly, I'm judging you too.",
                "There's no I in team, but there's definitely in damage taken.",
                f"{damage} HP gone. That's not a bug, that's a feature of your playstyle."
            ],
            "existential": [
                f"The void takes {damage} HP. The void is within you.",
                f"You've been damaged for {damage}. Not physically. Existentially.",
                f"{attacker} saw your soul and dealt {damage} psychic damage.",
                "Every bug you defeat brings you closer to the truth: you're the real bug.",
                f"{damage} damage. Your grandmother plays better than this."
            ],
            "corporate": [
                f"{damage} damage? That's going in your performance review.",
                "We need to have a one-on-one about your {damage} HP loss.",
                "The {attacker} team is outperforming you. By {damage} points.",
                "Have you tried not getting hit? It's a novel approach.",
                f"HR has been notified of your {damage} damage incident."
            ]
        }
        return random.choice(roasts[self.current_personality])
    
    def _roast_victory(self, context):
        enemy = context.get("enemy", "bug")
        
        roasts = {
            "socratic": [
                f"You defeated a {enemy}. Before you celebrate, ask yourself: was it worth it?",
                f"Another {enemy} bites the dust. Are you the hero or the villain?",
                "Victory is fleeting. Your inadequacy is eternal.",
                f"Congratulations on beating {enemy}. The real challenge is next.",
                "You won. But at what cost? (The cost was your time.)"
            ],
            "existential": [
                f"The {enemy} is gone. And yet, you still remain.",
                f"You've slain {enemy}. The void grows larger.",
                "Victory against {enemy} means nothing in a universe of bugs.",
                f"Another {enemy} defeated. Your soul grows heavier.",
                "You celebrate? The bugs are laughing. In the code."
            ],
            "corporate": [
                f"Great job defeating {enemy}. Let's pivot to the next KPI.",
                "{enemy} neutralized. Updating your OKRs.",
                "That's one small step for duck, one giant leap for your leaderboard.",
                f"Another {enemy} closed. Are we on track for Q4 goals?",
                "Victory! But can we scale this? What's the ROI on that {enemy}?"
            ]
        }
        return random.choice(roasts[self.current_personality]).format(enemy=enemy)
    
    def _roast_defeat(self, context):
        roasts = {
            "socratic": [
                "You died. The bugs win. Have you learned nothing?",
                "Game over. And honestly, it was coming.",
                "Did you think you could actually win? That's adorable.",
                "The bugs have consumed you. As they should.",
                "Your duck has been pwned. N00b."
            ],
            "existential": [
                "You are dead. But then, you were always dead inside.",
                "Game over. The void welcomes you home.",
                "Your duck is gone. The code persists. Nothing matters.",
                "Death is just a bug in the simulation. You're the feature.",
                "You failed. And yet, you still tried. How noble. How futile."
            ],
            "corporate": [
                "Let's schedule a post-mortem on your performance.",
                "Your duck has been let go. Sorry, it's just business.",
                "That's a termination-worthy performance. Quack.",
                "HR will reach out about your sudden career change.",
                "We're going in a different direction. Specifically, away from you."
            ]
        }
        return random.choice(roasts[self.current_personality])
    
    def _roast_mistake(self, context):
        mistake = context.get("mistake", "error")
        
        roasts = {
            "socratic": [
                f"You made a {mistake}. Do you even know what you're doing?",
                f"Interesting choice: {mistake}. Was that a bug or a feature?",
                f"I've seen better decisions in production code from 1998.",
                "That's not a mistake, that's your entire playstyle.",
                f"{mistake}? Really? I'm speechless. Almost."
            ],
            "existential": [
                f"You chose {mistake}. And in choosing, you defined yourself.",
                f"{mistake} echoes through the void of your gameplay.",
                "Every mistake brings you closer to the truth: you're the bug.",
                f"{mistake} - the name of your autobiography.",
                "Your decisions are the real bug in this system."
            ],
            "corporate": [
                f"Documentation note: {mistake} is not best practice.",
                "We need to discuss your {mistake} in our next sync.",
                "That's a red flag. Multiple red flags. A whole flag factory.",
                f"I've added {mistake} to your permanent record.",
                "Your decision-making needs work. And everything else."
            ]
        }
        return random.choice(roasts[self.current_personality])
    
    def _roast_turn_start(self):
        if self.turn_count == 1:
            return f"A new game begins. The {self.current_personality} roast master awakens."
        
        roasts = {
            "socratic": [
                "Your turn. Try not to embarrass yourself.",
                "Another turn. Another chance to fail creatively.",
                "The duck awaits your command. Foolish mortal."
            ],
            "existential": [
                "Time passes. Bugs persist. You endure, inexplicably.",
                "Another turn in the eternal battle against code.",
                "The duck quacks. The void listens."
            ],
            "corporate": [
                "Sprint {turn} begins. What's the velocity? Low, presumably.".format(turn=self.turn_count),
                "New turn, same duck. Let's make this one count.",
                "Daily standup: what's your plan for this turn?"
            ]
        }
        return random.choice(roasts[self.current_personality])
    
    def _roast_upgrade(self, context):
        upgrade = context.get("upgrade", "something")
        
        roasts = {
            "socratic": [
                f"You upgraded {upgrade}. Will it matter? Unclear.",
                f"{upgrade}. A bold choice. We shall see.",
                "Upgrading is nice. Using it correctly is another matter."
            ],
            "existential": [
                f"You cling to {upgrade} like a life raft in the void.",
                f"{upgrade} won't save you. Nothing will.",
                "More power, more responsibility, more disappointment."
            ],
            "corporate": [
                f"Great investment in {upgrade}. ROI: TBD.",
                f"Upgrading {upgrade}. Let me know when it's ready for review.",
                f"{upgrade} approved. Moving to the next backlog item."
            ]
        }
        return random.choice(roasts[self.current_personality])
    
    def _roast_boss(self):
        roasts = {
            "socratic": [
                "Ah, the Legacy Code Boss. The real enemy was always technical debt.",
                "The boss approaches. Are you ready? No, clearly not.",
                "This is it. The final boss. Try not to die immediately."
            ],
            "existential": [
                "The Legacy Code Boss emerges from the depths of forgotten repos.",
                "You face the ultimate enemy: code written by someone else.",
                "This is where your journey ends. Or begins again. Does it matter?"
            ],
            "corporate": [
                "The boss has entered the arena. Time to deliver or get pip'd.",
                "Final boss: Legacy Code. The stakeholder is watching.",
                "This is your big moment. Don't mess it up. (You'll mess it up.)"
            ]
        }
        return random.choice(roasts[self.current_personality])


class Entity:
    def __init__(self, name, hp, max_hp, attack, defense, emoji):
        self.name = name
        self.hp = hp
        self.max_hp = max_hp
        self.attack = attack
        self.defense = defense
        self.emoji = emoji
    
    def is_alive(self):
        return self.hp > 0
    
    def take_damage(self, damage):
        actual_damage = max(1, damage - self.defense)
        self.hp = max(0, self.hp - actual_damage)
        return actual_damage
    
    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)


class Player(Entity):
    def __init__(self):
        super().__init__("Rubber Duck", 100, 100, 20, 5, "DUCK")
        self.xp = 0
        self.level = 1
        self.gold = 0
        self.actions_per_turn = 2
        self.actions_used = 0
        
        self.attacks = {
            "Quack": {"damage": 15, "accuracy": 95, "description": "Basic quack attack"},
            "Splash": {"damage": 10, "accuracy": 90, "description": "Water splash, hits all"},
            "Rubber Beak": {"damage": 25, "accuracy": 70, "description": "Powerful beak attack"},
            "Existential Crisis": {"damage": 5, "accuracy": 100, "description": "Confuse enemies, reduces their attack"},
            "Float Above": {"damage": 0, "accuracy": 100, "description": "Dodge next attack"},
        }
        
        self.upgrades = {
            "Golden Beak": {"cost": 50, "effect": "attack", "value": 10, "description": "+10 Attack"},
            "Extra Floaties": {"cost": 50, "effect": "defense", "value": 10, "description": "+10 Defense"},
            "Vitamin D": {"cost": 40, "effect": "heal", "value": 30, "description": "Heal 30 HP"},
            "XP Boost": {"cost": 60, "effect": "xp_boost", "value": 20, "description": "+20% XP gain"},
            "Lucky Quack": {"cost": 45, "effect": "crit", "value": 15, "description": "+15% Crit chance"},
            "Rubber Soul": {"cost": 70, "effect": "max_hp", "value": 30, "description": "+30 Max HP"},
            "Sonic Quack": {"damage": 20, "accuracy": 80, "description": "New attack: stuns enemy"},
        }
        
        self.active_upgrades = []
        self.crit_chance = 10
        self.xp_multiplier = 1.0
        self.dodging = False
    
    def reset_turn(self):
        self.actions_used = 0
        self.dodging = False
    
    def can_act(self):
        return self.actions_used < self.actions_per_turn
    
    def attack_target(self, attack_name, target):
        if attack_name not in self.attacks:
            return 0, False
        
        attack = self.attacks[attack_name]
        if random.random() * 100 > attack["accuracy"]:
            return 0, False
        
        damage = attack["damage"]
        crit = random.random() * 100 < self.crit_chance
        if crit:
            damage *= 2
        
        for upgrade in self.active_upgrades:
            if upgrade["effect"] == "attack":
                damage += upgrade["value"]
        
        actual_damage = target.take_damage(damage)
        return actual_damage, crit


class Enemy(Entity):
    ENEMY_TYPES = {
        "Syntax Error": {"hp": 30, "attack": 8, "defense": 2, "emoji": "X", "xp": 10, "gold": 5},
        "Null Pointer": {"hp": 25, "attack": 12, "defense": 0, "emoji": "NULL", "xp": 12, "gold": 8},
        "Infinite Loop": {"hp": 50, "attack": 5, "defense": 5, "emoji": "LOOP", "xp": 20, "gold": 15},
        "Memory Leak": {"hp": 35, "attack": 10, "defense": 3, "emoji": "LEAK", "xp": 15, "gold": 10},
        "Race Condition": {"hp": 40, "attack": 15, "defense": 2, "emoji": "RACE", "xp": 18, "gold": 12},
        "Legacy Code Boss": {"hp": 200, "attack": 25, "defense": 10, "emoji": "BOSS", "xp": 100, "gold": 100},
    }
    
    def __init__(self, enemy_type=None):
        if enemy_type is None:
            enemy_type = random.choice(list(self.ENEMY_TYPES.keys())[:-1])
        
        stats = self.ENEMY_TYPES[enemy_type]
        super().__init__(enemy_type, stats["hp"], stats["hp"], stats["attack"], stats["defense"], stats["emoji"])
        self.xp_reward = stats["xp"]
        self.gold_reward = stats["gold"]
        self.enemy_type = enemy_type
    
    def enemy_attack(self, player):
        if player.dodging:
            player.dodging = False
            return 0, True
        
        actual_damage = player.take_damage(self.attack)
        return actual_damage, False


class Game:
    def __init__(self):
        self.roast_engine = RoastEngine()
        self.player = Player()
        self.enemies = []
        self.current_enemy_index = 0
        self.game_state = "menu"
        self.roast_message = "Welcome to Rubber Duck Debugging: The Roast Edition!"
        self.floor = 1
        self.high_score = 0
        self.score = 0
        
        self.generate_floor()
    
    def generate_floor(self):
        self.enemies = []
        enemy_count = min(2 + self.floor // 2, 5)
        
        if self.floor % 5 == 0:
            self.enemies.append(Enemy("Legacy Code Boss"))
        else:
            for _ in range(enemy_count):
                self.enemies.append(Enemy())
        
        self.current_enemy_index = 0
        self.roast_message = self.roast_engine.get_roast("turn_start")
    
    def get_current_enemy(self):
        if self.current_enemy_index < len(self.enemies):
            return self.enemies[self.current_enemy_index]
        return None
    
    def player_attack(self, attack_name):
        global effects
        if not self.player.can_act():
            return "No actions left!"
        
        enemy = self.get_current_enemy()
        if not enemy:
            return "No enemy to attack!"
        
        self.player.actions_used += 1
        
        if attack_name == "Float Above":
            self.player.dodging = True
            self.roast_message = self.roast_engine.get_roast("attack", {"attack": attack_name, "enemy_hp": enemy.hp})
            effects.add_floating_text(WIDTH//2, 300, "Dodging!", CYAN, 30)
            return f"[DEF] You float above! Next attack will be dodged!"
        
        damage, crit = self.player.attack_target(attack_name, enemy)
        
        if damage == 0:
            self.roast_message = self.roast_engine.get_roast("mistake", {"mistake": "missed attack"})
            effects.add_floating_text(WIDTH//2, 300, "MISS!", GRAY, 30)
            return f"[MISS] You missed with {attack_name}!"
        
        self.roast_message = self.roast_engine.get_roast("attack", {"attack": attack_name, "enemy_hp": enemy.hp})
        
        # Visual effects for attack
        effects.add_screen_flash(RED, 8)
        effects.add_shake(8, 10)
        
        # Attack particles
        for _ in range(8):
            effects.add_particle(
                WIDTH//2 + 150, 300,
                RED if crit else ORANGE,
                random.randint(3, 8),
                (random.uniform(-3, 3), random.uniform(-2, -5)),
                25
            )
        
        result = f"[ATK] You used {attack_name}! "
        if crit:
            result += f"CRITICAL HIT! "
            effects.add_floating_text(WIDTH//2, 280, "CRITICAL!", GOLD, 40)
            effects.add_screen_flash(GOLD, 15)
        result += f"Dealt {damage} damage!"
        
        effects.add_floating_text(WIDTH//2, 260, f"-{damage}", WHITE if not crit else GOLD, 35)
        
        self.score += damage
        
        if not enemy.is_alive():
            # Death effect
            for _ in range(20):
                effects.add_particle(
                    WIDTH//2 + 150, 300,
                    random.choice([RED, ORANGE, PURPLE]),
                    random.randint(5, 12),
                    (random.uniform(-5, 5), random.uniform(-6, -2)),
                    40
                )
            effects.add_screen_flash(PURPLE, 20)
            effects.add_shake(15, 20)
            
            self.player.xp += enemy.xp_reward * self.player.xp_multiplier
            self.player.gold += enemy.gold_reward
            self.roast_message = self.roast_engine.get_roast("victory", {"enemy": enemy.name})
            result += f"\n[VICTORY] {enemy.name} defeated! +{int(enemy.xp_reward * self.player.xp_multiplier)} XP, {enemy.gold_reward} gold!"
            
            self.current_enemy_index += 1
            if self.current_enemy_index >= len(self.enemies):
                if self.floor >= 5 and self.floor % 5 == 0:
                    self.game_state = "victory"
                else:
                    self.floor += 1
                    self.generate_floor()
        
        return result
    
    def enemy_turn(self):
        global effects
        enemy = self.get_current_enemy()
        if not enemy:
            return
        
        damage, dodged = enemy.enemy_attack(self.player)
        
        if dodged:
            self.roast_message = "You dodged the attack! Even the roast engine is surprised."
            effects.add_floating_text(WIDTH//2 - 150, 300, "DODGED!", CYAN, 30)
            effects.add_screen_flash(CYAN, 10)
        else:
            self.roast_message = self.roast_engine.get_roast("damage_taken", {"damage": damage, "attacker": enemy.name})
            # Damage effects
            effects.add_screen_flash(DARK_RED, 12)
            effects.add_shake(12, 15)
            
            for _ in range(10):
                effects.add_particle(
                    WIDTH//2 - 150, 300,
                    RED,
                    random.randint(4, 10),
                    (random.uniform(-4, 4), random.uniform(-3, -6)),
                    25
                )
            
            effects.add_floating_text(WIDTH//2 - 150, 260, f"-{damage}", RED, 35)
        
        self.score += damage // 2
        
        if not self.player.is_alive():
            self.game_state = "defeat"
            self.roast_message = self.roast_engine.get_roast("defeat", {})
            effects.add_screen_flash(DARK_RED, 30)
            if self.score > self.high_score:
                self.high_score = self.score
    
    def buy_upgrade(self, upgrade_name):
        global effects
        if upgrade_name not in self.player.upgrades:
            return "Upgrade not found!"
        
        upgrade = self.player.upgrades[upgrade_name]
        if self.player.gold < upgrade["cost"]:
            return "Not enough gold!"
        
        self.player.gold -= upgrade["cost"]
        
        # Upgrade effects
        effects.add_screen_flash(GREEN, 15)
        for _ in range(15):
            effects.add_particle(
                WIDTH//2, HEIGHT//2,
                random.choice([GOLD, YELLOW, GREEN]),
                random.randint(4, 10),
                (random.uniform(-4, 4), random.uniform(-5, -2)),
                35
            )
        
        if upgrade_name == "Sonic Quack":
            self.player.attacks["Sonic Quack"] = {"damage": upgrade["damage"], "accuracy": upgrade["accuracy"], "description": upgrade["description"]}
        else:
            self.player.active_upgrades.append(upgrade)
            if upgrade["effect"] == "max_hp":
                self.player.max_hp += upgrade["value"]
                self.player.hp += upgrade["value"]
                effects.add_floating_text(WIDTH//2, HEIGHT//2 - 50, f"+{upgrade['value']} HP", GREEN, 40)
            elif upgrade["effect"] == "crit":
                self.player.crit_chance += upgrade["value"]
                effects.add_floating_text(WIDTH//2, HEIGHT//2 - 50, f"+{upgrade['value']}% Crit", GOLD, 40)
            elif upgrade["effect"] == "xp_boost":
                self.player.xp_multiplier += upgrade["value"] / 100
                effects.add_floating_text(WIDTH//2, HEIGHT//2 - 50, f"+{upgrade['value']}% XP", CYAN, 40)
        
        self.roast_message = self.roast_engine.get_roast("upgrade", {"upgrade": upgrade_name})
        return f"[BOUGHT] {upgrade_name}!"
    
    def heal_player(self):
        global effects
        if self.player.gold >= 30:
            self.player.gold -= 30
            old_hp = self.player.hp
            self.player.heal(40)
            healed_amount = self.player.hp - old_hp
            
            # Heal effects
            effects.add_screen_flash(GREEN, 12)
            for _ in range(12):
                effects.add_particle(
                    WIDTH//2 - 150, 300,
                    GREEN,
                    random.randint(4, 8),
                    (random.uniform(-3, 3), random.uniform(-4, -2)),
                    30
                )
            effects.add_floating_text(WIDTH//2 - 150, 260, f"+{healed_amount} HP", GREEN, 35)
            return f"[HEALED] Healed for {healed_amount} HP!"
        return "Not enough gold! (Need 30)"
    
    def start_new_game(self):
        global effects
        self.player = Player()
        self.floor = 1
        self.score = 0
        self.roast_engine.new_game()
        self.generate_floor()
        self.game_state = "playing"
        self.roast_message = self.roast_engine.get_roast("turn_start")
        effects = VisualEffects()  # Reset visual effects for new game


def draw_text(surface, text, x, y, font, color=WHITE, max_width=None, align="left"):
    if max_width:
        words = text.split()
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + " " + word if current_line else word
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        
        for i, line in enumerate(lines):
            text_surface = font.render(line, True, color)
            if align == "center":
                surface.blit(text_surface, (x - text_surface.get_width() // 2, y + i * font.get_height()))
            else:
                surface.blit(text_surface, (x, y + i * font.get_height()))
    else:
        text_surface = font.render(text, True, color)
        if align == "center":
            surface.blit(text_surface, (x - text_surface.get_width() // 2, y))
        else:
            surface.blit(text_surface, (x, y))


def draw_health_bar(surface, x, y, hp, max_hp, width=200, height=24, show_text=True):
    # Background
    bg_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(surface, DARK_GRAY, bg_rect, border_radius=4)
    
    # Health fill with gradient
    if max_hp > 0:
        fill_width = int((hp / max_hp) * (width - 4))
        if fill_width > 0:
            # Create gradient effect
            for i in range(fill_width):
                ratio = i / fill_width
                if hp > max_hp * 0.5:
                    r = int(GREEN[0] + (YELLOW[0] - GREEN[0]) * ratio * 2) if ratio < 0.5 else int(YELLOW[0] + (RED[0] - YELLOW[0]) * (ratio - 0.5) * 2)
                    g = int(GREEN[1] + (YELLOW[1] - GREEN[1]) * ratio * 2) if ratio < 0.5 else int(YELLOW[1] + (RED[1] - YELLOW[1]) * (ratio - 0.5) * 2)
                    b = int(GREEN[2] + (YELLOW[2] - GREEN[2]) * ratio * 2) if ratio < 0.5 else int(YELLOW[2] + (RED[2] - YELLOW[2]) * (ratio - 0.5) * 2)
                else:
                    r = int(RED[0] * 0.7 + 100 * ratio)
                    g = int(RED[1] * 0.7 + 50 * ratio)
                    b = int(RED[2] * 0.7 + 50 * ratio)
                pygame.draw.line(surface, (r, g, b), (x + 2 + i, y + 2), (x + 2 + i, y + height - 2))
    
    # Border
    border_color = WHITE if hp > max_hp * 0.3 else RED
    pygame.draw.rect(surface, border_color, bg_rect, 2, border_radius=4)
    
    # HP text
    if show_text:
        text = font_small.render(f"{hp}/{max_hp}", True, WHITE)
        surface.blit(text, (x + width // 2 - text.get_width() // 2, y + 3))
    
    # Add small decorative corners
    pygame.draw.circle(surface, GOLD, (x + 4, y + 4), 2)
    pygame.draw.circle(surface, GOLD, (x + width - 4, y + 4), 2)
    pygame.draw.circle(surface, GOLD, (x + 4, y + height - 4), 2)
    pygame.draw.circle(surface, GOLD, (x + width - 4, y + height - 4), 2)


def draw_entity_sprite(surface, x, y, sprite_type, name, hp, max_hp, size=80):
    # Draw the sprite area background
    sprite_bg = pygame.Rect(x - size//2 - 10, y - size//2 - 30, size + 20, size + 60)
    pygame.draw.rect(surface, DARK_GRAY, sprite_bg, border_radius=8)
    pygame.draw.rect(surface, PURPLE, sprite_bg, 2, border_radius=8)
    
    # Draw ASCII art based on type
    if sprite_type == "player":
        lines = DUCK_SPRITE.strip().split('\n')
    else:
        lines = ENEMY_SPRITES.get(name, "").strip().split('\n') if name in ENEMY_SPRITES else ["???", "???"]
    
    line_height = 14
    start_y = y - size//2 - 20
    for i, line in enumerate(lines):
        text = font_tiny.render(line, True, YELLOW if sprite_type == "player" else RED)
        surface.blit(text, (x - text.get_width() // 2, start_y + i * line_height))
    
    # Draw name
    name_text = font_small.render(name, True, WHITE)
    surface.blit(name_text, (x - name_text.get_width() // 2, y + size//2 - 10))
    
    # Draw health bar below
    draw_health_bar(surface, x - 80, y + size//2 + 5, hp, max_hp, 160, 16)


def draw_battle_scene(surface, game, center_x, center_y):
    enemy = game.get_current_enemy()
    
    # Draw battle background with animated elements
    battle_bg = pygame.Rect(50, 140, WIDTH - 100, 350)
    pygame.draw.rect(surface, (20, 20, 40), battle_bg, border_radius=12)
    pygame.draw.rect(surface, PURPLE, battle_bg, 3, border_radius=12)
    
    # Draw floor indicator
    pygame.draw.line(surface, (80, 80, 100), (80, 480), (WIDTH - 80, 480), 2)
    
    if enemy:
        # Enemy position with slight animation
        enemy_x = center_x + 150
        enemy_y = center_y - 30
        
        # Draw enemy with glow effect
        for i in range(3):
            glow_size = 100 + i * 10
            glow_alpha = 30 - i * 10
            glow_surf = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (*RED, glow_alpha), (glow_size//2, glow_size//2), glow_size//2)
            surface.blit(glow_surf, (enemy_x - glow_size//2, enemy_y - glow_size//2))
        
        draw_entity_sprite(surface, enemy_x, enemy_y, "enemy", enemy.name, enemy.hp, enemy.max_hp)
    
    # Player position with animation
    player_x = center_x - 150
    player_y = center_y - 30
    
    # Draw player with glow effect
    for i in range(3):
        glow_size = 90 + i * 10
        glow_alpha = 30 - i * 10
        glow_surf = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (*YELLOW, glow_alpha), (glow_size//2, glow_size//2), glow_size//2)
        surface.blit(glow_surf, (player_x - glow_size//2, player_y - glow_size//2))
    
    draw_entity_sprite(surface, player_x, player_y, "player", game.player.name, game.player.hp, game.player.max_hp)
    
    # VS indicator
    vs_text = font_large.render("VS", True, WHITE)
    pygame.draw.circle(surface, DARK_GRAY, (center_x, center_y + 20), 30)
    pygame.draw.circle(surface, RED, (center_x, center_y + 20), 30, 2)
    surface.blit(vs_text, (center_x - vs_text.get_width() // 2, center_y + 8))
    
    return player_y


def draw_game(screen, game):
    draw_gradient_background(screen)
    
    # Apply shake offset
    shake = effects.get_shake_offset()
    screen_copy = screen.copy()
    
    # Title section with better styling
    title = font_title.render("RUBBER DUCK DEBUGGING", True, YELLOW)
    subtitle = font_large.render("THE ROAST EDITION", True, GOLD)
    
    # Title background
    title_bg = pygame.Rect(WIDTH//2 - 300, 10, 600, 70)
    pygame.draw.rect(screen, DARK_GRAY, title_bg, border_radius=8)
    pygame.draw.rect(screen, (60, 40, 80), title_bg, 2, border_radius=8)
    
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))
    screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, 60))
    
    # Floor indicator with icon
    floor_box = pygame.Rect(WIDTH - 180, 25, 160, 40)
    pygame.draw.rect(screen, DARK_GRAY, floor_box, border_radius=6)
    pygame.draw.rect(screen, CYAN, floor_box, 2, border_radius=6)
    floor_text = font_medium.render(f"Floor {game.floor}", True, CYAN)
    screen.blit(floor_text, (WIDTH - 170, 32))
    
    # Turn indicator
    turn_text = font_small.render(f"Turn: {game.roast_engine.turn_count}", True, LIGHT_GRAY)
    screen.blit(turn_text, (30, 35))
    
    # Draw battle scene
    center_x = WIDTH // 2
    center_y = 340
    duck_y = draw_battle_scene(screen, game, center_x, center_y)
    
    # Roast message panel - more prominent
    roast_panel_y = 510
    roast_panel = pygame.Rect(40, roast_panel_y, WIDTH - 80, 120)
    pygame.draw.rect(screen, (25, 20, 45), roast_panel, border_radius=12)
    pygame.draw.rect(screen, PURPLE, roast_panel, 3, border_radius=12)
    
    # Roast label with glow effect
    roast_label = font_medium.render("THE ROAST", True, GOLD)
    screen.blit(roast_label, (60, roast_panel_y + 10))
    
    # Decorative quote marks
    quote_font = font_title
    screen.blit(quote_font.render('"', True, PURPLE), (45, roast_panel_y + 5))
    screen.blit(quote_font.render('"', True, PURPLE), (WIDTH - 60, roast_panel_y + 50))
    
    # Roast message with typewriter effect feel
    draw_text(screen, game.roast_message, 60, roast_panel_y + 40, font_medium, WHITE, WIDTH - 150)
    
    # Action feedback indicator
    action_hint = font_small.render("Press 1-7 to attack | ENTER to end turn | U for upgrades | H to heal", True, (120, 120, 140))
    screen.blit(action_hint, (WIDTH // 2 - action_hint.get_width() // 2, roast_panel_y + 95))
    
    # Stats bar at bottom
    stats_panel = pygame.Rect(40, 650, WIDTH - 80, 60)
    pygame.draw.rect(screen, DARK_GRAY, stats_panel, border_radius=8)
    pygame.draw.rect(screen, (50, 50, 70), stats_panel, 2, border_radius=8)
    
    # Stats with icons
    stats = [
        (f"{game.player.gold}", GOLD, "Gold"),
        (f"{int(game.player.xp)}", CYAN, "XP"),
        (f"Lv {game.player.level}", GREEN, "Level"),
        (f"{game.score}", WHITE, "Score"),
        (f"{game.high_score}", RED, "Best"),
    ]
    
    for i, (value, color, label) in enumerate(stats):
        x = 80 + i * 200
        label_text = font_small.render(label, True, (100, 100, 120))
        screen.blit(label_text, (x, 660))
        value_text = font_large.render(value, True, color)
        screen.blit(value_text, (x, 680))
    
    # Draw visual effects
    effects.draw(screen)
    
    return duck_y


def draw_menu(screen, game):
    draw_gradient_background(screen)
    
    # Title with glow effect
    for i in range(5):
        glow_surface = pygame.Surface((600, 120), pygame.SRCALPHA)
        alpha = 40 - i * 8
        pygame.draw.rect(glow_surface, (*YELLOW, alpha), (0, 0, 600, 120), border_radius=20)
        screen.blit(glow_surface, (WIDTH//2 - 300, 120))
    
    title_box = pygame.Rect(WIDTH//2 - 280, 130, 560, 100)
    pygame.draw.rect(screen, DARK_GRAY, title_box, border_radius=12)
    pygame.draw.rect(screen, YELLOW, title_box, 3, border_radius=12)
    
    title = font_title.render("RUBBER DUCK DEBUGGING", True, YELLOW)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 150))
    
    subtitle = font_large.render("THE ROAST EDITION", True, GOLD)
    screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, 200))
    
    # Duck sprite display
    duck_box = pygame.Rect(WIDTH//2 - 100, 280, 200, 120)
    pygame.draw.rect(screen, (30, 30, 50), duck_box, border_radius=10)
    pygame.draw.rect(screen, YELLOW, duck_box, 2, border_radius=10)
    
    lines = DUCK_SPRITE.strip().split('\n')
    for i, line in enumerate(lines):
        text = font_tiny.render(line, True, YELLOW)
        screen.blit(text, (WIDTH//2 - text.get_width()//2, 300 + i * 16))
    
    # Start button with animation hint
    start_text = font_large.render("Press ENTER to Start", True, GREEN)
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, 430))
    
    # How to Play button
    howto_box = pygame.Rect(WIDTH//2 - 80, 480, 160, 40)
    pygame.draw.rect(screen, (60, 40, 80), howto_box, border_radius=8)
    pygame.draw.rect(screen, PURPLE, howto_box, 2, border_radius=8)
    howto_text = font_medium.render("HOW TO PLAY", True, WHITE)
    screen.blit(howto_text, (WIDTH//2 - howto_text.get_width()//2, 490))
    
    # High score
    high_box = pygame.Rect(WIDTH//2 - 120, 540, 240, 35)
    pygame.draw.rect(screen, DARK_GRAY, high_box, border_radius=6)
    high_text = font_small.render(f"High Score: {game.high_score}", True, GOLD)
    screen.blit(high_text, (WIDTH // 2 - high_text.get_width() // 2, 550))


def draw_how_to_play(screen):
    draw_gradient_background(screen)
    
    # Title
    title = font_title.render("HOW TO PLAY", True, YELLOW)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
    
    # Back hint
    back_text = font_medium.render("Press H to go back", True, CYAN)
    screen.blit(back_text, (WIDTH // 2 - back_text.get_width() // 2, 100))
    
    # Left panel - Gameplay
    left_panel = pygame.Rect(50, 150, 500, 550)
    pygame.draw.rect(screen, (20, 20, 35), left_panel, border_radius=15)
    pygame.draw.rect(screen, CYAN, left_panel, 3, border_radius=15)
    
    left_title = font_large.render("GAMEPLAY", True, YELLOW)
    screen.blit(left_title, (70, 165))
    
    gameplay_info = [
        ("OBJECTIVE", GOLD),
        ("Defeat the Legacy Code Boss on Floor 5!", WHITE),
        ("", None),
        ("COMBAT", GOLD),
        ("- You have 2 actions per turn", WHITE),
        ("- Use attacks to damage bugs", WHITE),
        ("- Each bug has HP, Attack & Defense", WHITE),
        ("- Defeat all bugs to advance floors", WHITE),
        ("- Boss appears every 5 floors", WHITE),
        ("", None),
        ("UPGRADES", GOLD),
        ("- Earn gold by defeating enemies", WHITE),
        ("- Buy upgrades between battles", WHITE),
        ("- Upgrades boost attack, defense, HP", WHITE),
        ("", None),
        ("TIPS", GOLD),
        ("- Watch your HP - it doesn't auto-heal", WHITE),
        ("- Heal costs 30 gold when needed", WHITE),
        ("- Prioritize upgrades that match your style", WHITE),
    ]
    
    y = 210
    for item in gameplay_info:
        if item[1] is None:
            y += 15
        elif item[0] in ("OBJECTIVE", "COMBAT", "UPGRADES", "TIPS"):
            font = font_medium
            y += 10
        else:
            font = font_small
        rendered = font.render(item[0], True, item[1] if item[1] else WHITE)
        screen.blit(rendered, (70, y))
        y += 28 if item[0] in ("OBJECTIVE", "COMBAT", "UPGRADES", "TIPS") else 22
    
    # Right panel - Controls
    right_panel = pygame.Rect(580, 150, 550, 550)
    pygame.draw.rect(screen, (20, 20, 35), right_panel, border_radius=15)
    pygame.draw.rect(screen, PURPLE, right_panel, 3, border_radius=15)
    
    right_title = font_large.render("CONTROLS", True, YELLOW)
    screen.blit(right_title, (600, 165))
    
    controls_info = [
        ("KEY", WHITE),
        ("1-7", CYAN),
        ("Use attack (number = attack slot)", GRAY),
        ("", None),
        ("KEY", WHITE),
        ("ENTER", CYAN),
        ("End your turn / Start game", GRAY),
        ("", None),
        ("KEY", WHITE),
        ("U", CYAN),
        ("Open upgrade shop", GRAY),
        ("", None),
        ("KEY", WHITE),
        ("H", CYAN),
        ("Heal 40 HP (costs 30 gold)", GRAY),
        ("", None),
        ("KEY", WHITE),
        ("ESC", CYAN),
        ("Close upgrade shop", GRAY),
        ("", None),
        ("KEY", WHITE),
        ("1-7 (in shop)", CYAN),
        ("Buy upgrade (number = upgrade slot)", GRAY),
    ]
    
    y = 210
    i = 0
    while i < len(controls_info):
        item = controls_info[i]
        
        # Handle empty rows
        if len(item) == 2 and item[1] is None:
            y += 15
            i += 1
            continue
        
        # Check if this is a "KEY" label row
        if len(item) == 2 and item[0] == "KEY":
            label = font_small.render(item[0], True, (100, 100, 100))
            screen.blit(label, (620, y))
            y += 20
            i += 1
            continue
        
        # Otherwise it's a key+description pair (3 elements)
        if len(item) >= 3:
            key = font_medium.render(item[0], True, item[1])
            screen.blit(key, (620, y))
            desc = font_small.render(item[2], True, item[2])
            screen.blit(desc, (700, y + 3))
            y += 30
        
        i += 1


def draw_attack_menu(screen, game, duck_y):
    menu_x = WIDTH - 300
    menu_y = max(150, duck_y - 100)
    
    # Menu panel - bigger and more readable
    menu_width = 280
    menu_height = 450
    menu_bg = pygame.Rect(menu_x, menu_y, menu_width, menu_height)
    pygame.draw.rect(screen, (20, 20, 35), menu_bg, border_radius=15)
    pygame.draw.rect(screen, CYAN, menu_bg, 3, border_radius=15)
    
    # Title with keyboard hint style
    title = font_large.render("ATTACKS", True, YELLOW)
    screen.blit(title, (menu_x + 20, menu_y + 15))
    
    # Actions remaining
    actions_left = game.player.actions_per_turn - game.player.actions_used
    actions_text = font_medium.render(f"Actions: {actions_left}/{game.player.actions_per_turn}", True, GREEN if actions_left > 0 else RED)
    screen.blit(actions_text, (menu_x + 20, menu_y + 50))
    
    # Attack list with keyboard indicators
    y_offset = 90
    for i, (name, attack) in enumerate(game.player.attacks.items()):
        key = str(i + 1)
        can_use = game.player.can_act()
        
        # Row background
        row_bg = pygame.Rect(menu_x + 10, menu_y + y_offset, menu_width - 20, 50)
        bg_color = (40, 40, 60) if can_use else (25, 25, 30)
        pygame.draw.rect(screen, bg_color, row_bg, border_radius=8)
        
        # Key indicator box - bigger
        key_box = pygame.Rect(menu_x + 20, menu_y + y_offset + 10, 36, 36)
        key_bg = PURPLE if can_use else (50, 50, 50)
        pygame.draw.rect(screen, key_bg, key_box, border_radius=6)
        pygame.draw.rect(screen, WHITE if can_use else GRAY, key_box, 2, border_radius=6)
        key_text = font_medium.render(key, True, WHITE if can_use else GRAY)
        screen.blit(key_text, (menu_x + 26, menu_y + y_offset + 15))
        
        # Attack name - bigger font
        atk_text = f"{name}"
        atk_render = font_medium.render(atk_text, True, WHITE if can_use else GRAY)
        screen.blit(atk_render, (menu_x + 70, menu_y + y_offset + 5))
        
        # Damage/accuracy info - more visible
        info_text = f"{attack['damage']} DMG  |  {attack['accuracy']}% ACC"
        info_render = font_small.render(info_text, True, CYAN if can_use else GRAY)
        screen.blit(info_render, (menu_x + 70, menu_y + y_offset + 28))
        
        y_offset += 58
    
    # Actions section
    actions_y = menu_y + y_offset + 10
    
    # Divider
    pygame.draw.line(screen, GRAY, (menu_x + 20, actions_y), (menu_x + menu_width - 20, actions_y), 2)
    actions_y += 15
    
    # End turn indicator - bigger button
    enter_box = pygame.Rect(menu_x + 10, actions_y, menu_width - 20, 40)
    pygame.draw.rect(screen, (30, 80, 30), enter_box, border_radius=8)
    pygame.draw.rect(screen, GREEN, enter_box, 2, border_radius=8)
    enter_text = font_medium.render("[ENTER] End Turn", True, WHITE)
    screen.blit(enter_text, (menu_x + 30, actions_y + 8))
    
    # Upgrade and heal - bigger buttons
    pygame.draw.rect(screen, (80, 40, 80), (menu_x + 10, actions_y + 50, 125, 35), border_radius=6)
    pygame.draw.rect(screen, PURPLE, (menu_x + 10, actions_y + 50, 125, 35), 2, border_radius=6)
    
    pygame.draw.rect(screen, (40, 80, 40), (menu_x + 145, actions_y + 50, 125, 35), border_radius=6)
    pygame.draw.rect(screen, GREEN, (menu_x + 145, actions_y + 50, 125, 35), 2, border_radius=6)
    
    u_text = font_medium.render("[U] Upgrades", True, WHITE)
    h_text = font_medium.render("[H] Heal", True, WHITE)
    screen.blit(u_text, (menu_x + 20, actions_y + 55))
    screen.blit(h_text, (menu_x + 160, actions_y + 55))
    
    # Gold display
    gold_text = font_medium.render(f"Gold: {game.player.gold}", True, GOLD)
    screen.blit(gold_text, (menu_x + 20, actions_y + 100))
    
    # Actions remaining indicator
    actions_left = game.player.actions_per_turn - game.player.actions_used
    actions_box = pygame.Rect(menu_x + 10, menu_y + menu_height - 35, menu_width - 20, 25)
    pygame.draw.rect(screen, (30, 30, 45), actions_box, border_radius=4)
    
    actions_text = font_small.render(f"Actions: {actions_left}/{game.player.actions_per_turn}", True, GREEN if actions_left > 0 else RED)
    screen.blit(actions_text, (menu_x + 20, menu_y + menu_height - 30))


def draw_upgrade_shop(screen, game):
    # Dark overlay
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    # Shop panel
    shop_rect = pygame.Rect(150, 60, WIDTH - 300, HEIGHT - 120)
    pygame.draw.rect(screen, (20, 20, 40), shop_rect, border_radius=16)
    pygame.draw.rect(screen, GOLD, shop_rect, 4, border_radius=16)
    
    # Title with decorative elements
    title = font_title.render("UPGRADE SHOP", True, YELLOW)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))
    
    # Gold display
    gold_box = pygame.Rect(WIDTH//2 - 80, 130, 160, 40)
    pygame.draw.rect(screen, DARK_GRAY, gold_box, border_radius=6)
    pygame.draw.rect(screen, GOLD, gold_box, 2, border_radius=6)
    gold_text = font_medium.render(f"{game.player.gold} Gold", True, GOLD)
    screen.blit(gold_text, (WIDTH // 2 - gold_text.get_width() // 2, 140))
    
    # Upgrade cards in a grid
    upgrades = list(game.player.upgrades.items())
    cols = 3
    for i, (name, upgrade) in enumerate(upgrades):
        col = i % cols
        row = i // cols
        x = 200 + col * 300
        y = 200 + row * 130
        
        # Card background
        card = pygame.Rect(x, y, 270, 115)
        can_afford = game.player.gold >= upgrade["cost"]
        card_color = (40, 40, 60) if can_afford else (30, 30, 40)
        pygame.draw.rect(screen, card_color, card, border_radius=8)
        
        border_color = GOLD if can_afford else RED
        pygame.draw.rect(screen, border_color, card, 2, border_radius=8)
        
        # Upgrade name
        name_text = font_medium.render(name, True, YELLOW if can_afford else GRAY)
        screen.blit(name_text, (x + 15, y + 10))
        
        # Description
        desc_text = font_small.render(upgrade["description"], True, WHITE if can_afford else GRAY)
        screen.blit(desc_text, (x + 15, y + 40))
        
        # Cost
        cost_color = GREEN if can_afford else RED
        cost_text = font_medium.render(f"{upgrade['cost']}g", True, cost_color)
        screen.blit(cost_text, (x + 15, y + 70))
        
        # Key hint
        key_hint = font_small.render(f"[{i+1}]", True, (100, 100, 120))
        screen.blit(key_hint, (x + 200, y + 85))
    
    # Exit hint
    exit_box = pygame.Rect(WIDTH//2 - 120, HEIGHT - 100, 240, 40)
    pygame.draw.rect(screen, DARK_GRAY, exit_box, border_radius=6)
    pygame.draw.rect(screen, WHITE, exit_box, 1, border_radius=6)
    exit_text = font_medium.render("ESC to close", True, WHITE)
    screen.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, HEIGHT - 90))


def main():
    game = Game()
    running = True
    shop_open = False
    show_how_to_play = False
    global effects
    effects = VisualEffects()  # Reset effects
    
    while running:
        # Update visual effects every frame
        effects.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if game.game_state == "menu":
                    if event.key == pygame.K_RETURN:
                        game.start_new_game()
                    elif event.key == pygame.K_h:
                        show_how_to_play = not show_how_to_play
                
                elif game.game_state == "playing":
                    if shop_open:
                        if event.key == pygame.K_ESCAPE:
                            shop_open = False
                        elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7]:
                            idx = event.key - pygame.K_1
                            if idx < len(game.player.upgrades):
                                name = list(game.player.upgrades.keys())[idx]
                                result = game.buy_upgrade(name)
                                print(result)
                    else:
                        if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]:
                            idx = event.key - pygame.K_1
                            if idx < len(game.player.attacks):
                                name = list(game.player.attacks.keys())[idx]
                                result = game.player_attack(name)
                                print(result)
                        
                        elif event.key == pygame.K_6:
                            if len(game.player.attacks) > 5:
                                name = list(game.player.attacks.keys())[5]
                                result = game.player_attack(name)
                                print(result)
                        
                        elif event.key == pygame.K_7:
                            if len(game.player.attacks) > 6:
                                name = list(game.player.attacks.keys())[6]
                                result = game.player_attack(name)
                                print(result)
                        
                        elif event.key == pygame.K_u:
                            shop_open = True
                        
                        elif event.key == pygame.K_h:
                            result = game.heal_player()
                            print(result)
                        
                        elif event.key == pygame.K_RETURN:
                            if game.get_current_enemy():
                                game.enemy_turn()
                                game.player.reset_turn()
                
                elif game.game_state in ["victory", "defeat"]:
                    if event.key == pygame.K_RETURN:
                        game.game_state = "menu"
        
        if game.game_state == "menu":
            if show_how_to_play:
                draw_how_to_play(screen)
            else:
                draw_menu(screen, game)
        elif game.game_state == "playing":
            duck_y = draw_game(screen, game)
            draw_attack_menu(screen, game, duck_y)
            if shop_open:
                draw_upgrade_shop(screen, game)
        elif game.game_state == "victory":
            draw_gradient_background(screen)
            
            # Victory panel
            victory_box = pygame.Rect(WIDTH//2 - 250, 150, 500, 400)
            pygame.draw.rect(screen, DARK_GRAY, victory_box, border_radius=20)
            pygame.draw.rect(screen, GOLD, victory_box, 4, border_radius=20)
            
            # Victory text with glow
            for i in range(3):
                glow = font_title.render("VICTORY!", True, (*GOLD, 100 - i * 30))
                screen.blit(glow, (WIDTH // 2 - glow.get_width() // 2 + (i-1)*2, 180 + (i-1)*2))
            
            win_text = font_title.render("VICTORY!", True, GOLD)
            screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, 180))
            
            # Score display
            score_box = pygame.Rect(WIDTH//2 - 150, 280, 300, 80)
            pygame.draw.rect(screen, (30, 30, 50), score_box, border_radius=10)
            score_label = font_medium.render("Final Score", True, LIGHT_GRAY)
            screen.blit(score_label, (WIDTH // 2 - score_label.get_width() // 2, 295))
            score_text = font_large.render(f"{game.score}", True, WHITE)
            screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 325))
            
            # Roast message
            roast_box = pygame.Rect(WIDTH//2 - 200, 380, 400, 60)
            pygame.draw.rect(screen, PURPLE, roast_box, border_radius=8)
            roast_text = font_medium.render(game.roast_message, True, YELLOW)
            screen.blit(roast_text, (WIDTH // 2 - roast_text.get_width() // 2, 400))
            
            # Restart hint
            restart_box = pygame.Rect(WIDTH//2 - 150, 480, 300, 50)
            pygame.draw.rect(screen, DARK_GREEN, restart_box, border_radius=8)
            restart_text = font_medium.render("Press ENTER to play again", True, WHITE)
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, 495))
        
        elif game.game_state == "defeat":
            draw_gradient_background(screen)
            
            # Defeat panel
            defeat_box = pygame.Rect(WIDTH//2 - 250, 150, 500, 400)
            pygame.draw.rect(screen, DARK_GRAY, defeat_box, border_radius=20)
            pygame.draw.rect(screen, DARK_RED, defeat_box, 4, border_radius=20)
            
            # Defeat text
            lose_text = font_title.render("GAME OVER", True, RED)
            screen.blit(lose_text, (WIDTH // 2 - lose_text.get_width() // 2, 180))
            
            # Score display
            score_box = pygame.Rect(WIDTH//2 - 150, 280, 300, 80)
            pygame.draw.rect(screen, (40, 20, 20), score_box, border_radius=10)
            score_label = font_medium.render("Score", True, LIGHT_GRAY)
            screen.blit(score_label, (WIDTH // 2 - score_label.get_width() // 2, 295))
            score_text = font_large.render(f"{game.score}", True, WHITE)
            screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 325))
            
            # Roast message
            roast_box = pygame.Rect(WIDTH//2 - 200, 380, 400, 60)
            pygame.draw.rect(screen, (60, 30, 30), roast_box, border_radius=8)
            roast_text = font_medium.render(game.roast_message, True, YELLOW)
            screen.blit(roast_text, (WIDTH // 2 - roast_text.get_width() // 2, 400))
            
            # Restart hint
            restart_box = pygame.Rect(WIDTH//2 - 150, 480, 300, 50)
            pygame.draw.rect(screen, DARK_GREEN, restart_box, border_radius=8)
            restart_text = font_medium.render("Press ENTER to try again", True, WHITE)
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, 495))
        
        pygame.display.flip()
        clock.tick(30)
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
