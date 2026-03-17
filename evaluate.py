import pygame
import math
import numpy as np
import matplotlib.pyplot as plt
from stable_baselines3 import PPO

from agent import BBTANGymEnv
from game import BBTAN, Block

def get_aimbot_prediction(real_game):
    """Aimbot symuluje opcje i zwraca najlepszy kąt oraz spodziewaną nagrodę."""
    best_angle = -math.pi / 2
    max_reward = -float('inf')

    # Testujemy kąty co 5 stopni
    for deg in range(15, 166, 5):
        test_angle_rad = -math.pi * deg / 180.0
        
        sim = BBTAN(render_mode=False)
        sim.level = real_game.level
        sim.max_balls = real_game.max_balls
        sim.start_x = real_game.start_x
        sim.start_y = real_game.start_y
        sim.done = real_game.done
        
        # Kopiowanie klocków
        sim.blocks = []
        for b in real_game.blocks:
            new_b = Block(b.col, b.row, b.hp)
            new_b.rect.x = b.rect.x
            new_b.rect.y = b.rect.y
            sim.blocks.append(new_b)
            
        _, reward, _, _ = sim.step(test_angle_rad)
        
        if reward > max_reward:
            max_reward = reward
            best_angle = test_angle_rad
            
    return best_angle, max_reward

def draw_aim_lines(game, aimbot_angle, agent_angle):
    """Rysuje linie celowania Aimbota (zielona) i Agenta (czerwona)."""
    # Wymuszamy narysowanie czystej klatki bez poruszających się kulek
    game._render_frame(balls=[])
    
    start_x, start_y = game.start_x, game.start_y
    line_length = 200
    
    # Rysuj linię Aimbota (Idealna - Zielona)
    aimbot_end_x = start_x + math.cos(aimbot_angle) * line_length
    aimbot_end_y = start_y + math.sin(aimbot_angle) * line_length
    pygame.draw.line(game.screen, (0, 255, 0), (start_x, start_y), (aimbot_end_x, aimbot_end_y), 3)
    
    # Rysuj linię Agenta RL (Rzeczywista - Czerwona)
    agent_end_x = start_x + math.cos(agent_angle) * line_length
    agent_end_y = start_y + math.sin(agent_angle) * line_length
    pygame.draw.line(game.screen, (255, 0, 0), (start_x, start_y), (agent_end_x, agent_end_y), 3)
    
    pygame.display.flip()
    # Zatrzymujemy grę na 0.5 sekundy, żebyś mógł na własne oczy porównać strzały
    pygame.time.delay(500)

if __name__ == "__main__":
    print("Wczytywanie modelu i środowiska...")
    env = BBTANGymEnv(render_mode=True)
    
    try:
        model = PPO.load("models/ppo_bbtan_model")
    except FileNotFoundError:
        print("Nie znaleziono modelu! Najpierw uruchom train_rl.py na jakiś czas.")
        exit()

    # Listy do zbierania statystyk
    angle_deviations = []
    score_deviations = []

    obs, info = env.reset()
    done = False
    turn_number = 1

    print("Rozpoczynam starcie AI vs Aimbot!")

    while not done:
        # 1. Aimbot myśli
        aimbot_angle, aimbot_expected_reward = get_aimbot_prediction(env.game)
        
        # 2. Agent myśli
        action, _states = model.predict(obs, deterministic=True)
        agent_angle = action[0]
        
        # 3. Pokazujemy strzał na ekranie (Zielona vs Czerwona linia)
        draw_aim_lines(env.game, aimbot_angle, agent_angle)
        
        # 4. Agent oddaje strzał!
        obs, agent_reward, done, truncated, info = env.step(action)
        
        # 5. Obliczamy odchylenia
        angle_diff_deg = abs(math.degrees(aimbot_angle) - math.degrees(agent_angle))
        score_diff = aimbot_expected_reward - agent_reward
        
        angle_deviations.append(angle_diff_deg)
        score_deviations.append(score_diff)
        
        print(f"Tura {turn_number} | Błąd Kąta: {angle_diff_deg:.1f}° | Strata Punktów: {score_diff:.1f}")
        turn_number += 1

    env.close()

    # ==========================================
    # GENEROWANIE WYKRESÓW W MATPLOTLIB
    # ==========================================
    print("\nGra zakończona! Generuję raport z odchyleniami...")
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    # Wykres 1: Odchylenie kąta
    ax1.plot(angle_deviations, color='red', marker='o', linestyle='-')
    ax1.set_title("Odchylenie wyboru AI od Aimbota w stopniach (°)")
    ax1.set_ylabel("Błąd kąta (°)")
    ax1.set_xlabel("Numer tury")
    ax1.grid(True)
    
    # Wykres 2: Utracone punkty
    ax2.plot(score_deviations, color='orange', marker='x', linestyle='--')
    ax2.set_title("Strata punktowa (Ile punktów więcej zyskałby Aimbot)")
    ax2.set_ylabel("Utracone punkty HP")
    ax2.set_xlabel("Numer tury")
    ax2.grid(True)
    
    plt.tight_layout()
    plt.show()