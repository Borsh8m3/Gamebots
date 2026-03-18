import pygame
import math
from game import BBTAN, Block

def get_aimbot_move(real_game):
    """
    Aimbot symuluje opcje (co 5 stopni) i zwraca najlepszy kąt.
    """
    best_angle = -math.pi / 2
    max_reward = -float('inf')

    for deg in range(15, 166, 5):
        test_angle_rad = -math.pi * deg / 180.0
        
        sim = BBTAN(render_mode=False)
        sim.level = real_game.level
        sim.max_balls = real_game.max_balls
        sim.start_x = real_game.start_x
        sim.start_y = real_game.start_y
        sim.done = real_game.done
        
        sim.blocks = []
        for b in real_game.blocks:
            new_b = Block(b.col, b.row, b.hp)
            new_b.rect.x = b.rect.x
            new_b.rect.y = b.rect.y
            sim.blocks.append(new_b)
            
        _, reward, _, _ = sim.step(test_angle_rad)
        
        # best shot
        if reward > max_reward:
            max_reward = reward
            best_angle = test_angle_rad
            
    return best_angle

def play() -> None:
    print("Uruchamianie Aimbota...")
    
    game = BBTAN(render_mode=True)
    done = False
    
    while not done:
        best_angle = get_aimbot_move(game)
        
        end_x = game.start_x + math.cos(best_angle) * 150
        end_y = game.start_y + math.sin(best_angle) * 150
        pygame.draw.line(game.screen, (0, 255, 0), (game.start_x, game.start_y), (end_x, end_y), 3)
        pygame.display.flip()
        
        # shot
        state, reward, done, info = game.step(best_angle)
        
        print(f"Linia: {game.level - 1} | Oddano strzał pod kątem: {math.degrees(best_angle):.1f}°")

    print(f"\nGra zakończona! Aimbot dotarł do {game.level - 1} poziomu.")
    game.close()