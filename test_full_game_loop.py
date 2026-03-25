#!/usr/bin/env python3
"""Full game loop test for Rubber Duck Roguelike"""

import os
import sys

os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

import pygame
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((1200, 800))

import importlib.util
spec = importlib.util.spec_from_file_location("game", "/Users/Suprasidh/opencode-projects/rubber_duck_roguelike/main.py")
game_module = importlib.util.module_from_spec(spec)

test_results = []
errors = []
warnings = []

def run_test(name, test_func):
    print(f"\n{name}...")
    try:
        result = test_func()
        test_results.append((name, result))
        return result
    except Exception as e:
        print(f"  ✗ EXCEPTION: {type(e).__name__}: {e}")
        errors.append(f"{name}: {type(e).__name__}: {e}")
        test_results.append((name, False))
        return False

def test_1_full_game_loop():
    """Test: Start game, fight enemies, advance floors, check flash effects"""
    try:
        spec.loader.exec_module(game_module)
        
        if not hasattr(game_module, 'Game'):
            print("  ✗ Game class not found")
            errors.append("Game class not found")
            return False
        
        game = game_module.Game()
        
        # Start game
        game.start_new_game()
        if game.game_state != "playing":
            print(f"  ✗ Game state is '{game.game_state}', expected 'playing'")
            errors.append(f"Game start: state = {game.game_state}")
            return False
        print("  ✓ Game started")
        
        # Get player
        player = game.player
        if not player:
            print("  ✗ Player not created")
            errors.append("Player not created")
            return False
        print(f"  ✓ Player created (HP: {player.hp})")
        
        # Check for floor
        if not hasattr(game, 'floor'):
            print("  ✗ floor attribute missing")
            errors.append("floor missing")
            return False
        
        original_floor = game.floor
        print(f"  ✓ On floor {original_floor}")
        
        # Check enemies exist
        if not hasattr(game, 'enemies') or not game.enemies:
            print("  ✗ No enemies spawned")
            errors.append("No enemies")
            return False
        print(f"  ✓ {len(game.enemies)} enemies spawned")
        
        # Test screen flash during combat
        effects = game_module.effects
        effects.add_screen_flash(game_module.RED, 10)
        effects.add_screen_flash(game_module.GREEN, 10)
        effects.add_screen_flash(game_module.BLUE, 10)
        
        # Update effects to ensure no crashes
        for _ in range(15):
            effects.update()
            try:
                effects.draw(screen)
            except Exception as e:
                print(f"  ✗ Screen flash draw crashed: {e}")
                errors.append(f"Screen flash draw: {e}")
                return False
        
        print("  ✓ Screen flash effects work without crash")
        
        # Kill all enemies to advance
        game.enemies = []
        
        # Check for floor transition logic
        if hasattr(game, 'advance_floor'):
            game.advance_floor()
            if game.floor > original_floor:
                print(f"  ✓ Advanced to floor {game.floor}")
            else:
                print(f"  ⚠ advance_floor didn't change floor")
                warnings.append("advance_floor didn't work")
        
        # Test more flash effects after floor change
        effects.add_screen_flash(game_module.PURPLE, 20)
        effects.add_screen_flash(game_module.CYAN, 10)
        
        for _ in range(25):
            effects.update()
            try:
                effects.draw(screen)
            except Exception as e:
                print(f"  ✗ Screen flash after floor advance crashed: {e}")
                errors.append(f"Screen flash post-floor: {e}")
                return False
        
        print("  ✓ Screen flash after floor advance works")
        
        # Simulate game over and restart
        player.hp = 0
        
        if hasattr(game, 'game_over'):
            game.game_over()
            if game.game_state == "game_over":
                print("  ✓ Game over state reached")
        
        # Restart from game over
        if hasattr(game, 'start_new_game'):
            game.start_new_game()
            if game.game_state == "playing":
                print("  ✓ Game restart works")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        errors.append(f"Full game loop: {type(e).__name__}: {e}")
        return False

def test_2_all_screen_flashes():
    """Test: Verify all screen flash calls don't crash"""
    try:
        spec.loader.exec_module(game_module)
        
        effects = game_module.effects
        
        # Test all color combinations used in the game
        test_colors = [
            game_module.RED, game_module.GREEN, game_module.BLUE,
            game_module.GOLD, game_module.PURPLE, game_module.CYAN,
            game_module.DARK_RED, game_module.DARK_GREEN,
        ]
        
        for color in test_colors:
            effects.add_screen_flash(color, 10)
        
        # Run through full duration
        for _ in range(20):
            effects.update()
            effects.draw(screen)
        
        print("  ✓ All screen flash color variants work")
        return True
        
    except Exception as e:
        print(f"  ✗ Error: {type(e).__name__}: {e}")
        errors.append(f"Screen flash variants: {type(e).__name__}: {e}")
        return False

def test_3_enemy_combat():
    """Test: Combat with enemies doesn't crash"""
    try:
        spec.loader.exec_module(game_module)
        
        game = game_module.Game()
        game.start_new_game()
        
        if not game.enemies:
            print("  ✗ No enemies")
            errors.append("No enemies for combat test")
            return False
        
        enemy = game.enemies[0]
        original_enemy_hp = enemy.hp
        
        # Player attacks enemy
        if hasattr(game, 'attack_enemy'):
            game.attack_enemy(0)
            
            if enemy.hp < original_enemy_hp:
                print(f"  ✓ Player can damage enemy")
            else:
                print("  ⚠ Enemy damage not applied")
                warnings.append("Enemy not taking damage")
        
        # Enemy attacks player
        player = game.player
        original_player_hp = player.hp
        
        if hasattr(game, 'enemy_attack_player'):
            game.enemy_attack_player(0)
            
            if player.hp < original_player_hp:
                print(f"  ✓ Enemy can damage player")
            else:
                print("  ⚠ Player damage not applied")
                warnings.append("Player not taking damage")
        
        # Verify effects system still works after combat
        effects = game_module.effects
        effects.add_screen_flash(game_module.RED, 5)
        effects.update()
        effects.draw(screen)
        
        print("  ✓ Combat effects work without crash")
        return True
        
    except Exception as e:
        print(f"  ✗ Error: {type(e).__name__}: {e}")
        errors.append(f"Combat test: {type(e).__name__}: {e}")
        return False

def main():
    print("=" * 60)
    print("Rubber Duck Roguelike - Full Game Loop Test")
    print("=" * 60)
    
    run_test("Test 1: Full Game Loop (start -> fight -> advance)", test_1_full_game_loop)
    run_test("Test 2: All Screen Flash Variants", test_2_all_screen_flashes)
    run_test("Test 3: Enemy Combat", test_3_enemy_combat)
    
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    
    passed = 0
    for name, result in test_results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {name}: {status}")
        if result:
            passed += 1
    
    print(f"\nTotal: {passed}/{len(test_results)} tests passed")
    
    if warnings:
        print("\nWarnings (non-critical):")
        for w in warnings:
            print(f"  ⚠ {w}")
    
    if errors:
        print("\nErrors found:")
        for err in errors:
            print(f"  ✗ {err}")
        return 1
    
    print("\n✓ All tests passed! No crashes or errors.")
    return 0

if __name__ == "__main__":
    sys.exit(main())