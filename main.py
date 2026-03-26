import pygame
import random
import sys
import math

pygame.init()

# ============================================
# ZONE DEFINITIONS
# ============================================
ZONES = {
    1: {"name": "Night City Slums", "levels": [1, 2, 3], "minions": ["Glitch", "Lag", "Error", "Bug"], "general": "Virus"},
    2: {"name": "Industrial District", "levels": [4, 5, 6], "minions": ["Crasher", "Freezer", "Trojan", "Malware"], "general": "Lagomorph"},
    3: {"name": "Corporate Tower", "levels": [7, 8, 9], "minions": ["The Firewall", "Hacker", "Netrunner"], "general": None, "boss": "The System"},
    4: {"name": "The Sprawl", "levels": [10, 11, 12], "minions": ["Chrome Commando", "A.I. Security"], "general": None, "boss": "The Architect"},
    5: {"name": "Cyber Hell", "levels": [13, 14, 15], "minions": ["Rogue A.I.", "Cybernetic Demon"], "general": None, "boss": "MEGACORP CEO"},
}

# ============================================
# SHOP ITEMS DEFINITION
# ============================================
SHOP_ITEMS = {
    # Consumables (stackable, can be bought multiple times)
    "Med Kit": {"price": 50, "effect": "heal", "value": 30, "type": "consumable", "description": "Heal 30 HP"},
    "Super Med Kit": {"price": 100, "effect": "heal", "value": 60, "type": "consumable", "description": "Heal 60 HP"},
    
    # Permanent upgrades (one-time purchase only)
    "Damage Amp": {"price": 200, "effect": "attack", "value": 5, "type": "permanent", "description": "+5 Attack (permanent)"},
    "Shield Generator": {"price": 200, "effect": "defense", "value": 5, "type": "permanent", "description": "+5 Defense (permanent)"},
    "Speed Chip": {"price": 150, "effect": "speed", "value": 2, "type": "permanent", "description": "+2 Speed (permanent)"},
    "Crit Lens": {"price": 250, "effect": "crit", "value": 3, "type": "permanent", "description": "+3% Crit (permanent)"},
    
    # Special - Overcharge Chip (stackable, expires after 10 turns)
    "Overcharge Chip": {"price": 150, "effect": "charge_chance", "value": 10, "max_stacks": 5, "type": "stackable", "expires": True, "expires_turns": 10, "description": "+10% chance for +2 charge (max 50%)"},
}


def get_shop_items_by_category():
    """Return items organized by category."""
    consumables = {k: v for k, v in SHOP_ITEMS.items() if v.get("type") == "consumable"}
    permanent = {k: v for k, v in SHOP_ITEMS.items() if v.get("type") == "permanent"}
    stackable = {k: v for k, v in SHOP_ITEMS.items() if v.get("type") == "stackable"}
    return consumables, permanent, stackable
ENEMY_STATS = {
    # Zone 1: Night City Slums (Levels 1-3)
    "Glitch": {"level": 1, "hp": 30, "attack": 8, "defense": 3, "charge_attack": 1, "xp": 15, "gold": 10, "emoji": "GLITCH"},
    "Lag": {"level": 2, "hp": 50, "attack": 12, "defense": 6, "charge_attack": 1, "xp": 30, "gold": 25, "emoji": "LAG"},
    "Error": {"level": 2, "hp": 40, "attack": 15, "defense": 4, "charge_attack": 1, "xp": 35, "gold": 20, "emoji": "ERROR"},
    "Bug": {"level": 3, "hp": 70, "attack": 18, "defense": 8, "charge_attack": 1, "xp": 50, "gold": 40, "emoji": "BUG"},
    "Virus": {"level": 3, "hp": 100, "attack": 22, "defense": 12, "charge_attack": 2, "xp": 80, "gold": 75, "emoji": "VIRUS"},
    
    # Zone 2: Industrial District (Levels 4-6)
    "Crasher": {"level": 4, "hp": 80, "attack": 20, "defense": 12, "charge_attack": 2, "xp": 70, "gold": 50, "emoji": "CRASH"},
    "Freezer": {"level": 4, "hp": 60, "attack": 25, "defense": 15, "charge_attack": 2, "xp": 60, "gold": 45, "emoji": "FREEZE"},
    "Trojan": {"level": 5, "hp": 110, "attack": 28, "defense": 18, "charge_attack": 2, "xp": 100, "gold": 80, "emoji": "TROJAN"},
    "Malware": {"level": 5, "hp": 90, "attack": 30, "defense": 20, "charge_attack": 2, "xp": 90, "gold": 70, "emoji": "MALWARE"},
    "Lagomorph": {"level": 6, "hp": 150, "attack": 35, "defense": 22, "charge_attack": 2, "xp": 140, "gold": 120, "emoji": "LAGO"},
    
    # Zone 3: Corporate Tower (Levels 7-9)
    "The Firewall": {"level": 7, "hp": 130, "attack": 32, "defense": 25, "charge_attack": 3, "xp": 130, "gold": 100, "emoji": "FIREWALL"},
    "Hacker": {"level": 7, "hp": 100, "attack": 38, "defense": 20, "charge_attack": 3, "xp": 120, "gold": 95, "emoji": "HACKER"},
    "Netrunner": {"level": 8, "hp": 150, "attack": 40, "defense": 28, "charge_attack": 3, "xp": 160, "gold": 130, "emoji": "NETRUN"},
    "The System": {"level": 9, "hp": 220, "attack": 48, "defense": 35, "charge_attack": 3, "xp": 220, "gold": 200, "emoji": "SYSTEM"},
    
    # Zone 4: The Sprawl (Levels 10-12)
    "Chrome Commando": {"level": 10, "hp": 200, "attack": 50, "defense": 38, "charge_attack": 3, "xp": 230, "gold": 200, "emoji": "COMMANDO"},
    "A.I. Security": {"level": 11, "hp": 250, "attack": 52, "defense": 45, "charge_attack": 3, "xp": 300, "gold": 280, "emoji": "AI_SEC"},
    "The Architect": {"level": 12, "hp": 350, "attack": 65, "defense": 50, "charge_attack": 3, "xp": 400, "gold": 400, "emoji": "ARCH"},
    
    # Zone 5: Cyber Hell (Levels 13-15)
    "Rogue A.I.": {"level": 13, "hp": 300, "attack": 60, "defense": 48, "charge_attack": 3, "xp": 450, "gold": 350, "emoji": "ROGUE_AI"},
    "Cybernetic Demon": {"level": 13, "hp": 380, "attack": 70, "defense": 52, "charge_attack": 3, "xp": 500, "gold": 400, "emoji": "DEMON"},
    "MEGACORP CEO": {"level": 15, "hp": 600, "attack": 90, "defense": 65, "charge_attack": 3, "xp": 800, "gold": 750, "emoji": "CEO"},
}


def get_zone_for_level(level):
    """Get zone number for a given level."""
    for zone_num, zone_data in ZONES.items():
        if level in zone_data["levels"]:
            return zone_num
    return 5  # Default to max zone


def spawn_enemy_for_zone(zone_num, enemy_list=None):
    """Spawn a random enemy appropriate for the zone."""
    if zone_num not in ZONES:
        zone_num = 1
    
    zone_data = ZONES[zone_num]
    minions = zone_data.get("minions", [])
    
    if not minions:
        # Fallback to zone 1 enemies
        minions = ZONES[1]["minions"]
    
    if enemy_list is not None and enemy_list:
        # Spawn from remaining enemies in the list
        enemy_name = enemy_list.pop(0)
        return Enemy(enemy_name)
    
    # Random minion from zone
    enemy_name = random.choice(minions)
    return Enemy(enemy_name)


# ============================================
# COMBAT ACTIONS DEFINITION
# ============================================
ACTIONS = {
    "charge": {"key": 1, "cost": 0, "name": "CHARGE"},
    "dodge": {"key": 2, "cost": 0, "name": "DODGE"},
    "block": {"key": 3, "cost": 0, "name": "BLOCK"},
    "shoot": {"key": 4, "cost": 1, "name": "SHOOT"},
    "special": {"key": 5, "cost": 2, "name": "SPECIAL"},
}

# Action success rates
ACTION_RATES = {
    "dodge": 85,      # 85% against charge=1
    "block_charge1": 70,  # 70% against charge=1
    "block_charge2plus": 60,  # 60% against charge=2-3
    "shoot": 85,      # 85% hit rate
    "special": 70,    # 70% hit rate
}

WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CYBERPUNK RPG - Neo-Tokyo 2087")
clock = pygame.time.Clock()

# Enhanced Cyberpunk color scheme
WHITE = (255, 255, 255)
BLACK = (13, 13, 26)
YELLOW = (255, 223, 0)
GOLD = (255, 215, 0)
RED = (255, 49, 49)
DARK_RED = (180, 30, 30)
GREEN = (57, 255, 20)  # Neon green
DARK_GREEN = (30, 100, 50)
BLUE = (60, 130, 255)
CYAN = (0, 255, 255)  # Bright cyan
MAGENTA = (255, 0, 255)  # Magenta
PURPLE = (191, 0, 255)
PINK = (255, 100, 150)
ORANGE = (255, 150, 50)
NEON_CYAN = (0, 255, 255)
NEON_MAGENTA = (255, 0, 255)
NEON_GREEN = (57, 255, 20)

GRAY = (100, 100, 120)
DARK_GRAY = (40, 40, 55)
LIGHT_GRAY = (150, 150, 170)

# Background gradient colors - cyberpunk dark
BG_TOP = (13, 13, 26)  # #0D0D0D
BG_BOTTOM = (26, 26, 46)  # #1A1A2E

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
            alpha = self.screen_flash.get("alpha", 150)
            if alpha <= 0:
                self.screen_flash = None
                return
            if isinstance(color, (list, tuple)) and len(color) >= 3:
                r = max(0, min(255, int(color[0])))
                g = max(0, min(255, int(color[1])))
                b = max(0, min(255, int(color[2])))
                a = max(0, min(255, int(alpha)))
                flash_color = (r, g, b, a)
                flash = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                flash.fill(flash_color)
                surface.blit(flash, (0, 0))
    
    def get_shake_offset(self):
        return self.shake_offset


effects = VisualEffects()


