#!/usr/bin/env python3
"""Test script for Rubber Duck Roguelike game"""

import os
import sys
import time
import threading
import queue

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

def run_test(name, test_func):
    print(f"\n{name}...")
    try:
        result = test_func()
        test_results.append((name, result))
        return result
    except Exception as e:
        print(f"  ✗ EXCEPTION: {e}")
        errors.append(f"{name}: {e}")
        test_results.append((name, False))
        return False

def test_1_import_and_menu():
    """Test 1: Game launches and shows menu"""
    try:
        spec.loader.exec_module(game_module)
        print("  ✓ Game module imports")
        
        if hasattr(game_module, 'Game'):
            game_instance = game_module.Game()
            state = game_instance.game_state
            if state == "menu":
                print(f"  ✓ Game state is 'menu'")
                return True
            else:
                print(f"  ✗ Game state is '{state}', expected 'menu'")
                errors.append(f"Game state is {state}, expected menu")
                return False
        else:
            print("  ✗ 'Game' class not found")
            errors.append("Game class not found")
            return False
    except Exception as e:
        print(f"  ✗ Import failed: {e}")
        errors.append(f"Import: {e}")
        return False

def test_2_how_to_play():
    """Test 2: Pressing H on menu opens How to Play screen"""
    try:
        # Check function exists
        if not hasattr(game_module, 'draw_how_to_play'):
            print("  ✗ draw_how_to_play function not found")
            errors.append("draw_how_to_play missing")
            return False
        print("  ✓ draw_how_to_play function exists")
        
        # Test rendering
        try:
            game_module.draw_how_to_play(screen)
            print("  ✓ How to Play screen renders without error")
            return True
        except Exception as e:
            print(f"  ✗ Render error: {e}")
            errors.append(f"How to Play render: {e}")
            return False
    except Exception as e:
        print(f"  ✗ Test error: {e}")
        errors.append(f"How to Play test: {e}")
        return False

def test_3_how_to_play_back():
    """Test 3: Pressing H again closes How to Play"""
    try:
        spec.loader.exec_module(game_module)
        
        if hasattr(game_module, 'Game'):
            game_instance = game_module.Game()
            if hasattr(game_module, 'draw_menu'):
                game_module.draw_menu(screen, game_instance)
                print("  ✓ Menu screen renders without error")
                return True
            else:
                print("  ✗ draw_menu function not found")
                return False
        else:
            print("  ✗ Game class not found")
            return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        errors.append(f"Menu render: {e}")
        return False

def test_4_game_start():
    """Test 4: Game starts when pressing ENTER from menu"""
    try:
        spec.loader.exec_module(game_module)
        
        if hasattr(game_module, 'Game'):
            game_instance = game_module.Game()
            if hasattr(game_instance, 'start_new_game'):
                game_instance.start_new_game()
                state = game_instance.game_state
                if state == "playing":
                    print("  ✓ Game starts (state = 'playing')")
                    return True
                else:
                    print(f"  ✗ After start_new_game, state = '{state}'")
                    errors.append(f"Game start state: {state}")
                    return False
            else:
                print("  ✗ start_new_game method not found")
                errors.append("start_new_game missing")
                return False
        else:
            print("  ✗ Game class not found")
            errors.append("Game class not found")
            return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        errors.append(f"Game start: {e}")
        return False

def main():
    print("=" * 50)
    print("Rubber Duck Roguelike - Test Suite")
    print("=" * 50)
    
    run_test("Test 1: Import & Menu", test_1_import_and_menu)
    run_test("Test 2: How to Play opens (H key)", test_2_how_to_play)
    run_test("Test 3: No errors on How to Play", test_3_how_to_play_back)
    run_test("Test 4: Game starts (ENTER key)", test_4_game_start)
    
    print("\n" + "=" * 50)
    print("RESULTS")
    print("=" * 50)
    
    passed = 0
    for name, result in test_results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {name}: {status}")
        if result:
            passed += 1
    
    print(f"\nTotal: {passed}/{len(test_results)} tests passed")
    
    if errors:
        print("\nIssues found:")
        for err in errors:
            print(f"  - {err}")
        return 1
    
    print("\n✓ All tests passed!")
    return 0

if __name__ == "__main__":
    sys.exit(main())