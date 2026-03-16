from stable_baselines3 import PPO
from agent import BBTAN

if __name__ == "__main__":
    print("Wczytywanie wytrenowanego modelu...")
    # Tutaj włączamy renderowanie, by widzieć grę
    env = BBTAN(render_mode=True)
    
    try:
        model = PPO.load("models/ppo_bbtan_model")
    except FileNotFoundError:
        print("Nie znaleziono pliku modelu! Najpierw uruchom train_rl.py")
        exit()

    episodes = 5 # Liczba gier do oceny performance'u
    
    for ep in range(episodes):
        obs, info = env.reset()
        done = False
        total_reward = 0
        
        while not done:
            # Model przewiduje najlepszą akcję na podstawie obserwacji planszy
            action, _states = model.predict(obs, deterministic=True)
            obs, reward, done, truncated, info = env.step(action)
            total_reward += reward
            
        # Info["score"] to poziom, do którego dotarł agent (zdefiniowany w game.py)
        print(f"Gra {ep+1} zakończona. Maksymalny poziom (LINE): {info.get('score', 0)} | Nagroda: {total_reward:.2f}")

    env.close()