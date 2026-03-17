import pandas as pd
import gymnasium as gym
from gymnasium import spaces
import numpy as np
import math
from game import BBTAN, COLS

def get_rainforce_agent_move(real_game, model, translator_env):
    raw_state = real_game._get_state() 
    obs = translator_env._format_state(raw_state)
    action, _ = model.predict(obs, deterministic=True)
    best_angle = float(action[0])
    return best_angle

def get_supervised_agent_move(real_game, sl_model):
    # 1. ZACZYNAMY od Start_X (jeśli w CSV była to pierwsza kolumna)
    # Kolejność w słowniku musi odpowiadać kolejności w X_train!
    board_state = {'Start_X': real_game.start_x}
    
    # 2. Dodajemy siatkę klocków R0_C0... R9_C6
    for r in range(10):
        for c in range(7):
            board_state[f'R{r}_C{c}'] = 0
            
    # 3. Wypełniamy HP klocków
    for b in real_game.blocks:
        if 0 <= b.row < 10 and 0 <= b.col < 7:
            board_state[f'R{b.row}_C{b.col}'] = b.hp
            
    # 4. Konwersja na DataFrame
    input_df = pd.DataFrame([board_state])
    
    # 5. KLUCZOWY MOMENT: Upewnij się, że kolumny są w tej samej kolejności co w modelu
    # sl_model.feature_names_in_ to lista nazw, których oczekuje model
    input_df = input_df[sl_model.feature_names_in_]
    
    # 6. Predykcja
    predicted_angle = sl_model.predict(input_df)[0]
    
    return predicted_angle
class BBTANGymEnv(gym.Env):
    
    def __init__(self, render_mode=True):
        super(BBTANGymEnv, self).__init__()
        self.game = BBTAN(render_mode=render_mode)
        
        min_angle = -math.pi * 170 / 180
        max_angle = -math.pi * 10 / 180
        self.action_space = spaces.Box(low=min_angle, high=max_angle, shape=(1,), dtype=np.float32)
        self.observation_space = spaces.Box(low=0, high=1000, shape=(72,), dtype=np.float32)

    def _format_state(self, state_dict):
        obs_list = []
        for row in state_dict["grid"]:
            obs_list.extend(row)
        obs_list.append(state_dict["start_x"])
        obs_list.append(state_dict["balls"])
        return np.array(obs_list, dtype=np.float32)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        raw_state = self.game.reset()
        return self._format_state(raw_state), {}

    def step(self, action):
        angle = action[0]
        raw_state, reward, done, info = self.game.step(angle)
        return self._format_state(raw_state), reward, done, False, info

    def close(self):
        self.game.close()