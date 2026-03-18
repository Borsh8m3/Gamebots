import os
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import CheckpointCallback
from agent import BBTANGymEnv 

if __name__ == "__main__":
    env = BBTANGymEnv(render_mode=False)
    
    # 1. Ładujemy istniejący mózg z pliku .zip
    # Ważne: musimy mu od razu przypisać środowisko (env=env)
    model_path = "models/ppo_bbtan_model" # bez .zip na końcu, biblioteka sama to ogarnie
    
    print(f"Wczytywanie starego modelu z {model_path}.zip...")
    model = PPO.load(model_path, env=env, tensorboard_log="./ppo_bbtan_tensorboard/")
    
    TIMESTEPS = 20000 # Ile KOLEJNYCH kroków chcemy go douczyć
    
    checkpoint_callback = CheckpointCallback(
        save_freq=5000, 
        save_path='./models/',
        name_prefix='bbtan_checkpoint_v2' # Zmieniamy nazwę, żeby odróżnić nowe checkpointy
    )
    
    print(f"Wznawiam trening na kolejne {TIMESTEPS} kroków...")
    
    try:
        # 2. Po prostu wywołujemy learn() jeszcze raz!
        # reset_num_timesteps=False sprawi, że w TensorBoardzie wykresy będą 
        # ładnie kontynuowane, a nie zaczną się od zera.
        model.learn(total_timesteps=TIMESTEPS, callback=checkpoint_callback, reset_num_timesteps=False)
    except KeyboardInterrupt:
        print("\nPrzerwano! Zapisuję obecny stan...")
    finally:
        # 3. Zapisujemy zaktualizowany model (możesz nadpisać stary, ale bezpieczniej dodać dopisek v2)
        new_model_path = "models/ppo_bbtan_model_v2"
        model.save(new_model_path)
        print(f"Douczony model zapisano w {new_model_path}.zip")
        env.close()