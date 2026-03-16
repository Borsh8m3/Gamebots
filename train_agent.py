import os
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import CheckpointCallback
from agent import BBTAN

os.makedirs("models", exist_ok=True)

if __name__ == "__main__":
    print("Inicjalizacja środowiska...")
    env = BBTAN(render_mode=False)
    
    model = PPO("MlpPolicy", env, verbose=1, tensorboard_log="./ppo_bbtan_tensorboard/")
    TIMESTEPS = 100000 
    
    # 1. Autozapis: Tworzymy callback, który co 10 000 kroków zapisze model do folderu 'models'
    # Dzięki temu nawet jeśli odetną prąd, masz kopię zapasową!
    checkpoint_callback = CheckpointCallback(
        save_freq=10000, 
        save_path='./models/',
        name_prefix='bbtan_checkpoint'
    )
    
    print(f"Rozpoczynam trening na {TIMESTEPS} kroków...")
    
    # 2. Zabezpieczenie przed przerwaniem (try/except)
    try:
        # Dodajemy nasz callback do funkcji uczącej
        model.learn(total_timesteps=TIMESTEPS, callback=checkpoint_callback)
    except KeyboardInterrupt:
        # Ten blok wykona się, gdy wciśniesz Ctrl+C w terminalu
        print("\nTrening przerwany przez użytkownika (Ctrl+C)!")
        print("Nie martw się, zapisuję obecny stan mózgu agenta...")
    finally:
        # Ten blok wykona się zawsze na samym końcu (czy przerwano, czy skończono normalnie)
        model_path = "models/ppo_bbtan_model"
        model.save(model_path)
        print(f"Ostateczny model bezpiecznie zapisany w {model_path}.zip")
        env.close()