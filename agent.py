import gymnasium as gym
from gymnasium import spaces
import numpy as np
import math
from game import BBTAN, COLS

class BBTANGymEnv(gym.Env):
    """Opakowanie Gymnasium dla gry BBTAN"""
    
    def __init__(self, render_mode=True):
        super(BBTANGymEnv, self).__init__()
        # Tutaj przekazujemy render_mode do samej gry
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