import pygame
import random
import sys

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rubber Duck Debugging: The Roast Edition")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 223, 0)
RED = (220, 50, 50)
GREEN = (50, 200, 50)
BLUE = (50, 100, 200)
PURPLE = (150, 50, 200)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
GOLD = (255, 215, 0)

try:
    font_emoji = pygame.font.Font("/System/Library/Fonts/Apple Color Emoji.ttc", 48)
except:
    font_emoji = pygame.font.Font(None, 48)

font_title = pygame.font.Font(None, 64)
font_large = pygame.font.Font(None, 48)
font_medium = pygame.font.Font(None, 32)
font_small = pygame.font.Font(None, 24)

EMOJI_MAP = {
    "🦆": "DUCK",
    "❌": "X",
    "🔗": "LINK",
    "🔄": "LOOP",
    "💧": "LEAK",
    "🏃": "RACE",
    "👹": "BOSS",
    "⚔️": "ATK",
    "🛡️": "DEF",
    "🎉": "WIN",
    "💀": "DEAD",
    "💰": "$",
    "⭐": "*",
    "🔥": "ROAST",
    "❤️": "HP",
}

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
                f"The {attacker} is judging you. And honestly, I'm同情.",
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
        super().__init__("🦆 Rubber Duck", 100, 100, 20, 5, "🦆")
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
        "Syntax Error": {"hp": 30, "attack": 8, "defense": 2, "emoji": "❌", "xp": 10, "gold": 5},
        "Null Pointer": {"hp": 25, "attack": 12, "defense": 0, "emoji": "🔗", "xp": 12, "gold": 8},
        "Infinite Loop": {"hp": 50, "attack": 5, "defense": 5, "emoji": "🔄", "xp": 20, "gold": 15},
        "Memory Leak": {"hp": 35, "attack": 10, "defense": 3, "emoji": "💧", "xp": 15, "gold": 10},
        "Race Condition": {"hp": 40, "attack": 15, "defense": 2, "emoji": "🏃", "xp": 18, "gold": 12},
        "Legacy Code Boss": {"hp": 200, "attack": 25, "defense": 10, "emoji": "👹", "xp": 100, "gold": 100},
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
        if not self.player.can_act():
            return "No actions left!"
        
        enemy = self.get_current_enemy()
        if not enemy:
            return "No enemy to attack!"
        
        self.player.actions_used += 1
        
        if attack_name == "Float Above":
            self.player.dodging = True
            self.roast_message = self.roast_engine.get_roast("attack", {"attack": attack_name, "enemy_hp": enemy.hp})
            return f"[DEF] You float above! Next attack will be dodged!"
        
        damage, crit = self.player.attack_target(attack_name, enemy)
        
        if damage == 0:
            self.roast_message = self.roast_engine.get_roast("mistake", {"mistake": "missed attack"})
            return f"[MISS] You missed with {attack_name}!"
        
        self.roast_message = self.roast_engine.get_roast("attack", {"attack": attack_name, "enemy_hp": enemy.hp})
        
        result = f"[ATK] You used {attack_name}! "
        if crit:
            result += f"CRITICAL HIT! "
        result += f"Dealt {damage} damage!"
        
        self.score += damage
        
        if not enemy.is_alive():
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
        enemy = self.get_current_enemy()
        if not enemy:
            return
        
        damage, dodged = enemy.enemy_attack(self.player)
        
        if dodged:
            self.roast_message = "You dodged the attack! Even the roast engine is surprised."
        else:
            self.roast_message = self.roast_engine.get_roast("damage_taken", {"damage": damage, "attacker": enemy.name})
        
        self.score += damage // 2
        
        if not self.player.is_alive():
            self.game_state = "defeat"
            self.roast_message = self.roast_engine.get_roast("defeat", {})
            if self.score > self.high_score:
                self.high_score = self.score
    
    def buy_upgrade(self, upgrade_name):
        if upgrade_name not in self.player.upgrades:
            return "Upgrade not found!"
        
        upgrade = self.player.upgrades[upgrade_name]
        if self.player.gold < upgrade["cost"]:
            return "Not enough gold!"
        
        self.player.gold -= upgrade["cost"]
        
        if upgrade_name == "Sonic Quack":
            self.player.attacks["Sonic Quack"] = {"damage": upgrade["damage"], "accuracy": upgrade["accuracy"], "description": upgrade["description"]}
        else:
            self.player.active_upgrades.append(upgrade)
            if upgrade["effect"] == "max_hp":
                self.player.max_hp += upgrade["value"]
                self.player.hp += upgrade["value"]
            elif upgrade["effect"] == "crit":
                self.player.crit_chance += upgrade["value"]
            elif upgrade["effect"] == "xp_boost":
                self.player.xp_multiplier += upgrade["value"] / 100
        
        self.roast_message = self.roast_engine.get_roast("upgrade", {"upgrade": upgrade_name})
        return f"[BOUGHT] {upgrade_name}!"
    
    def heal_player(self):
        if self.player.gold >= 30:
            self.player.gold -= 30
            self.player.heal(40)
            return "✅ Healed for 40 HP!"
        return "Not enough gold! (Need 30)"
    
    def start_new_game(self):
        self.player = Player()
        self.floor = 1
        self.score = 0
        self.roast_engine.new_game()
        self.generate_floor()
        self.game_state = "playing"
        self.roast_message = self.roast_engine.get_roast("turn_start")