# ============================================
# PLAYER STATS CLASS
# ============================================
class PlayerStats:
    def __init__(self):
        self.level = 1
        self.xp = 0
        self.xp_to_next = 100  # For level 2
        self.hp = 100
        self.max_hp = 100
        self.attack = 15
        self.defense = 10
        self.speed = 10
        self.crit = 5  # 5% crit chance
        self.gold = 0
        self.charge = 0
        self.max_charge = 10
        
        # Shop-related inventory
        self.inventory = {
            "Med Kit": 0,
            "Super Med Kit": 0,
        }
        self.purchased = []  # Track permanent upgrades already purchased
        self.overcharge_stacks = 0
        self.overcharge_turns = 0  # Turns until overcharge expires
    
    def take_damage(self, damage):
        """Apply damage to player, factoring in defense."""
        actual_damage = max(1, damage - self.defense)
        self.hp = max(0, self.hp - actual_damage)
        return actual_damage
    
    def get_overcharge_chance(self):
        """Calculate current overcharge chance (max 50%)."""
        return min(50, self.overcharge_stacks)
    
    def update_overcharge(self):
        """Decrement overcharge turns counter."""
        if self.overcharge_turns > 0:
            self.overcharge_turns -= 1
            if self.overcharge_turns == 0:
                self.overcharge_stacks = 0
    
    def apply_item_effect(self, item_name):
        """Apply item effect based on type."""
        global effects
        
        if item_name not in SHOP_ITEMS:
            return "Item not found!"
        
        item = SHOP_ITEMS[item_name]
        
        # Check consumable stack
        if item.get("type") == "consumable":
            if self.inventory.get(item_name, 0) <= 0:
                return "No more of this item!"
            
            # Use the item
            self.inventory[item_name] -= 1
            
            if item["effect"] == "heal":
                old_hp = self.hp
                self.hp = min(self.max_hp, self.hp + item["value"])
                healed = self.hp - old_hp
                
                # Visual effects
                effects.add_screen_flash(GREEN, 12)
                for _ in range(12):
                    effects.add_particle(
                        WIDTH//2 - 150, 300,
                        GREEN,
                        random.randint(4, 8),
                        (random.uniform(-3, 3), random.uniform(-4, -2)),
                        30
                    )
                effects.add_floating_text(WIDTH//2 - 150, 260, f"+{healed} HP", GREEN, 35)
                return f"Used {item_name}! Healed {healed} HP."
        
        return "Cannot use this item!"
    
    def level_up(self):
        """Returns True if player leveled up"""
        if self.xp >= self.xp_to_next:
            self.level += 1
            self.xp -= self.xp_to_next
            
            # XP formula: level * 100 + (level-1) * 50 for next level
            self.xp_to_next = self.level * 100 + (self.level - 1) * 50
            
            # Stat growth
            self.max_hp += 12
            self.hp = self.max_hp  # Full heal on level up
            self.attack += 3
            self.defense += 2
            self.speed += 1
            self.crit += 0.5
            
            return True
        return False
    
    def add_xp(self, amount):
        """Add XP and check for level up. Returns True if player leveled up."""
        self.xp += amount
        leveled_up = False
        while self.level_up():
            leveled_up = True  # Handle multiple level ups
        return leveled_up
    
    def reset_charge(self):
        """Reset charge at start of combat"""
        self.charge = 0
    
    def add_charge(self, amount=1):
        """Add charge, capped at max_charge. Includes overcharge logic."""
        overcharge_chance = self.get_overcharge_chance()
        
        # Check for overcharge bonus
        actual_amount = amount
        if overcharge_chance > 0 and random.random() * 100 < overcharge_chance:
            actual_amount = 2  # Get +2 instead of +1
            global effects
            effects.add_floating_text(WIDTH//2 - 150, 250, "OVERCHARGE! +2", GOLD, 30)
            effects.add_screen_flash(GOLD, 10)
        
        self.charge = min(self.max_charge, self.charge + actual_amount)
        
        return actual_amount  # Return actual amount gained (for display)


# ============================================
# COMBAT MANAGER FOR CHARGE-BASED COMBAT
# ============================================
class CombatManager:
    def __init__(self):
        self.last_player_action = None
        self.last_enemy_action = None
        self.combat_log = []
    
    def resolve_player_action(self, player, enemy, action_name):
        """
        Resolve player's action based on the charge-based combat system.
        
        Flow:
        1. Player picks action
        2. Charge +1 at turn start (handled elsewhere)
        3. Resolve action based on type
        """
        self.last_player_action = action_name
        result = {
            "action": action_name,
            "success": False,
            "damage": 0,
            "message": "",
            "effects": []
        }
        
        # Check if action requires charge
        action_cost = ACTIONS[action_name]["cost"]
        if player.charge < action_cost:
            result["message"] = f"Not enough charge! Need {action_cost}, have {player.charge}"
            return result
        
        if action_name == "charge":
            # Just add charge, no other effect
            player.add_charge(1)
            result["success"] = True
            result["message"] = "Charged up! +1 Charge"
            return result
        
        elif action_name == "dodge":
            # Dodge blocks Shoot only - 85% against charge=1, auto-fail against charge>1
            if enemy.charge <= 1:
                if random.random() < 0.85:  # 85%
                    result["success"] = True
                    result["message"] = "Dodged the attack!"
                    result["effects"].append("dodged")
                else:
                    result["message"] = "Dodge failed!"
            else:
                result["message"] = "Dodge failed! Enemy charge too high!"
            return result
        
        elif action_name == "block":
            # Block blocks Shoot/Special - 70%/60%
            if enemy.charge <= 1:
                if random.random() < 0.70:  # 70%
                    result["success"] = True
                    result["message"] = "Blocked the attack!"
                    result["effects"].append("blocked")
                else:
                    result["message"] = "Block failed!"
            else:  # charge >= 2
                if random.random() < 0.60:  # 60%
                    result["success"] = True
                    result["message"] = "Blocked the attack!"
                    result["effects"].append("blocked")
                else:
                    result["message"] = "Block failed!"
            return result
        
        elif action_name == "shoot":
            # Uses 1 charge, 85% hit, deals damage
            player.charge -= action_cost
            if random.random() < 0.85:  # 85% hit rate
                # Calculate damage
                is_crit = random.random() * 100 < player.crit
                base_damage = player.attack
                if is_crit:
                    base_damage *= 2
                
                damage = enemy.take_damage(base_damage)
                result["success"] = True
                result["damage"] = damage
                if is_crit:
                    result["message"] = f"CRITICAL! Dealt {damage} damage!"
                    result["effects"].append("crit")
                else:
                    result["message"] = f"Shot hit for {damage} damage!"
            else:
                result["message"] = "Shot missed!"
            return result
        
        elif action_name == "special":
            # Uses 2 charges, 70% hit, deals 2x damage
            player.charge -= action_cost
            if random.random() < 0.70:  # 70% hit rate
                # Calculate damage (2x)
                is_crit = random.random() * 100 < player.crit
                base_damage = player.attack * 2
                if is_crit:
                    base_damage *= 2
                
                damage = enemy.take_damage(base_damage)
                result["success"] = True
                result["damage"] = damage
                if is_crit:
                    result["message"] = f"MASSIVE CRITICAL! Dealt {damage} damage!"
                    result["effects"].append("crit")
                else:
                    result["message"] = f"Special attack hit for {damage} damage!"
            else:
                result["message"] = "Special attack missed!"
            return result
        
        return result
    
    def resolve_enemy_turn(self, player, enemy):
        """
        Resolve enemy's attack based on their charge level.
        """
        enemy.add_charge()
        
        result = {
            "action": "attack",
            "damage": 0,
            "blocked": False,
            "dodged": False,
            "message": ""
        }
        
        # Enemy attack based on charge level
        # If enemy charge >= 2, they do charge attack
        if enemy.charge >= 2:
            # Charge attack - more damage
            base_damage = enemy.attack * 1.5
            damage = player.take_damage(int(base_damage))
            result["damage"] = damage
            result["message"] = f"Enemy used CHARGE ATTACK! Dealt {damage} damage!"
        else:
            # Normal attack
            damage = player.take_damage(enemy.attack)
            result["damage"] = damage
            result["message"] = f"Enemy attacked for {damage} damage!"
        
        self.last_enemy_action = result
        return result


# ============================================
# ENEMY CLASS FOR CHARGE-BASED COMBAT
# ============================================
class Enemy:
    def __init__(self, enemy_type=None, level=1):
        if enemy_type is None:
            # Fallback: pick from Zone 1 enemies
            enemy_type = random.choice(ZONES[1]["minions"])
        
        if enemy_type not in ENEMY_STATS:
            enemy_type = random.choice(list(ENEMY_STATS.keys()))
        
        stats = ENEMY_STATS[enemy_type]
        self.name = enemy_type
        self.level = stats["level"]
        self.hp = stats["hp"]
        self.max_hp = stats["hp"]
        self.attack = stats["attack"]
        self.defense = stats["defense"]
        self.emoji = stats["emoji"]
        self.xp_reward = stats["xp"]
        self.gold_reward = stats["gold"]
        self.charge = 0  # Enemy charge for attacks
        self.charge_attack = stats["charge_attack"]  # Charge attack threshold
    
    def is_alive(self):
        return self.hp > 0
    
    def take_damage(self, damage):
        actual_damage = max(1, damage - self.defense)
        self.hp = max(0, self.hp - actual_damage)
        return actual_damage
    
    def reset_charge(self):
        """Reset charge at start of combat"""
        self.charge = 0
    
    def add_charge(self):
        """Add charge each turn"""
        self.charge += 1


# ASCII art and sprite definitions
CYBER_RUNNER_SPRITE = r"""
   .---.
  /     \
  |o_o  |
  |:_/  |
 //   \ \
(|     | )
/  \_  /  \
\  | |   /
 )_)_(_(
"""

# Cyberpunk player avatar for menus
CYBER_AVATAR = r"""
  [=======]
  |CYBER|
  |======|
  | (o_o) |
  |  \_/  |
  [=======]
"""

ENEMY_SPRITES = {
    # Zone 1 Enemies
    "Glitch": """
   [!!!]
  |GLITCH|
  |_____|""",
    "Lag": """
   _____
  | LAG |
  |~~~~~|
  |_____|""",
    "Error": """
   [ERR]
  |ERROR |
  |_____|""",
    "Bug": """
   /-o-\\
  | BUG |
  \\___/""",
    "Virus": """
   \\v/
  |VIRUS|
  /___\\""",
    
    # Zone 2 Enemies
    "Crasher": """
  /===\\
  |CRASH|
  \\___/""",
    "Freezer": """
  |***|
  |FROZEN|
  |***|""",
    "Trojan": """
   (T)
  |TROJAN|
  |______|""",
    "Malware": """
  |XXXXX|
  |MALWR |
  |XXXXX|""",
    "Lagomorph": """
   \\o/
  |LAGO|
  /___\\""",
    
    # Zone 3 Enemies
    "The Firewall": """
  |####|
  |FIRE |
  |WALL |
  |####|""",
    "Hacker": """
   /***\\
  |HACK |
  |_____|
   \\_/""",
    "Netrunner": """
  |@@@|
  |NET |
  |RUN |
  |@@@|""",
    "The System": """
  ___________
 |   SYSTEM   |
 |  (O_O_O)  |
 |___________|""",
    
    # Zone 4 Enemies
    "Chrome Commando": """
  /[=]\\
  |CMDO|
  |####|
  \\___/""",
    "A.I. Security": """
  |[AI]|
  |SEC |
  |URITY|
  |____|""",
    "The Architect": """
  _____________
 |  ARCHITECT |
 |   (O_O)   |
 |___________|""",
    
    # Zone 5 Enemies
    "Rogue A.I.": """
  |#####|
  |ROGUE|
  | AI  |
  |_____|""",
    "Cybernetic Demon": """
  \\(o_o)/
  |DEMON|
  |~~~~~|
  /_____\\""",
    "MEGACORP CEO": """
  $$$$$$$$$$
 |  MEGACORP |
 |    CEO    |
 |  (O_O)   |
 |___________|""",
    
    # Legacy fallback
    "Legacy Code Boss": """
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
        elif event_type == "level_up":
            return self._roast_level_up(context)
        else:
            return "You stand there in confusion. Even the enemy is confused."
    
    def _roast_attack(self, context):
        attack_name = context.get("attack", "attack")
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
                "That's one small step for runner, one giant leap for your leaderboard.",
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
                "Your runner has been pwned. N00b."
            ],
            "existential": [
                "You are dead. But then, you were always dead inside.",
                "Game over. The void welcomes you home.",
                "Your runner is gone. The code persists. Nothing matters.",
                "Death is just a bug in the simulation. You're the feature.",
                "You failed. And yet, you still tried. How noble. How futile."
            ],
            "corporate": [
                "Let's schedule a post-mortem on your performance.",
                "Your runner has been let go. Sorry, it's just business.",
                "That's a termination-worthy performance. Runner.",
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
                "The runner awaits your command. Foolish mortal."
            ],
            "existential": [
                "Time passes. Bugs persist. You endure, inexplicably.",
                "Another turn in the eternal battle against code.",
                "The runner fires. The void listens."
            ],
            "corporate": [
                "Sprint {turn} begins. What's the velocity? Low, presumably.".format(turn=self.turn_count),
                "New turn, same runner. Let's make this one count.",
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
    
    def _roast_level_up(self, context):
        new_level = context.get("new_level", 1)
        
        roasts = {
            "socratic": [
                f"You leveled up! Even the bugs are impressed.",
                f"Level {new_level}? Don't let it go to your head.",
                "Congratulations on leveling up. Now try not to die immediately.",
                f"Level {new_level} achieved. The void remains unimpressed."
            ],
            "existential": [
                "You've grown stronger. And yet, the bugs persist.",
                f"Level {new_level}. Power is an illusion. So is victory.",
                "You level up. The bugs don't care. They will persist.",
                f"Level {new_level} - more power, same existential dread."
            ],
            "corporate": [
                f"Level {new_level}! HR will want to discuss your career growth.",
                "You've been promoted. Same bugs, higher expectations.",
                f"Level {new_level} achieved! Let's circle back on your KPIs.",
                "Congratulations on the promotion. Now deliver more damage."
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
        super().__init__("Cyber Runner", 100, 100, 20, 5, "RUNNER")
        self.xp = 0
        self.level = 1
        self.gold = 0
        self.actions_per_turn = 2
        self.actions_used = 0
        
        # Cyberpunk themed attacks
        self.attacks = {
            "Quick Shot": {"damage": 15, "accuracy": 95, "description": "Basic shot attack"},
            "Pulse Wave": {"damage": 10, "accuracy": 90, "description": "Energy wave, hits all"},
            "Plasma Blade": {"damage": 25, "accuracy": 70, "description": "Powerful melee attack"},
            "Hack": {"damage": 5, "accuracy": 100, "description": "Hack enemy, reduces attack"},
            "Phase Shift": {"damage": 0, "accuracy": 100, "description": "Dodge next attack"},
        }
        
        self.upgrades = {
            "Laser Cannon": {"cost": 50, "effect": "attack", "value": 10, "description": "+10 Attack"},
            "Shield Matrix": {"cost": 50, "effect": "defense", "value": 10, "description": "+10 Defense"},
            "Nano Repair": {"cost": 40, "effect": "heal", "value": 30, "description": "Heal 30 HP"},
            "XP Boost": {"cost": 60, "effect": "xp_boost", "value": 20, "description": "+20% XP gain"},
            "Targeting AI": {"cost": 45, "effect": "crit", "value": 15, "description": "+15% Crit chance"},
            "Cyber Core": {"cost": 70, "effect": "max_hp", "value": 30, "description": "+30 Max HP"},
            "Sonic Pulse": {"damage": 20, "accuracy": 80, "description": "Stun attack"},
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
    def __init__(self, enemy_type=None):
        if enemy_type is None:
            # Fallback to zone 1 enemies
            enemy_type = random.choice(ZONES[1]["minions"])
        
        if enemy_type not in ENEMY_STATS:
            enemy_type = random.choice(list(ENEMY_STATS.keys()))
        
        stats = ENEMY_STATS[enemy_type]
        super().__init__(enemy_type, stats["hp"], stats["hp"], stats["attack"], stats["defense"], stats["emoji"])
        self.xp_reward = stats["xp"]
        self.gold_reward = stats["gold"]
        self.enemy_type = enemy_type
        self.charge_attack = stats.get("charge_attack", 1)
        self.charge = 0  # Reset charge at spawn
    
    def add_charge(self):
        self.charge = min(3, self.charge + 1)
    
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
        self.stats = PlayerStats()  # New charge-based stats
        self.combat_manager = CombatManager()  # New combat manager
        self.enemies = []
        self.current_enemy_index = 0
        self.game_state = "menu"
        self.roast_message = "Welcome to Cyberpunk RPG!"
        self.floor = 1
        self.high_score = 0
        self.score = 0
        self.action_cooldown = 0
        self.turn_in_progress = False  # Track if player is in combat turn
        
        self.generate_floor()
        
        # Zone transition state
        self.zone_transition_state = None  # "complete" or "entering"
        self.zone_transition_timer = 0
        self.zone_rewards = {"xp": 0, "gold": 0}
        self.previous_zone = 0
    
    def generate_floor(self):
        """Generate enemies based on zone progression."""
        self.enemies = []
        
        # Determine zone based on floor (now acting as level)
        # floor 1-3 = Zone 1, floor 4-6 = Zone 2, etc.
        zone_num = get_zone_for_level(self.floor)
        zone_data = ZONES[zone_num]
        
        # Determine number of enemies to spawn
        enemy_count = min(2 + self.floor // 2, 5)
        
        # Build enemy list for this zone/floor
        enemy_list = []
        
        # Check for boss fight (zones 3-5 have bosses after clearing minions)
        if zone_num >= 3 and "boss" in zone_data:
            # Spawn minions first, then boss
            minions_to_spawn = zone_data["minions"].copy()
            random.shuffle(minions_to_spawn)
            
            # Add minions (fewer than total to leave room for boss)
            for _ in range(min(enemy_count - 1, len(minions_to_spawn))):
                if minions_to_spawn:
                    enemy_list.append(minions_to_spawn.pop())
            
            # Add boss at the end
            enemy_list.append(zone_data["boss"])
        else:
            # Regular floor - spawn from zone minions
            minions = zone_data["minions"].copy()
            for _ in range(enemy_count):
                if minions:
                    enemy_list.append(random.choice(minions))
        
        # Create Enemy objects
        for enemy_name in enemy_list:
            self.enemies.append(Enemy(enemy_name))
        
        # Reset player charge at start of new zone/floor
        self.stats.reset_charge()
        
        self.current_enemy_index = 0
        self.roast_message = self.roast_engine.get_roast("turn_start")
    
    def get_current_enemy(self):
        if self.current_enemy_index < len(self.enemies):
            return self.enemies[self.current_enemy_index]
        return None
    
    def player_attack(self, action_key):
        """Handle player action using charge-based combat system."""
        global effects
        
        # Map keys to action names
        action_map = {
            1: "charge",
            2: "dodge", 
            3: "block",
            4: "shoot",
            5: "special"
        }
        
        if action_key not in action_map:
            return "Invalid action!"
        
        action_name = action_map[action_key]
        
        enemy = self.get_current_enemy()
        if not enemy:
            return "No enemy to attack!"
        
        # Add +1 charge at turn start
        self.stats.add_charge(1)
        
        # Resolve player action
        result = self.combat_manager.resolve_player_action(self.stats, enemy, action_name)
        
        # Add visual effects based on action
        if action_name == "charge":
            effects.add_floating_text(WIDTH//2 - 150, 300, "+1 CHARGE", CYAN, 30)
            effects.add_screen_flash(CYAN, 8)
        elif action_name == "dodge":
            if result["success"]:
                effects.add_floating_text(WIDTH//2 - 150, 300, "DODGED!", CYAN, 30)
                effects.add_screen_flash(CYAN, 10)
            else:
                effects.add_floating_text(WIDTH//2 - 150, 300, "DODGE FAILED", RED, 30)
        elif action_name == "block":
            if result["success"]:
                effects.add_floating_text(WIDTH//2 - 150, 300, "BLOCKED!", GREEN, 30)
                effects.add_screen_flash(GREEN, 10)
            else:
                effects.add_floating_text(WIDTH//2 - 150, 300, "BLOCK FAILED", RED, 30)
        elif action_name == "shoot":
            if result["success"]:
                if "crit" in result.get("effects", []):
                    effects.add_floating_text(WIDTH//2 + 150, 280, f"CRITICAL! -{result['damage']}", GOLD, 40)
                    effects.add_screen_flash(GOLD, 15)
                else:
                    effects.add_floating_text(WIDTH//2 + 150, 280, f"-{result['damage']}", WHITE, 35)
                effects.add_screen_flash(RED, 8)
                effects.add_shake(8, 10)
                # Attack particles
                for _ in range(8):
                    effects.add_particle(
                        WIDTH//2 + 150, 300,
                        RED if "crit" not in result.get("effects", []) else GOLD,
                        random.randint(3, 8),
                        (random.uniform(-3, 3), random.uniform(-2, -5)),
                        25
                    )
            else:
                effects.add_floating_text(WIDTH//2 + 150, 300, "MISS!", GRAY, 30)
        elif action_name == "special":
            if result["success"]:
                if "crit" in result.get("effects", []):
                    effects.add_floating_text(WIDTH//2 + 150, 280, f"MASSIVE! -{result['damage']}", GOLD, 40)
                    effects.add_screen_flash(GOLD, 20)
                else:
                    effects.add_floating_text(WIDTH//2 + 150, 280, f"-{result['damage']}", ORANGE, 35)
                effects.add_screen_flash(ORANGE, 12)
                effects.add_shake(12, 15)
                # Special attack particles
                for _ in range(12):
                    effects.add_particle(
                        WIDTH//2 + 150, 300,
                        ORANGE if "crit" not in result.get("effects", []) else GOLD,
                        random.randint(4, 10),
                        (random.uniform(-4, 4), random.uniform(-3, -6)),
                        30
                    )
            else:
                effects.add_floating_text(WIDTH//2 + 150, 300, "MISS!", GRAY, 30)
        
        # Check if enemy is defeated
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
            
            # Grant XP and gold
            leveled_up = self.stats.add_xp(enemy.xp_reward)
            self.stats.gold += enemy.gold_reward
            
            # Level up celebration!
            if leveled_up:
                # Screen flash - gold color
                effects.add_screen_flash(GOLD, 25)
                effects.add_shake(15, 20)
                
                # Floating text "LEVEL UP!"
                effects.add_floating_text(WIDTH//2, 200, "LEVEL UP!", GOLD, 60)
                effects.add_floating_text(WIDTH//2, 240, f"Welcome to Level {self.stats.level}!", WHITE, 50)
                
                # Particle celebration
                for _ in range(25):
                    effects.add_particle(
                        WIDTH//2 + random.randint(-200, 200),
                        HEIGHT//2,
                        random.choice([GOLD, YELLOW, ORANGE, WHITE]),
                        random.randint(4, 12),
                        (random.uniform(-5, 5), random.uniform(-8, -3)),
                        50
                    )
                
                # Roast message for level up
                self.roast_message = self.roast_engine.get_roast("level_up", {"new_level": self.stats.level})
                result_message = f"\n[VICTORY] {enemy.name} defeated! +{enemy.xp_reward} XP, {enemy.gold_reward} gold!\n*** LEVEL UP! Now level {self.stats.level}! ***"
            else:
                self.roast_message = self.roast_engine.get_roast("victory", {"enemy": enemy.name})
                result_message = f"\n[VICTORY] {enemy.name} defeated! +{enemy.xp_reward} XP, {enemy.gold_reward} gold!"
            
            self.current_enemy_index += 1
            if self.current_enemy_index >= len(self.enemies):
                # Check for final boss victory (Zone 5, Level 15 = MEGACORP CEO)
                if enemy.name == "MEGACORP CEO":
                    self.game_state = "victory"
                    self.roast_message = "YOU DEFEATED MEGACORP CEO! THE CYBER WORLD IS FREE!"
                    effects.add_screen_flash(GOLD, 30)
                    effects.add_shake(20, 25)
                    for _ in range(40):
                        effects.add_particle(
                            WIDTH//2, HEIGHT//2,
                            random.choice([GOLD, YELLOW, WHITE, CYAN]),
                            random.randint(5, 15),
                            (random.uniform(-8, 8), random.uniform(-10, -4)),
                            60
                        )
                else:
                    # Check if we're completing a zone (floors 3, 6, 9, 12 complete)
                    current_zone = get_zone_for_level(self.floor)
                    next_floor = self.floor + 1
                    next_zone = get_zone_for_level(next_floor)
                    
                    if next_zone > current_zone:
                        # Zone transition! Show transition screen
                        self.trigger_zone_transition(current_zone)
                    else:
                        # Same zone, just advance floor
                        self.floor += 1
                        self.generate_floor()
            
            return result["message"] + result_message
        
        # Enemy turn
        self.enemy_turn()
        
        return result["message"]
        
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
                # Check for final boss victory (Zone 5 = MEGACORP CEO)
                if enemy.name == "MEGACORP CEO":
                    self.game_state = "victory"
                    self.roast_message = "YOU DEFEATED MEGACORP CEO! THE CYBER WORLD IS FREE!"
                    effects.add_screen_flash(GOLD, 30)
                    effects.add_shake(20, 25)
                    for _ in range(40):
                        effects.add_particle(
                            WIDTH//2, HEIGHT//2,
                            random.choice([GOLD, YELLOW, WHITE, CYAN]),
                            random.randint(5, 15),
                            (random.uniform(-8, 8), random.uniform(-10, -4)),
                            60
                        )
                else:
                    # Check if we're completing a zone
                    current_zone = get_zone_for_level(self.floor)
                    next_floor = self.floor + 1
                    next_zone = get_zone_for_level(next_floor)
                    
                    if next_zone > current_zone:
                        # Zone transition! Show transition screen
                        self.trigger_zone_transition(current_zone)
                    else:
                        # Same zone, just advance floor
                        self.floor += 1
                        self.generate_floor()
        
        return result
    
    def enemy_turn(self):
        """Handle enemy turn using charge-based combat system."""
        global effects
        enemy = self.get_current_enemy()
        if not enemy:
            return
        
        # Resolve enemy attack using combat manager
        result = self.combat_manager.resolve_enemy_turn(self.stats, enemy)
        
        if result.get("dodged"):
            self.roast_message = "You dodged the attack! Even the roast engine is surprised."
            effects.add_floating_text(WIDTH//2 - 150, 300, "DODGED!", CYAN, 30)
            effects.add_screen_flash(CYAN, 10)
        elif result.get("blocked"):
            self.roast_message = "You blocked the enemy attack!"
            effects.add_floating_text(WIDTH//2 - 150, 300, "BLOCKED!", GREEN, 30)
            effects.add_screen_flash(GREEN, 10)
        else:
            damage = result.get("damage", 0)
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
        
        self.score += result.get("damage", 0) // 2
        
        # Update overcharge (decrement turns)
        self.stats.update_overcharge()
        
        # Check if player is defeated (using stats.hp)
        if self.stats.hp <= 0:
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
        
        if upgrade_name == "Sonic Pulse":
            self.player.attacks["Sonic Pulse"] = {"damage": upgrade["damage"], "accuracy": upgrade["accuracy"], "description": upgrade["description"]}
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
        """Heal the player using gold from new stats."""
        global effects
        if self.stats.gold >= 30:
            self.stats.gold -= 30
            old_hp = self.stats.hp
            self.stats.hp = min(self.stats.max_hp, self.stats.hp + 40)
            healed_amount = self.stats.hp - old_hp
            
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
    
    def buy_shop_item(self, item_name):
        """Buy an item from the shop."""
        global effects
        
        if item_name not in SHOP_ITEMS:
            return "Item not found!"
        
        item = SHOP_ITEMS[item_name]
        
        # Check if already purchased permanent item
        if item.get("type") == "permanent" and item_name in self.stats.purchased:
            return f"Already purchased {item_name}!"
        
        # Check gold
        if self.stats.gold < item["price"]:
            return f"Not enough gold! Need {item['price']}, have {self.stats.gold}"
        
        # Deduct gold
        self.stats.gold -= item["price"]
        
        # Apply item effect based on type
        if item.get("type") == "consumable":
            # Add to inventory
            if item_name not in self.stats.inventory:
                self.stats.inventory[item_name] = 0
            self.stats.inventory[item_name] += 1
            return f"Bought {item_name}! Use [I] to use items."
        
        elif item.get("type") == "permanent":
            # Apply permanent stat boost
            effect = item["effect"]
            value = item["value"]
            
            if effect == "attack":
                self.stats.attack += value
                effects.add_floating_text(WIDTH//2, HEIGHT//2 - 50, f"+{value} Attack", RED, 40)
            elif effect == "defense":
                self.stats.defense += value
                effects.add_floating_text(WIDTH//2, HEIGHT//2 - 50, f"+{value} Defense", BLUE, 40)
            elif effect == "speed":
                self.stats.speed += value
                effects.add_floating_text(WIDTH//2, HEIGHT//2 - 50, f"+{value} Speed", CYAN, 40)
            elif effect == "crit":
                self.stats.crit += value
                effects.add_floating_text(WIDTH//2, HEIGHT//2 - 50, f"+{value}% Crit", GOLD, 40)
            
            # Mark as purchased
            self.stats.purchased.append(item_name)
            
            # Visual effect
            effects.add_screen_flash(GREEN, 15)
            for _ in range(15):
                effects.add_particle(
                    WIDTH//2, HEIGHT//2,
                    random.choice([GOLD, YELLOW, GREEN]),
                    random.randint(4, 10),
                    (random.uniform(-4, 4), random.uniform(-5, -2)),
                    35
                )
            
            self.roast_message = self.roast_engine.get_roast("upgrade", {"upgrade": item_name})
            return f"Bought {item_name}! Permanent upgrade applied."
        
        elif item.get("type") == "stackable" and item["effect"] == "charge_chance":
            # Add overcharge stacks (max 50% = 5 stacks)
            max_chance = item.get("max_stacks", 5) * item["value"]
            current_chance = self.stats.get_overcharge_chance()
            
            if current_chance >= max_chance:
                self.stats.gold += item["price"]  # Refund
                return "Max overcharge reached (50%)!"
            
            self.stats.overcharge_stacks += 1
            self.stats.overcharge_turns = item.get("expires_turns", 10)
            
            new_chance = self.stats.get_overcharge_chance()
            effects.add_floating_text(WIDTH//2, HEIGHT//2 - 50, f"Overcharge: {new_chance}%", GOLD, 40)
            
            effects.add_screen_flash(GOLD, 15)
            for _ in range(15):
                effects.add_particle(
                    WIDTH//2, HEIGHT//2,
                    random.choice([GOLD, YELLOW, CYAN]),
                    random.randint(4, 10),
                    (random.uniform(-4, 4), random.uniform(-5, -2)),
                    35
                )
            
            return f"Bought {item_name}! Overcharge chance: {new_chance}%"
        
        return "Unknown item type!"
    
    def calculate_zone_rewards(self, zone_num):
        """Calculate bonus rewards for completing a zone."""
        # Base rewards scale with zone number
        base_xp = zone_num * 50
        base_gold = zone_num * 30
        
        # Bonus for completing zone
        bonus_xp = zone_num * 25
        bonus_gold = zone_num * 15
        
        return {
            "xp": base_xp + bonus_xp,
            "gold": base_gold + bonus_gold
        }
    
    def trigger_zone_transition(self, completed_zone_num):
        """Trigger zone transition screen when completing a zone."""
        global effects
        
        self.previous_zone = completed_zone_num
        self.zone_rewards = self.calculate_zone_rewards(completed_zone_num)
        
        # Grant zone completion rewards
        self.stats.add_xp(self.zone_rewards["xp"])
        self.stats.gold += self.zone_rewards["gold"]
        
        # Add celebration effects
        for _ in range(30):
            effects.add_particle(
                WIDTH//2, HEIGHT//2,
                random.choice([GOLD, YELLOW, CYAN, GREEN]),
                random.randint(4, 12),
                (random.uniform(-6, 6), random.uniform(-8, -3)),
                50
            )
        effects.add_screen_flash(GOLD, 25)
        effects.add_shake(15, 20)
        
        # Start zone transition
        self.game_state = "zone_transition"
        self.zone_transition_state = "complete"
        self.zone_transition_timer = 90  # ~3 seconds at 30 FPS for "ZONE COMPLETE"
        
        self.roast_message = f"ZONE {completed_zone_num} COMPLETE!"
    
    def update_zone_transition(self):
        """Update zone transition state. Called each frame."""
        global effects
        
        if self.game_state != "zone_transition":
            return
        
        self.zone_transition_timer -= 1
        
        if self.zone_transition_state == "complete":
            # After "ZONE COMPLETE" timer, show "Entering next zone"
            if self.zone_transition_timer <= 0:
                next_zone = self.previous_zone + 1
                if next_zone <= 5:
                    zone_name = ZONES[next_zone]["name"]
                    self.roast_message = f"Entering {zone_name}..."
                    self.zone_transition_state = "entering"
                    self.zone_transition_timer = 60  # ~2 seconds for "Entering"
                    
                    # Add transition effects
                    effects.add_screen_flash(CYAN, 15)
                    for _ in range(20):
                        effects.add_particle(
                            WIDTH//2, HEIGHT//2,
                            random.choice([CYAN, BLUE, WHITE]),
                            random.randint(4, 10),
                            (random.uniform(-5, 5), random.uniform(-6, -2)),
                            40
                        )
                else:
                    # Should not happen, but cap at zone 5
                    self.floor += 1
                    self.generate_floor()
                    self.game_state = "playing"
        
        elif self.zone_transition_state == "entering":
            # After "Entering" timer, advance to next floor
            if self.zone_transition_timer <= 0:
                self.floor += 1
                self.generate_floor()
                self.game_state = "playing"
                self.roast_message = self.roast_engine.get_roast("turn_start")
    
    def start_new_game(self):
        global effects
        self.player = Player()
        self.stats = PlayerStats()  # Reset new combat stats
        self.combat_manager = CombatManager()  # Reset combat manager
        self.floor = 1
        self.score = 0
        self.roast_engine.new_game()
        self.generate_floor()
        self.game_state = "playing"
        self.roast_message = self.roast_engine.get_roast("turn_start")
        effects = VisualEffects()  # Reset visual effects for new game
        
        # Reset zone transition state
        self.zone_transition_state = None
        self.zone_transition_timer = 0
        self.zone_rewards = {"xp": 0, "gold": 0}
        self.previous_zone = 0


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
    # Glow effect behind the bar
    if max_hp > 0 and hp > 0:
        hp_ratio = hp / max_hp
        glow_color = NEON_GREEN if hp_ratio > 0.5 else (YELLOW if hp_ratio > 0.25 else RED)
        # Draw glow
        for i in range(3):
            glow_alpha = 40 - i * 12
            glow_rect = pygame.Rect(x - 2 + i, y - 2 + i, width + 4 - i*2, height + 4 - i*2)
            glow_surf = pygame.Surface((width + 4, height + 4), pygame.SRCALPHA)
            pygame.draw.rect(glow_surf, (*glow_color, glow_alpha), (0, 0, width + 4, height + 4), border_radius=6)
            surface.blit(glow_surf, (x - 2 - i, y - 2 - i))
    
    # Background
    bg_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(surface, (30, 30, 45), bg_rect, border_radius=4)
    
    # Health fill with gradient - neon colors
    if max_hp > 0:
        fill_width = int((hp / max_hp) * (width - 4))
        if fill_width > 0:
            # Create gradient effect with neon colors
            for i in range(fill_width):
                ratio = i / fill_width
                if hp > max_hp * 0.5:
                    # Green to Yellow to Orange
                    r = int(NEON_GREEN[0] + (255 - NEON_GREEN[0]) * ratio * 2) if ratio < 0.5 else int(255 + (ORANGE[0] - 255) * (ratio - 0.5) * 2)
                    g = int(NEON_GREEN[1] + (223 - NEON_GREEN[1]) * ratio * 2) if ratio < 0.5 else int(223 + (150 - 223) * (ratio - 0.5) * 2)
                    b = int(NEON_GREEN[2] + (0 - NEON_GREEN[2]) * ratio * 2) if ratio < 0.5 else int(0 + (50 - 0) * (ratio - 0.5) * 2)
                else:
                    # Orange to Red
                    r = int(ORANGE[0] * 0.8 + 200 * ratio)
                    g = int(ORANGE[1] * 0.6 + 80 * ratio)
                    b = int(ORANGE[2] * 0.6 + 50 * ratio)
                pygame.draw.line(surface, (r, g, b), (x + 2 + i, y + 2), (x + 2 + i, y + height - 2))
    
    # Border - neon glow
    border_color = NEON_GREEN if hp > max_hp * 0.3 else RED
    pygame.draw.rect(surface, border_color, bg_rect, 2, border_radius=4)
    
    # HP text with shadow
    if show_text:
        text_shadow = font_small.render(f"{hp}/{max_hp}", True, (0, 0, 0))
        surface.blit(text_shadow, (x + width // 2 - text_shadow.get_width() // 2 + 1, y + 4))
        text = font_small.render(f"{hp}/{max_hp}", True, WHITE)
        surface.blit(text, (x + width // 2 - text.get_width() // 2, y + 3))
    
    # Add small decorative corners - neon style
    corner_color = NEON_GREEN if hp > max_hp * 0.3 else RED
    pygame.draw.circle(surface, corner_color, (x + 4, y + 4), 2)
    pygame.draw.circle(surface, corner_color, (x + width - 4, y + 4), 2)
    pygame.draw.circle(surface, corner_color, (x + 4, y + height - 4), 2)
    pygame.draw.circle(surface, corner_color, (x + width - 4, y + height - 4), 2)


def draw_entity_sprite(surface, x, y, sprite_type, name, hp, max_hp, size=80):
    # Draw the sprite area background - cyberpunk style
    sprite_bg = pygame.Rect(x - size//2 - 10, y - size//2 - 30, size + 20, size + 60)
    
    # Color based on type
    bg_color = (25, 30, 50)  # Dark blue-gray
    border_col = NEON_CYAN if sprite_type == "player" else RED
    
    pygame.draw.rect(surface, bg_color, sprite_bg, border_radius=8)
    pygame.draw.rect(surface, border_col, sprite_bg, 2, border_radius=8)
    
    # Draw ASCII art based on type - use cyber runner for player
    if sprite_type == "player":
        lines = CYBER_RUNNER_SPRITE.strip().split('\n')
        line_color = NEON_CYAN
    else:
        lines = ENEMY_SPRITES.get(name, "").strip().split('\n') if name in ENEMY_SPRITES else ["???", "???"]
        line_color = RED
    
    line_height = 14
    start_y = y - size//2 - 20
    for i, line in enumerate(lines):
        text = font_tiny.render(line, True, line_color)
        surface.blit(text, (x - text.get_width() // 2, start_y + i * line_height))
    
    # Draw name
    name_color = NEON_CYAN if sprite_type == "player" else RED
    name_text = font_small.render(name, True, name_color)
    surface.blit(name_text, (x - name_text.get_width() // 2, y + size//2 - 10))
    
    # Draw health bar below
    draw_health_bar(surface, x - 80, y + size//2 + 5, hp, max_hp, 160, 16)


def draw_battle_scene(surface, game, center_x, center_y):
    enemy = game.get_current_enemy()
    
    # Draw battle background with animated elements - cyberpunk style
    battle_bg = pygame.Rect(50, 140, WIDTH - 100, 350)
    pygame.draw.rect(surface, (20, 25, 45), battle_bg, border_radius=12)
    pygame.draw.rect(surface, NEON_MAGENTA, battle_bg, 3, border_radius=12)
    
    # Draw floor indicator with cyberpunk line
    pygame.draw.line(surface, (*NEON_CYAN, 40), (80, 480), (WIDTH - 80, 480), 2)
    
    if enemy:
        # Enemy position
        enemy_x = center_x + 150
        enemy_y = center_y - 30
        
        # Draw enemy with glow effect - red glow
        for i in range(3):
            glow_size = 100 + i * 10
            glow_alpha = 30 - i * 10
            glow_surf = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (*RED, glow_alpha), (glow_size//2, glow_size//2), glow_size//2)
            surface.blit(glow_surf, (enemy_x - glow_size//2, enemy_y - glow_size//2))
        
        draw_entity_sprite(surface, enemy_x, enemy_y, "enemy", enemy.name, enemy.hp, enemy.max_hp)
        
        # === CHARGE THREAT INDICATOR ===
        # Show enemy charge level (1, 2, or 3)
        threat_x = enemy_x + 80
        threat_y = enemy_y - 60
        
        # Threat background
        threat_box = pygame.Rect(threat_x - 15, threat_y - 10, 50, 25)
        pygame.draw.rect(surface, (30, 20, 40), threat_box, border_radius=4)
        
        # Border color based on charge level
        if enemy.charge >= 3:
            threat_color = RED  # Maximum danger
        elif enemy.charge >= 2:
            threat_color = ORANGE  # High danger
        else:
            threat_color = YELLOW  # Low danger
        
        pygame.draw.rect(surface, threat_color, threat_box, 2, border_radius=4)
        
        # Threat label and number
        threat_label = font_tiny.render("CHARGE:", True, threat_color)
        surface.blit(threat_label, (threat_x - 12, threat_y - 7))
        
        # Draw lightning bolts based on charge
        for b in range(enemy.charge):
            bolt_x = threat_x + 25 + b * 12
            bolt = font_small.render("⚡", True, threat_color)
            surface.blit(bolt, (bolt_x, threat_y + 5))
    
    # Player position
    player_x = center_x - 150
    player_y = center_y - 30
    
    # Draw player with cyan glow effect
    for i in range(3):
        glow_size = 90 + i * 10
        glow_alpha = 30 - i * 10
        glow_surf = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (*NEON_CYAN, glow_alpha), (glow_size//2, glow_size//2), glow_size//2)
        surface.blit(glow_surf, (player_x - glow_size//2, player_y - glow_size//2))
    
    # Use new PlayerStats for HP display - use cyber avatar
    draw_entity_sprite(surface, player_x, player_y, "player", "Cyber Runner", game.stats.hp, game.stats.max_hp)
    
    # VS indicator - cyberpunk style
    vs_text = font_large.render("VS", True, WHITE)
    pygame.draw.circle(surface, (30, 30, 50), (center_x, center_y + 20), 30)
    pygame.draw.circle(surface, NEON_MAGENTA, (center_x, center_y + 20), 30, 2)
    surface.blit(vs_text, (center_x - vs_text.get_width() // 2, center_y + 8))
    
    return player_y


def draw_game(screen, game):
    draw_gradient_background(screen)
    
    # Cyberpunk grid pattern
    for i in range(0, WIDTH, 50):
        pygame.draw.line(screen, (*CYAN, 10), (i, 0), (i, HEIGHT), 1)
    for i in range(0, HEIGHT, 50):
        pygame.draw.line(screen, (*CYAN, 8), (0, i), (WIDTH, i), 1)
    
    # Apply shake offset
    shake = effects.get_shake_offset()
    screen_copy = screen.copy()
    
    # Title section - CYBERPUNK RPG
    title_bg = pygame.Rect(WIDTH//2 - 300, 10, 600, 70)
    pygame.draw.rect(screen, (20, 20, 40), title_bg, border_radius=8)
    pygame.draw.rect(screen, NEON_CYAN, title_bg, 2, border_radius=8)
    
    title = font_title.render("CYBERPUNK RPG", True, NEON_CYAN)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))
    
    # Zone and Level indicator - top right
    current_zone = get_zone_for_level(game.floor)
    zone_name = ZONES[current_zone]["name"]
    floor_box = pygame.Rect(WIDTH - 220, 25, 200, 40)
    pygame.draw.rect(screen, DARK_GRAY, floor_box, border_radius=6)
    pygame.draw.rect(screen, NEON_MAGENTA, floor_box, 2, border_radius=6)
    zone_text = font_medium.render(f"Lv {game.floor} - Zone {current_zone}", True, NEON_MAGENTA)
    screen.blit(zone_text, (WIDTH - 210, 32))
    
    # Turn indicator
    turn_text = font_small.render(f"Turn: {game.roast_engine.turn_count}", True, LIGHT_GRAY)
    screen.blit(turn_text, (30, 35))
    
    # Draw battle scene
    center_x = WIDTH // 2
    center_y = 340
    runner_y = draw_battle_scene(screen, game, center_x, center_y)
    
    # Roast message panel - more prominent
    roast_panel_y = 510
    roast_panel = pygame.Rect(40, roast_panel_y, WIDTH - 80, 120)
    pygame.draw.rect(screen, (25, 20, 45), roast_panel, border_radius=12)
    pygame.draw.rect(screen, NEON_MAGENTA, roast_panel, 3, border_radius=12)
    
    # Roast label with glow effect
    roast_label = font_medium.render("SYSTEM MESSAGE", True, GOLD)
    screen.blit(roast_label, (60, roast_panel_y + 10))
    
    # Decorative quote marks
    quote_font = font_title
    screen.blit(quote_font.render('"', True, NEON_MAGENTA), (45, roast_panel_y + 5))
    screen.blit(quote_font.render('"', True, NEON_MAGENTA), (WIDTH - 60, roast_panel_y + 50))
    
    # Roast message with typewriter effect feel
    draw_text(screen, game.roast_message, 60, roast_panel_y + 40, font_medium, WHITE, WIDTH - 150)
    
    # Action feedback indicator
    action_hint = font_small.render("Press 1-5: Combat Actions | S: Shop | I: Inventory | H: Quick Heal", True, (120, 120, 140))
    screen.blit(action_hint, (WIDTH // 2 - action_hint.get_width() // 2, roast_panel_y + 95))
    
    # Stats bar at bottom - MORE PROMINENT
    stats_panel = pygame.Rect(40, 650, WIDTH - 80, 70)
    pygame.draw.rect(screen, (20, 25, 40), stats_panel, border_radius=8)
    pygame.draw.rect(screen, NEON_CYAN, stats_panel, 2, border_radius=8)
    
    # Stats with prominent display - using new PlayerStats
    stats = [
        (f"{game.stats.hp}/{game.stats.max_hp}", NEON_GREEN, "HP", game.stats.hp, game.stats.max_hp),
        (f"{game.stats.charge}/{game.stats.max_charge}", NEON_CYAN, "CHARGE", game.stats.charge, game.stats.max_charge),
        (f"Lv {game.stats.level}", GOLD, "LEVEL", game.stats.level, 15),
        (f"{game.stats.xp}/{game.stats.xp_to_next}", NEON_MAGENTA, "XP", game.stats.xp, game.stats.xp_to_next),
        (f"{game.stats.gold}", GOLD, "GOLD", game.stats.gold, 1000),
    ]
    
    bar_width = 180
    for i, (value, color, label, current, max_val) in enumerate(stats):
        x = 60 + i * 220
        
        # Label
        label_text = font_small.render(label, True, color)
        screen.blit(label_text, (x, 660))
        
        # Value text
        value_text = font_large.render(value, True, color)
        screen.blit(value_text, (x, 680))
        
        # Draw mini bar for stats that make sense
        if label in ["HP", "CHARGE", "XP"]:
            bar_x = x + 80
            bar_y = 685
            # Bar background
            pygame.draw.rect(screen, DARK_GRAY, (bar_x, bar_y, 120, 12), border_radius=3)
            # Bar fill
            fill_pct = min(1.0, current / max_val) if max_val > 0 else 0
            fill_width = int(116 * fill_pct)
            if fill_width > 0:
                pygame.draw.rect(screen, color, (bar_x + 2, bar_y + 2, fill_width, 8), border_radius=2)
            # Bar border
            pygame.draw.rect(screen, color, (bar_x, bar_y, 120, 12), 1, border_radius=3)
    
    # Draw visual effects
    effects.draw(screen)
    
    return runner_y


def draw_menu(screen, game):
    draw_gradient_background(screen)
    
    # Cyberpunk grid pattern in background
    for i in range(0, WIDTH, 50):
        pygame.draw.line(screen, (*CYAN, 20), (i, 0), (i, HEIGHT), 1)
    for i in range(0, HEIGHT, 50):
        pygame.draw.line(screen, (*CYAN, 15), (0, i), (WIDTH, i), 1)
    
    # Title with neon glow effect
    for i in range(5):
        glow_surface = pygame.Surface((700, 120), pygame.SRCALPHA)
        alpha = 50 - i * 10
        # Cyan glow
        pygame.draw.rect(glow_surface, (*NEON_CYAN, alpha), (0, 0, 700, 120), border_radius=20)
        screen.blit(glow_surface, (WIDTH//2 - 350, 100))
    
    title_box = pygame.Rect(WIDTH//2 - 300, 120, 600, 100)
    pygame.draw.rect(screen, (20, 20, 40), title_box, border_radius=12)
    pygame.draw.rect(screen, NEON_CYAN, title_box, 3, border_radius=12)
    
    title = font_title.render("CYBERPUNK RPG", True, NEON_CYAN)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 135))
    
    subtitle = font_large.render("NEO-TOKYO 2087", True, NEON_MAGENTA)
    screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, 190))
    
    # Cyber Runner sprite display
    runner_box = pygame.Rect(WIDTH//2 - 100, 280, 200, 120)
    pygame.draw.rect(screen, (20, 30, 40), runner_box, border_radius=10)
    pygame.draw.rect(screen, NEON_CYAN, runner_box, 2, border_radius=10)
    
    lines = CYBER_AVATAR.strip().split('\n')
    for i, line in enumerate(lines):
        text = font_tiny.render(line, True, NEON_CYAN)
        screen.blit(text, (WIDTH//2 - text.get_width()//2, 300 + i * 14))
    
    # Start button with animation hint - neon green
    start_text = font_large.render("[ ENTER ] TO START", True, NEON_GREEN)
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, 430))
    
    # How to Play button
    howto_box = pygame.Rect(WIDTH//2 - 90, 480, 180, 40)
    pygame.draw.rect(screen, (40, 20, 60), howto_box, border_radius=8)
    pygame.draw.rect(screen, NEON_MAGENTA, howto_box, 2, border_radius=8)
    howto_text = font_medium.render("HOW TO PLAY", True, WHITE)
    screen.blit(howto_text, (WIDTH//2 - howto_text.get_width()//2, 490))
    
    # High score
    high_box = pygame.Rect(WIDTH//2 - 120, 540, 240, 35)
    pygame.draw.rect(screen, DARK_GRAY, high_box, border_radius=6)
    high_text = font_small.render(f"High Score: {game.high_score}", True, GOLD)
    screen.blit(high_text, (WIDTH // 2 - high_text.get_width() // 2, 550))
    
    # Version info
    version_text = font_tiny.render("v2.0 - Cyberpunk Edition", True, (80, 80, 100))
    screen.blit(version_text, (WIDTH // 2 - version_text.get_width() // 2, 700))


def draw_how_to_play(screen):
    draw_gradient_background(screen)
    
    # Grid pattern
    for i in range(0, WIDTH, 40):
        pygame.draw.line(screen, (*NEON_CYAN, 10), (i, 0), (i, HEIGHT), 1)
    
    # Title - cyberpunk style
    title = font_title.render(">> OPERATIONAL MANUAL <<", True, NEON_CYAN)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 40))
    
    # Back hint
    back_text = font_small.render("[ H ] or [ ESC ] to return", True, NEON_MAGENTA)
    screen.blit(back_text, (WIDTH // 2 - back_text.get_width() // 2, 90))
    
    # Left panel - Gameplay - cyberpunk style
    left_panel = pygame.Rect(40, 130, WIDTH//2 - 60, 600)
    pygame.draw.rect(screen, (20, 25, 45), left_panel, border_radius=15)
    pygame.draw.rect(screen, NEON_CYAN, left_panel, 3, border_radius=15)
    
    left_title = font_large.render(">> MISSION BRIEFING", True, GOLD)
    screen.blit(left_title, (60, 145))
    
    # Section headers and content - simple format
    y = 190
    
    # OBJECTIVE
    section = font_medium.render("> OBJECTIVE", True, NEON_MAGENTA)
    screen.blit(section, (60, y))
    y += 30
    obj = font_small.render("Defeat MEGACORP CEO in Sector 5!", True, WHITE)
    screen.blit(obj, (60, y))
    y += 45
    
    # COMBAT
    section = font_medium.render("> COMBAT PROTOCOL", True, NEON_MAGENTA)
    screen.blit(section, (60, y))
    y += 30
    combat_lines = [
        "- Combat uses CHARGE-based system",
        "- Build charge to use powerful attacks",
        "- DODGE blocks Shoot, BLOCK blocks all",
        "- Watch enemy CHARGE THREAT indicator!",
        "- Defeat all enemies to advance"
    ]
    for line in combat_lines:
        text = font_small.render(line, True, WHITE)
        screen.blit(text, (60, y))
        y += 22
    y += 15
    
    # UPGRADES
    section = font_medium.render("> CYBERWARE", True, NEON_MAGENTA)
    screen.blit(section, (60, y))
    y += 30
    upgrade_lines = [
        "- Earn ¥ by defeating enemies",
        "- Buy gear from the Armory shop",
        "- Consumables, permanent upgrades available"
    ]
    for line in upgrade_lines:
        text = font_small.render(line, True, WHITE)
        screen.blit(text, (60, y))
        y += 22
    y += 15
    
    # TIPS
    section = font_medium.render("> TACTICAL TIPS", True, NEON_MAGENTA)
    screen.blit(section, (60, y))
    y += 30
    tip_lines = [
        "- Monitor HP - no auto-regen in combat",
        "- Quick Heal costs ¥30 when needed",
        "- Prioritize upgrades for your playstyle"
    ]
    for line in tip_lines:
        text = font_small.render(line, True, WHITE)
        screen.blit(text, (60, y))
        y += 22
    
    # Right panel - Controls - cyberpunk style
    right_panel = pygame.Rect(WIDTH//2 + 20, 130, WIDTH//2 - 60, 600)
    pygame.draw.rect(screen, (20, 25, 45), right_panel, border_radius=15)
    pygame.draw.rect(screen, NEON_MAGENTA, right_panel, 3, border_radius=15)
    
    right_title = font_large.render(">> CONTROLS", True, GOLD)
    screen.blit(right_title, (WIDTH//2 + 40, 145))
    
    y = 190
    controls = [
        ("1-5", "Combat Actions"),
        ("ENTER", "End Turn / Start Game"),
        ("S", "Open Armory Shop"),
        ("I", "Inventory"),
        ("H", "Quick Heal (¥30)"),
        ("ESC", "Close Menu"),
    ]
    
    for key, desc in controls:
        # Key box - cyberpunk style
        key_box = pygame.Rect(WIDTH//2 + 40, y, 90, 35)
        pygame.draw.rect(screen, (40, 30, 60), key_box, border_radius=5)
        pygame.draw.rect(screen, NEON_CYAN, key_box, 2, border_radius=5)
        key_text = font_medium.render(key, True, NEON_CYAN)
        screen.blit(key_text, (WIDTH//2 + 55, y + 7))
        
        # Description
        desc_text = font_small.render(desc, True, (180, 180, 180))
        screen.blit(desc_text, (WIDTH//2 + 150, y + 10))
        
        y += 45


def draw_attack_menu(screen, game, runner_y):
    menu_x = WIDTH - 300
    menu_y = max(150, runner_y - 100)
    
    # Menu panel - bigger and more readable - cyberpunk style
    menu_width = 280
    menu_height = 450
    menu_bg = pygame.Rect(menu_x, menu_y, menu_width, menu_height)
    pygame.draw.rect(screen, (20, 25, 45), menu_bg, border_radius=15)
    pygame.draw.rect(screen, NEON_CYAN, menu_bg, 3, border_radius=15)
    
    # Title with keyboard hint style
    title = font_large.render("COMBAT ACTIONS", True, NEON_MAGENTA)
    screen.blit(title, (menu_x + 20, menu_y + 15))
    
    # Charge display - prominent
    charge_color = NEON_CYAN if game.stats.charge >= 1 else GRAY
    charge_text = font_medium.render(f"CHARGE: {game.stats.charge}/{game.stats.max_charge}", True, charge_color)
    screen.blit(charge_text, (menu_x + 20, menu_y + 45))
    
    # Combat actions list
    y_offset = 85
    
    # Define combat actions with descriptions - cyberpunk colors
    combat_actions = [
        ("1", "CHARGE", "Get +1 charge", "100%", NEON_CYAN),
        ("2", "DODGE", "Block Shoot (85%)", f"vs charge=1", BLUE),
        ("3", "BLOCK", "Block attack", "70%/60%", NEON_GREEN),
        ("4", "SHOOT", f"1 charge, {game.stats.attack} DMG", "85% hit", RED),
        ("5", "SPECIAL", f"2 charge, {game.stats.attack*2} DMG", "70% hit", ORANGE),
    ]
    
    for key, name, desc, rate, color in combat_actions:
        # Check if action can be used
        action_cost = ACTIONS[name.lower()]["cost"]
        can_use = game.stats.charge >= action_cost
        
        # Row background
        row_bg = pygame.Rect(menu_x + 10, menu_y + y_offset, menu_width - 20, 50)
        bg_color = (35, 40, 60) if can_use else (25, 25, 35)
        pygame.draw.rect(screen, bg_color, row_bg, border_radius=8)
        
        # Border - neon effect
        border_color = color if can_use else (50, 50, 50)
        pygame.draw.rect(screen, border_color, row_bg, 1, border_radius=8)
        
        # Key indicator box
        key_box = pygame.Rect(menu_x + 20, menu_y + y_offset + 10, 36, 36)
        key_bg = color if can_use else (50, 50, 50)
        pygame.draw.rect(screen, key_bg, key_box, border_radius=6)
        pygame.draw.rect(screen, WHITE if can_use else GRAY, key_box, 2, border_radius=6)
        key_text = font_medium.render(key, True, WHITE if can_use else GRAY)
        screen.blit(key_text, (menu_x + 26, menu_y + y_offset + 15))
        
        # Action name
        name_render = font_medium.render(name, True, color if can_use else GRAY)
        screen.blit(name_render, (menu_x + 70, menu_y + y_offset + 5))
        
        # Description with success rate
        info_text = f"{desc} | {rate}"
        info_render = font_small.render(info_text, True, NEON_CYAN if can_use else GRAY)
        screen.blit(info_render, (menu_x + 70, menu_y + y_offset + 28))
        
        y_offset += 58
    
    # Actions section
    actions_y = menu_y + y_offset + 10
    
    # Divider - neon line
    pygame.draw.line(screen, (*NEON_MAGENTA, 80), (menu_x + 20, actions_y), (menu_x + menu_width - 20, actions_y), 2)
    actions_y += 15
    
    # Shop and heal buttons - cyberpunk style
    # Shop button
    shop_box = pygame.Rect(menu_x + 10, actions_y, 125, 35)
    pygame.draw.rect(screen, (40, 30, 60), shop_box, border_radius=6)
    pygame.draw.rect(screen, NEON_CYAN, shop_box, 2, border_radius=6)
    s_text = font_medium.render("[S] Shop", True, WHITE)
    screen.blit(s_text, (menu_x + 30, actions_y + 5))
    
    # Heal button
    heal_box = pygame.Rect(menu_x + 145, actions_y, 125, 35)
    pygame.draw.rect(screen, (30, 50, 30), heal_box, border_radius=6)
    pygame.draw.rect(screen, NEON_GREEN, heal_box, 2, border_radius=6)
    h_text = font_medium.render("[H] Heal", True, WHITE)
    screen.blit(h_text, (menu_x + 165, actions_y + 5))
    
    # Inventory button
    inv_box = pygame.Rect(menu_x + 10, actions_y + 45, 125, 30)
    pygame.draw.rect(screen, (40, 30, 60), inv_box, border_radius=6)
    pygame.draw.rect(screen, NEON_MAGENTA, inv_box, 2, border_radius=6)
    i_text = font_small.render("[I] Inventory", True, WHITE)
    screen.blit(i_text, (menu_x + 25, actions_y + 50))
    
    # Gold display - cyberpunk style
    gold_box = pygame.Rect(menu_x + 10, actions_y + 85, menu_width - 20, 35)
    pygame.draw.rect(screen, (40, 35, 20), gold_box, border_radius=4)
    pygame.draw.rect(screen, GOLD, gold_box, 2, border_radius=4)
    gold_text = font_medium.render(f"¥ {game.stats.gold}", True, GOLD)
    screen.blit(gold_text, (menu_x + 30, actions_y + 90))


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


def draw_shop(screen, game):
    """Draw the new shop UI with shop items - cyberpunk style."""
    # Dark overlay
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(220)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    # Shop panel - wider for items - cyberpunk style
    shop_rect = pygame.Rect(80, 40, WIDTH - 160, HEIGHT - 80)
    pygame.draw.rect(screen, (20, 25, 45), shop_rect, border_radius=16)
    pygame.draw.rect(screen, NEON_CYAN, shop_rect, 3, border_radius=16)
    
    # Grid pattern overlay
    for i in range(0, WIDTH - 160, 40):
        pygame.draw.line(screen, (*NEON_CYAN, 10), (80 + i, 40), (80 + i, HEIGHT - 40), 1)
    
    # Title - cyberpunk style
    title = font_title.render("// ARMORY //", True, NEON_CYAN)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 55))
    
    # Gold and Overcharge display - cyberpunk
    gold_box = pygame.Rect(WIDTH//2 - 100, 100, 200, 40)
    pygame.draw.rect(screen, (30, 25, 40), gold_box, border_radius=6)
    pygame.draw.rect(screen, GOLD, gold_box, 2, border_radius=6)
    gold_text = font_medium.render(f"¥ {game.stats.gold}", True, GOLD)
    screen.blit(gold_text, (WIDTH // 2 - gold_text.get_width() // 2, 110))
    
    # Overcharge indicator
    overcharge_chance = game.stats.get_overcharge_chance()
    if overcharge_chance > 0:
        overcharge_box = pygame.Rect(WIDTH//2 - 120, 145, 240, 30)
        pygame.draw.rect(screen, (40, 30, 40), overcharge_box, border_radius=4)
        pygame.draw.rect(screen, NEON_MAGENTA, overcharge_box, 1, border_radius=4)
        overcharge_text = font_small.render(f"OVERCHARGE: {overcharge_chance}% ({game.stats.overcharge_turns}t)", True, NEON_MAGENTA)
        screen.blit(overcharge_text, (WIDTH // 2 - overcharge_text.get_width() // 2, 152))
    
    # Get items by category
    consumables, permanent, stackable = get_shop_items_by_category()
    
    y_start = 185
    
    # === CONSUMABLES ===
    section_y = y_start
    section_title = font_large.render("> CONSUMABLES", True, NEON_GREEN)
    screen.blit(section_title, (110, section_y))
    
    i = 0
    for name, item in consumables.items():
        col = i % 4
        row = i // 4
        x = 110 + col * 270
        y = section_y + 35 + row * 100
        
        card = pygame.Rect(x, y, 250, 90)
        can_afford = game.stats.gold >= item["price"]
        owned = game.stats.inventory.get(name, 0)
        
        card_color = (25, 40, 35) if can_afford else (30, 30, 35)
        pygame.draw.rect(screen, card_color, card, border_radius=8)
        border_color = NEON_GREEN if can_afford else RED
        pygame.draw.rect(screen, border_color, card, 2, border_radius=8)
        
        # Name
        name_text = font_medium.render(name, True, NEON_CYAN if can_afford else GRAY)
        screen.blit(name_text, (x + 12, y + 8))
        
        # Description
        desc_text = font_small.render(item["description"], True, WHITE if can_afford else GRAY)
        screen.blit(desc_text, (x + 12, y + 35))
        
        # Price and owned
        price_text = font_small.render(f"¥ {item['price']}", True, GOLD if can_afford else RED)
        screen.blit(price_text, (x + 12, y + 60))
        
        if owned > 0:
            owned_text = font_small.render(f"x{owned}", True, NEON_MAGENTA)
            screen.blit(owned_text, (x + 180, y + 60))
        
        # Key hint
        key_hint = font_tiny.render(f"[{i+1}]", True, (80, 80, 100))
        screen.blit(key_hint, (x + 215, y + 12))
        
        i += 1
    
    # === PERMANENT UPGRADES ===
    perm_start_y = section_y + 35 + ((len(consumables) + 3) // 4) * 100 + 25
    perm_title = font_large.render("> PERMANENT UPGRADES", True, NEON_CYAN)
    screen.blit(perm_title, (110, perm_start_y))
    
    i = 0
    for name, item in permanent.items():
        purchased = name in game.stats.purchased
        col = i % 4
        row = i // 4
        x = 110 + col * 270
        y = perm_start_y + 35 + row * 100
        
        card = pygame.Rect(x, y, 250, 90)
        can_afford = game.stats.gold >= item["price"] and not purchased
        
        card_color = (25, 35, 45) if can_afford else (30, 30, 40)
        if purchased:
            card_color = (25, 40, 30)  # Greenish for purchased
        pygame.draw.rect(screen, card_color, card, border_radius=8)
        
        if purchased:
            border_color = NEON_GREEN
        else:
            border_color = NEON_CYAN if can_afford else RED
        pygame.draw.rect(screen, border_color, card, 2, border_radius=8)
        
        # Name
        name_text = font_medium.render(name, True, NEON_CYAN if not purchased else NEON_GREEN)
        screen.blit(name_text, (x + 12, y + 8))
        
        # Description
        desc_text = font_small.render(item["description"], True, WHITE if not purchased else GRAY)
        screen.blit(desc_text, (x + 12, y + 35))
        
        # Price or purchased indicator
        if purchased:
            price_text = font_small.render("INSTALLED", True, NEON_GREEN)
        else:
            price_text = font_small.render(f"¥ {item['price']}", True, GOLD if can_afford else RED)
        screen.blit(price_text, (x + 12, y + 60))
        
        # Key hint
        key_hint = font_tiny.render(f"[{i+len(consumables)+1}]", True, (80, 80, 100))
        screen.blit(key_hint, (x + 215, y + 12))
        
        i += 1
    
    # === STACKABLE ===
    stack_start_y = perm_start_y + 35 + ((len(permanent) + 3) // 4) * 100 + 25
    stack_title = font_large.render("> TEMPORARY CHIPS (EXPIRES)", True, NEON_MAGENTA)
    screen.blit(stack_title, (110, stack_start_y))
    
    i = 0
    for name, item in stackable.items():
        col = i % 4
        row = i // 4
        x = 110 + col * 270
        y = stack_start_y + 35 + row * 100
        
        card = pygame.Rect(x, y, 250, 90)
        can_afford = game.stats.gold >= item["price"]
        
        card_color = (35, 30, 45) if can_afford else (35, 30, 40)
        pygame.draw.rect(screen, card_color, card, border_radius=8)
        border_color = NEON_MAGENTA if can_afford else RED
        pygame.draw.rect(screen, border_color, card, 2, border_radius=8)
        
        # Name
        name_text = font_medium.render(name, True, NEON_MAGENTA if can_afford else GRAY)
        screen.blit(name_text, (x + 12, y + 8))
        
        # Description
        desc_text = font_small.render(item["description"], True, WHITE if can_afford else GRAY)
        screen.blit(desc_text, (x + 12, y + 35))
        
        # Price
        price_text = font_small.render(f"¥ {item['price']}", True, GOLD if can_afford else RED)
        screen.blit(price_text, (x + 12, y + 60))
        
        # Key hint
        key_hint = font_tiny.render(f"[{i+len(consumables)+len(permanent)+1}]", True, (80, 80, 100))
        screen.blit(key_hint, (x + 215, y + 12))
        
        i += 1
    
    # Exit and inventory hints - cyberpunk style
    exit_box = pygame.Rect(WIDTH//2 - 180, HEIGHT - 70, 160, 35)
    pygame.draw.rect(screen, (30, 30, 45), exit_box, border_radius=6)
    pygame.draw.rect(screen, WHITE, exit_box, 1, border_radius=6)
    exit_text = font_small.render("ESC to close", True, WHITE)
    screen.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2 + 20, HEIGHT - 62))
    
    # Inventory hint
    inv_box = pygame.Rect(WIDTH//2 + 20, HEIGHT - 70, 160, 35)
    pygame.draw.rect(screen, (30, 30, 45), inv_box, border_radius=6)
    pygame.draw.rect(screen, NEON_MAGENTA, inv_box, 1, border_radius=6)
    inv_text = font_small.render("[I] Inventory", True, WHITE)
    screen.blit(inv_text, (WIDTH // 2 + 35, HEIGHT - 62))


def draw_inventory(screen, game):
    """Draw the inventory UI to use items - cyberpunk style."""
    # Dark overlay
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(220)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    # Inventory panel - cyberpunk style
    inv_rect = pygame.Rect(250, 120, WIDTH - 500, 500)
    pygame.draw.rect(screen, (20, 25, 45), inv_rect, border_radius=16)
    pygame.draw.rect(screen, NEON_MAGENTA, inv_rect, 3, border_radius=16)
    
    # Grid overlay
    for i in range(0, WIDTH - 500, 30):
        pygame.draw.line(screen, (*NEON_MAGENTA, 10), (250 + i, 120), (250 + i, 620), 1)
    
    # Title
    title = font_title.render("// INVENTORY //", True, NEON_MAGENTA)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 135))
    
    # Subtitle
    sub_text = font_small.render("Press number to USE item", True, NEON_CYAN)
    screen.blit(sub_text, (WIDTH // 2 - sub_text.get_width() // 2, 175))
    
    # Show consumables
    y = 220
    has_items = False
    
    for item_name, count in game.stats.inventory.items():
        if count > 0:
            has_items = True
            item = SHOP_ITEMS.get(item_name)
            if not item:
                continue
            
            # Item card - cyberpunk style
            card = pygame.Rect(290, y, WIDTH - 580, 70)
            pygame.draw.rect(screen, (25, 35, 40), card, border_radius=8)
            pygame.draw.rect(screen, NEON_GREEN, card, 2, border_radius=8)
            
            # Name and count
            name_text = font_medium.render(item_name, True, NEON_CYAN)
            screen.blit(name_text, (310, y + 10))
            
            count_text = font_medium.render(f"x{count}", True, NEON_MAGENTA)
            screen.blit(count_text, (WIDTH - 360, y + 10))
            
            # Description
            desc_text = font_small.render(item["description"], True, WHITE)
            screen.blit(desc_text, (310, y + 38))
            
            # Use button hint
            use_text = font_tiny.render("[USE]", True, NEON_GREEN)
            screen.blit(use_text, (WIDTH - 360, y + 40))
            
            y += 85
    
    if not has_items:
        empty_text = font_medium.render("No items in inventory!", True, GRAY)
        screen.blit(empty_text, (WIDTH // 2 - empty_text.get_width() // 2, 320))
    
    # Exit hint - cyberpunk style
    exit_box = pygame.Rect(WIDTH//2 - 120, HEIGHT - 100, 240, 40)
    pygame.draw.rect(screen, (30, 35, 50), exit_box, border_radius=6)
    pygame.draw.rect(screen, WHITE, exit_box, 1, border_radius=6)
    exit_text = font_small.render("ESC or S to close", True, WHITE)
    screen.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, HEIGHT - 90))


def draw_zone_transition(screen, game):
    """Draw zone transition screen with completion message and rewards - cyberpunk style."""
    draw_gradient_background(screen)
    
    # Glitch effect - random horizontal offset
    glitch_offset = random.randint(-3, 3) if random.random() < 0.3 else 0
    
    # Draw celebration particles in background - cyberpunk colors
    for _ in range(5):
        effects.add_particle(
            random.randint(100, WIDTH - 100),
            random.randint(100, HEIGHT - 100),
            random.choice([GOLD, NEON_CYAN, NEON_GREEN, NEON_MAGENTA, PURPLE]),
            random.randint(3, 10),
            (random.uniform(-3, 3), random.uniform(-4, -1)),
            40
        )
    
    # Scanline effect
    for y in range(0, HEIGHT, 4):
        pygame.draw.line(screen, (*BLACK, 30), (0, y), (WIDTH, y), 1)
    
    # Main transition panel - cyberpunk style
    panel_width = 650
    panel_height = 480
    panel_x = WIDTH // 2 - panel_width // 2
    panel_y = HEIGHT // 2 - panel_height // 2
    
    # Panel background with gradient effect
    panel_bg = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
    pygame.draw.rect(screen, (20, 25, 50), panel_bg, border_radius=20)
    pygame.draw.rect(screen, NEON_CYAN, panel_bg, 4, border_radius=20)
    
    # Decorative tech lines
    for i in range(0, panel_width, 20):
        pygame.draw.line(screen, (*NEON_CYAN, 30), (panel_x + i, panel_y), (panel_x + i + 10, panel_y), 2)
        pygame.draw.line(screen, (*NEON_CYAN, 30), (panel_x + i, panel_y + panel_height), (panel_x + i + 10, panel_y + panel_height), 2)
    
    if game.zone_transition_state == "complete":
        # ZONE COMPLETE - Big celebration with glitch effect
        zone_num = game.previous_zone
        zone_name = ZONES[zone_num]["name"]
        
        # Animated "ZONE COMPLETE" with glow - cyan/magenta
        for i in range(5):
            glow_alpha = 100 - i * 20
            glow_text = font_title.render(f"ZONE {zone_num} COMPLETE!", True, (*NEON_MAGENTA, glow_alpha))
            screen.blit(glow_text, (WIDTH // 2 - glow_text.get_width() // 2 + (i-2) + glitch_offset, 160 + (i-2)))
        
        zone_complete_text = font_title.render(f"ZONE {zone_num} COMPLETE!", True, GOLD)
        screen.blit(zone_complete_text, (WIDTH // 2 - zone_complete_text.get_width() // 2 + glitch_offset, 160))
        
        # Zone name - cyan
        name_text = font_large.render(zone_name, True, NEON_CYAN)
        screen.blit(name_text, (WIDTH // 2 - name_text.get_width() // 2, 220))
        
        # Rewards panel - tech style
        rewards_box = pygame.Rect(panel_x + 50, panel_y + 90, panel_width - 100, 180)
        pygame.draw.rect(screen, (25, 30, 50), rewards_box, border_radius=12)
        pygame.draw.rect(screen, NEON_MAGENTA, rewards_box, 2, border_radius=12)
        
        # Rewards title
        rewards_title = font_large.render(">> SYSTEM REWARDS <<", True, GOLD)
        screen.blit(rewards_title, (WIDTH // 2 - rewards_title.get_width() // 2, panel_y + 105))
        
        # XP reward - magenta
        xp_text = font_medium.render(f"+ {game.zone_rewards['xp']} XP", True, NEON_MAGENTA)
        screen.blit(xp_text, (WIDTH // 2 - xp_text.get_width() // 2, panel_y + 155))
        
        # Gold reward - gold
        gold_text = font_medium.render(f"+ ¥ {game.zone_rewards['gold']}", True, GOLD)
        screen.blit(gold_text, (WIDTH // 2 - gold_text.get_width() // 2, panel_y + 190))
        
        # Continue hint - glitchy text
        timer_text = font_small.render(f">> ENTERING SECTOR {zone_num + 1} IN {game.zone_transition_timer // 30 + 1}... <<", True, NEON_CYAN)
        screen.blit(timer_text, (WIDTH // 2 - timer_text.get_width() // 2, panel_y + 270))
        
        # Decorative cyber runner
        runner_box = pygame.Rect(WIDTH//2 - 60, panel_y + 320, 120, 90)
        pygame.draw.rect(screen, (25, 35, 50), runner_box, border_radius=8)
        pygame.draw.rect(screen, NEON_CYAN, runner_box, 2, border_radius=8)
        
        lines = CYBER_AVATAR.strip().split('\n')
        for i, line in enumerate(lines):
            text = font_tiny.render(line, True, NEON_CYAN)
            screen.blit(text, (WIDTH//2 - text.get_width()//2, panel_y + 335 + i * 12))
    
    elif game.zone_transition_state == "entering":
        # ENTERING NEXT ZONE - glitch/tech effect
        next_zone = game.previous_zone + 1
        zone_name = ZONES[next_zone]["name"]
        
        # Animated "Entering" with glow - scanline effect
        for i in range(4):
            glow_alpha = 80 - i * 20
            glow_text = font_title.render(f">> ENTERING {zone_name}... <<", True, (*NEON_CYAN, glow_alpha))
            screen.blit(glow_text, (WIDTH // 2 - glow_text.get_width() // 2 + (i-1) + glitch_offset, 200 + (i-1)))
        
        entering_text = font_title.render(f">> ENTERING {zone_name}... <<", True, NEON_CYAN)
        screen.blit(entering_text, (WIDTH // 2 - entering_text.get_width() // 2 + glitch_offset, 200))
        
        # Zone number indicator - tech style
        zone_indicator = font_large.render(f"SECTOR {next_zone} / 5", True, WHITE)
        screen.blit(zone_indicator, (WIDTH // 2 - zone_indicator.get_width() // 2, 280))
        
        # Progress bar showing zone progression - cyberpunk
        progress_width = 450
        progress_height = 25
        progress_x = WIDTH // 2 - progress_width // 2
        progress_y = 340
        
        # Background
        pygame.draw.rect(screen, DARK_GRAY, (progress_x, progress_y, progress_width, progress_height), border_radius=10)
        
        # Fill based on zone - gradient cyan to magenta
        fill_ratio = next_zone / 5
        fill_width = int(progress_width * fill_ratio)
        if fill_width > 0:
            pygame.draw.rect(screen, NEON_CYAN, (progress_x + 2, progress_y + 2, fill_width - 4, progress_height - 4), border_radius=8)
        
        # Border - neon
        pygame.draw.rect(screen, NEON_MAGENTA, (progress_x, progress_y, progress_width, progress_height), 2, border_radius=10)
        
        # Zone markers
        for z in range(1, 6):
            marker_x = progress_x + (progress_width * z // 5)
            marker_color = NEON_GREEN if z <= next_zone else GRAY
            pygame.draw.circle(screen, marker_color, (marker_x, progress_y + progress_height // 2), 6)
        
        # Loading text - tech style
        loading_text = font_small.render(">> INITIALIZING COMBAT SEQUENCE... <<", True, NEON_CYAN)
        screen.blit(loading_text, (WIDTH // 2 - loading_text.get_width() // 2, 400))
        
        # Timer
        timer_text = font_medium.render(f"{game.zone_transition_timer // 30 + 1}...", True, NEON_MAGENTA)
        screen.blit(timer_text, (WIDTH // 2 - timer_text.get_width() // 2, 440))
    
    # Draw visual effects
    effects.draw(screen)


def main():
    game = Game()
    running = True
    shop_open = False
    inventory_open = False
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
                    elif event.key == pygame.K_h or event.key == pygame.K_ESCAPE:
                        show_how_to_play = not show_how_to_play
                
                elif game.game_state == "playing":
                    # Handle shop state
                    if shop_open:
                        if event.key == pygame.K_ESCAPE or event.key == pygame.K_s:
                            shop_open = False
                        elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, 
                                         pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0]:
                            # Get all shop items in order
                            consumables, permanent, stackable = get_shop_items_by_category()
                            all_items = list(consumables.keys()) + list(permanent.keys()) + list(stackable.keys())
                            
                            # Key mapping: 1-7 for consumables, 8-11 for permanent, 12+ for stackable
                            key_idx = event.key - pygame.K_1
                            if event.key == pygame.K_0:
                                key_idx = 9  # 0 maps to position 9 (index 9)
                            
                            if key_idx < len(all_items):
                                item_name = all_items[key_idx]
                                result = game.buy_shop_item(item_name)
                                print(result)
                    # Handle inventory state
                    elif inventory_open:
                        if event.key == pygame.K_ESCAPE or event.key == pygame.K_i or event.key == pygame.K_s:
                            inventory_open = False
                        elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]:
                            # Use item from inventory
                            consumables_list = list(game.stats.inventory.items())
                            key_idx = event.key - pygame.K_1
                            if key_idx < len(consumables_list):
                                item_name, count = consumables_list[key_idx]
                                if count > 0:
                                    result = game.stats.apply_item_effect(item_name)
                                    print(result)
                    else:
                        # Handle new combat actions (keys 1-5)
                        if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]:
                            action_key = event.key - pygame.K_1 + 1  # Convert to 1-5
                            result = game.player_attack(action_key)
                            print(result)
                        
                        # Open shop with S
                        elif event.key == pygame.K_s:
                            shop_open = True
                        
                        # Open inventory with I
                        elif event.key == pygame.K_i:
                            inventory_open = True
                        
                        # Old heal with H (still works)
                        elif event.key == pygame.K_h:
                            result = game.heal_player()
                            print(result)
                
                elif game.game_state in ["victory", "defeat"]:
                    if event.key == pygame.K_RETURN:
                        game.game_state = "menu"
                
                elif game.game_state == "zone_transition":
                    # Zone transition is automatic - no user input needed
                    pass
        
        # Update zone transition state each frame
        if game.game_state == "zone_transition":
            game.update_zone_transition()
        
        if game.game_state == "menu":
            if show_how_to_play:
                draw_how_to_play(screen)
            else:
                draw_menu(screen, game)
        elif game.game_state == "playing":
            runner_y = draw_game(screen, game)
            draw_attack_menu(screen, game, runner_y)
            if shop_open:
                draw_shop(screen, game)
            if inventory_open:
                draw_inventory(screen, game)
        elif game.game_state == "zone_transition":
            draw_zone_transition(screen, game)
        elif game.game_state == "victory":
            draw_gradient_background(screen)
            
            # Add extra celebration particles for victory - cyberpunk colors
            if random.random() < 0.3:
                effects.add_particle(
                    random.randint(100, WIDTH - 100),
                    random.randint(50, HEIGHT - 150),
                    random.choice([GOLD, NEON_CYAN, NEON_MAGENTA, NEON_GREEN, WHITE]),
                    random.randint(4, 12),
                    (random.uniform(-4, 4), random.uniform(-5, -2)),
                    50
                )
            
            # Victory panel - cyberpunk style
            victory_box = pygame.Rect(WIDTH//2 - 320, 80, 640, 540)
            pygame.draw.rect(screen, (20, 25, 50), victory_box, border_radius=20)
            pygame.draw.rect(screen, NEON_CYAN, victory_box, 4, border_radius=20)
            
            # Tech decoration
            for i in range(0, 640, 30):
                pygame.draw.line(screen, (*NEON_CYAN, 40), (WIDTH//2 - 320 + i, 80), (WIDTH//2 - 320 + i + 15, 80), 2)
                pygame.draw.line(screen, (*NEON_CYAN, 40), (WIDTH//2 - 320 + i, 620), (WIDTH//2 - 320 + i + 15, 620), 2)
            
            # Victory text with glow - neon style
            for i in range(6):
                glow = font_title.render(">> MISSION COMPLETE <<", True, (*NEON_MAGENTA, 100 - i * 18))
                screen.blit(glow, (WIDTH // 2 - glow.get_width() // 2 + (i-2)*3, 110 + (i-2)*3))
            
            win_text = font_title.render(">> MISSION COMPLETE <<", True, NEON_CYAN)
            screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, 110))
            
            # Game complete message
            complete_text = font_large.render("NEO-TOKYO HAS BEEN LIBERATED!", True, NEON_MAGENTA)
            screen.blit(complete_text, (WIDTH // 2 - complete_text.get_width() // 2, 170))
            
            # Stats panel - tech style
            stats_box = pygame.Rect(WIDTH//2 - 220, 220, 440, 220)
            pygame.draw.rect(screen, (25, 30, 50), stats_box, border_radius=12)
            pygame.draw.rect(screen, NEON_MAGENTA, stats_box, 2, border_radius=12)
            
            # Stats title
            stats_title = font_medium.render(">> MISSION REPORT <<", True, GOLD)
            screen.blit(stats_title, (WIDTH // 2 - stats_title.get_width() // 2, 235))
            
            # Display various stats - cyberpunk
            final_stats = [
                ("Score", f"{game.score}", NEON_CYAN),
                ("Final Level", f"{game.stats.level}", GOLD),
                ("Credits Earned", f"¥ {game.stats.gold}", GOLD),
                ("Sectors Cleared", "5/5", NEON_GREEN),
            ]
            
            for i, (label, value, color) in enumerate(final_stats):
                y_pos = 280 + i * 40
                label_text = font_medium.render(label + ":", True, LIGHT_GRAY)
                value_text = font_large.render(str(value), True, color)
                screen.blit(label_text, (WIDTH // 2 - 160, y_pos))
                screen.blit(value_text, (WIDTH // 2 + 60, y_pos))
            
            # System message
            msg_box = pygame.Rect(WIDTH//2 - 260, 460, 520, 50)
            pygame.draw.rect(screen, (30, 35, 55), msg_box, border_radius=8)
            pygame.draw.rect(screen, NEON_CYAN, msg_box, 1, border_radius=8)
            roast_text = font_small.render(game.roast_message, True, WHITE)
            screen.blit(roast_text, (WIDTH // 2 - roast_text.get_width() // 2, 478))
            
            # Restart hint - cyberpunk button
            restart_box = pygame.Rect(WIDTH//2 - 160, 530, 320, 45)
            pygame.draw.rect(screen, (25, 40, 35), restart_box, border_radius=8)
            pygame.draw.rect(screen, NEON_GREEN, restart_box, 2, border_radius=8)
            restart_text = font_medium.render("[ ENTER ] TO RESTART", True, NEON_GREEN)
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, 542))
            
            # Draw visual effects
            effects.draw(screen)
        
        elif game.game_state == "defeat":
            draw_gradient_background(screen)
            
            # Red scanline effect for defeat
            for y in range(0, HEIGHT, 6):
                pygame.draw.line(screen, (40, 10, 10), (0, y), (WIDTH, y), 1)
            
            # Defeat panel - cyberpunk style
            defeat_box = pygame.Rect(WIDTH//2 - 280, 120, 560, 480)
            pygame.draw.rect(screen, (25, 20, 30), defeat_box, border_radius=20)
            pygame.draw.rect(screen, RED, defeat_box, 4, border_radius=20)
            
            # Tech decoration
            for i in range(0, 560, 25):
                pygame.draw.line(screen, (RED, 50), (WIDTH//2 - 280 + i, 120), (WIDTH//2 - 280 + i + 12, 120), 1)
                pygame.draw.line(screen, (RED, 50), (WIDTH//2 - 280 + i, 600), (WIDTH//2 - 280 + i + 12, 600), 1)
            
            # Defeat text - glitchy
            glitch = random.randint(-2, 2) if random.random() < 0.2 else 0
            lose_text = font_title.render(">> SYSTEM FAILURE <<", True, RED)
            screen.blit(lose_text, (WIDTH // 2 - lose_text.get_width() // 2 + glitch, 150))
            
            # Subtitle
            sub_text = font_large.render("CONNECTION TERMINATED", True, DARK_RED)
            screen.blit(sub_text, (WIDTH // 2 - sub_text.get_width() // 2, 200))
            
            # Score display - tech panel
            score_box = pygame.Rect(WIDTH//2 - 180, 260, 360, 100)
            pygame.draw.rect(screen, (30, 25, 35), score_box, border_radius=10)
            pygame.draw.rect(screen, RED, score_box, 2, border_radius=10)
            score_label = font_medium.render(">> FINAL SCORE <<", True, LIGHT_GRAY)
            screen.blit(score_label, (WIDTH // 2 - score_label.get_width() // 2, 275))
            score_text = font_large.render(f"{game.score}", True, RED)
            screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 310))
            
            # System message
            msg_box = pygame.Rect(WIDTH//2 - 220, 380, 440, 70)
            pygame.draw.rect(screen, (35, 25, 30), msg_box, border_radius=8)
            pygame.draw.rect(screen, (RED, 80), msg_box, 1, border_radius=8)
            roast_text = font_small.render(game.roast_message, True, YELLOW)
            screen.blit(roast_text, (WIDTH // 2 - roast_text.get_width() // 2, 405))
            
            # Restart hint - cyberpunk button
            restart_box = pygame.Rect(WIDTH//2 - 150, 480, 300, 50)
            pygame.draw.rect(screen, (30, 40, 35), restart_box, border_radius=8)
            pygame.draw.rect(screen, NEON_CYAN, restart_box, 2, border_radius=8)
            restart_text = font_medium.render("[ ENTER ] TO RETRY", True, WHITE)
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, 495))
        
        pygame.display.flip()
        if game.action_cooldown > 0:
            game.action_cooldown -= 1
        
        clock.tick(30)
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