def draw_text(surface, text, x, y, font, color=WHITE, max_width=None):
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
            surface.blit(text_surface, (x, y + i * font.get_height()))
    else:
        text_surface = font.render(text, True, color)
        surface.blit(text_surface, (x, y))


def draw_health_bar(surface, x, y, hp, max_hp, width=200, height=20):
    pygame.draw.rect(surface, DARK_GRAY, (x, y, width, height))
    fill_width = int((hp / max_hp) * width) if max_hp > 0 else 0
    pygame.draw.rect(surface, RED, (x, y, fill_width, height))
    pygame.draw.rect(surface, WHITE, (x, y, width, height), 2)
    
    text = font_small.render(f"{hp}/{max_hp}", True, WHITE)
    surface.blit(text, (x + width // 2 - text.get_width() // 2, y + 2))


def draw_game(screen, game):
    screen.fill(BLACK)
    
    pygame.draw.rect(screen, DARK_GRAY, (20, 20, WIDTH - 40, HEIGHT - 40), 3)
    
    title = font_title.render("RUBBER DUCK DEBUGGING: THE ROAST EDITION", True, YELLOW)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 30))
    
    floor_text = font_large.render(f"Floor {game.floor}", True, GOLD)
    screen.blit(floor_text, (WIDTH // 2 - floor_text.get_width() // 2, 90))
    
    enemy = game.get_current_enemy()
    if enemy:
        enemy_x = WIDTH // 2
        enemy_y = 200
        
        emoji_size = 80
        enemy_text = font_large.render(EMOJI_MAP.get(enemy.emoji, enemy.emoji), True, WHITE)
        screen.blit(enemy_text, (enemy_x - enemy_text.get_width() // 2, enemy_y - 40))
        
        enemy_name = font_medium.render(enemy.name, True, WHITE)
        screen.blit(enemy_name, (enemy_x - enemy_name.get_width() // 2, enemy_y + 50))
        
        draw_health_bar(screen, enemy_x - 100, enemy_y + 90, enemy.hp, enemy.max_hp, 200)
    
    pygame.draw.line(screen, GRAY, (50, 180), (WIDTH - 50, 180), 2)
    
    duck_x = WIDTH // 2
    duck_y = 450
    
    duck_text = font_title.render("DUCK", True, YELLOW)
    screen.blit(duck_text, (duck_x - duck_text.get_width() // 2, duck_y - 30))
    
    player_name = font_medium.render(game.player.name, True, WHITE)
    screen.blit(player_name, (duck_x - player_name.get_width() // 2, duck_y + 40))
    
    draw_health_bar(screen, duck_x - 100, duck_y + 75, game.player.hp, game.player.max_hp, 200)
    
    actions_text = font_small.render(f"Actions: {game.player.actions_per_turn - game.player.actions_used}/{game.player.actions_per_turn}", True, WHITE)
    screen.blit(actions_text, (duck_x - actions_text.get_width() // 2, duck_y + 105))
    
    pygame.draw.line(screen, GRAY, (50, 600), (WIDTH - 50, 600), 2)
    
    roast_bg = pygame.Rect(50, 610, WIDTH - 100, 80)
    pygame.draw.rect(screen, PURPLE, roast_bg)
    pygame.draw.rect(screen, GOLD, roast_bg, 3)
    
    roast_label = font_small.render("THE ROAST:", True, GOLD)
    screen.blit(roast_label, (60, 615))
    
    draw_text(screen, game.roast_message, 60, 640, font_small, WHITE, WIDTH - 140)
    
    stats_x = 50
    stats_y = 710
    
    stats_text = f"Gold: {game.player.gold}  |  XP: {int(game.player.xp)}  |  Score: {game.score}  |  High Score: {game.high_score}"
    draw_text(screen, stats_text, stats_x, stats_y, font_small, GOLD)
    
    return duck_y


def draw_menu(screen):
    screen.fill(BLACK)
    
    title = font_title.render("RUBBER DUCK DEBUGGING", True, YELLOW)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 150))
    
    subtitle = font_large.render("THE ROAST EDITION", True, GOLD)
    screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, 220))
    
    duck = font_title.render("DUCK " * 5, True, YELLOW)
    screen.blit(duck, (WIDTH // 2 - duck.get_width() // 2, 300))
    
    start_text = font_medium.render("Press ENTER to Start", True, GREEN)
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, 450))
    
    high_text = font_medium.render(f"High Score: 0", True, GOLD)
    screen.blit(high_text, (WIDTH // 2 - high_text.get_width() // 2, 520))
    
    instructions = [
        "🎮 CONTROLS:",
        "1-5: Select attack",
        "U: Open upgrade shop",
        "H: Heal (30 gold)",
        "ENTER: End turn",
        "",
        "🎯 Goal: Defeat the Legacy Code Boss on Floor 5!"
    ]
    
    for i, line in enumerate(instructions):
        text = font_small.render(line, True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 580 + i * 30))


def draw_attack_menu(screen, game, duck_y):
    menu_x = WIDTH - 250
    menu_y = duck_y + 130
    
    pygame.draw.rect(screen, DARK_GRAY, (menu_x, menu_y, 230, 250))
    pygame.draw.rect(screen, WHITE, (menu_x, menu_y, 230, 250), 2)
    
    title = font_small.render("ATTACKS:", True, YELLOW)
    screen.blit(title, (menu_x + 10, menu_y + 10))
    
    for i, (name, attack) in enumerate(game.player.attacks.items()):
        key = str(i + 1)
        color = WHITE if game.player.can_act() else GRAY
        text = f"{key}: {name} ({attack['damage']}dmg, {attack['accuracy']}%acc)"
        draw_text(screen, text, menu_x + 10, menu_y + 35 + i * 30, font_small, color, 210)
    
    y_extra = menu_y + 35 + len(game.player.attacks) * 30 + 10
    screen.blit(font_small.render("U: Upgrade Shop", True, GOLD if game.player.gold >= 30 else GRAY), (menu_x + 10, y_extra))
    screen.blit(font_small.render("H: Heal (30g)", True, GREEN if game.player.gold >= 30 else GRAY), (menu_x + 10, y_extra + 25))
    screen.blit(font_small.render("ENTER: End Turn", True, BLUE), (menu_x + 10, y_extra + 50))


def draw_upgrade_shop(screen, game):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    shop_rect = pygame.Rect(200, 100, WIDTH - 400, HEIGHT - 200)
    pygame.draw.rect(screen, DARK_GRAY, shop_rect)
    pygame.draw.rect(screen, GOLD, shop_rect, 4)
    
    title = font_large.render("🛒 UPGRADE SHOP", True, YELLOW)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 120))
    
    gold_text = font_medium.render(f"Your Gold: {game.player.gold}", True, GOLD)
    screen.blit(gold_text, (WIDTH // 2 - gold_text.get_width() // 2, 170))
    
    for i, (name, upgrade) in enumerate(game.player.upgrades.items()):
        x = 250 + (i % 3) * 280
        y = 230 + (i // 3) * 120
        
        card = pygame.Rect(x, y, 250, 100)
        pygame.draw.rect(screen, PURPLE, card)
        pygame.draw.rect(screen, WHITE, card, 2)
        
        name_text = font_small.render(name, True, YELLOW)
        screen.blit(name_text, (x + 10, y + 10))
        
        desc = font_small.render(upgrade["description"], True, WHITE)
        screen.blit(desc, (x + 10, y + 35))
        
        cost_color = GOLD if game.player.gold >= upgrade["cost"] else RED
        cost_text = font_small.render(f"Cost: {upgrade['cost']}g", True, cost_color)
        screen.blit(cost_text, (x + 10, y + 60))
        
        key_text = font_small.render(f"[{i + 1}]", True, WHITE)
        screen.blit(key_text, (x + 180, y + 75))
    
    exit_text = font_medium.render("Press ESC to close", True, WHITE)
    screen.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, HEIGHT - 130))


def main():
    game = Game()
    running = True
    shop_open = False
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if game.game_state == "menu":
                    if event.key == pygame.K_RETURN:
                        game.start_new_game()
                
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
            draw_menu(screen)
        elif game.game_state == "playing":
            duck_y = draw_game(screen, game)
            draw_attack_menu(screen, game, duck_y)
            if shop_open:
                draw_upgrade_shop(screen, game)
        elif game.game_state == "victory":
            screen.fill(BLACK)
            win_text = font_title.render("VICTORY!", True, GOLD)
            screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, 200))
            
            score_text = font_large.render(f"Final Score: {game.score}", True, WHITE)
            screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 350))
            
            roast_text = font_medium.render(game.roast_message, True, YELLOW)
            screen.blit(roast_text, (WIDTH // 2 - roast_text.get_width() // 2, 450))
            
            restart_text = font_medium.render("Press ENTER to play again", True, GREEN)
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, 550))
        
        elif game.game_state == "defeat":
            screen.fill(BLACK)
            lose_text = font_title.render("GAME OVER", True, RED)
            screen.blit(lose_text, (WIDTH // 2 - lose_text.get_width() // 2, 200))
            
            score_text = font_large.render(f"Score: {game.score}", True, WHITE)
            screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 350))
            
            roast_text = font_medium.render(game.roast_message, True, YELLOW)
            screen.blit(roast_text, (WIDTH // 2 - roast_text.get_width() // 2, 450))
            
            restart_text = font_medium.render("Press ENTER to try again", True, GREEN)
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, 550))
        
        pygame.display.flip()
        clock.tick(30)
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
