import minigrid
import numpy as np
import gymnasium as gym
from minigrid.wrappers import RGBImgPartialObsWrapper, ImgObsWrapper
import matplotlib.pyplot as plt

class BabyAI(gym.Env):
    def __init__(self, task, obs_key="image", act_key="action", size=(64, 64)):
        self._env = gym.make(f"{task}")
        self._env = RGBImgPartialObsWrapper(self._env, tile_size=8)
        self._env = ImgObsWrapper(self._env)
        self._obs_is_dict = hasattr(self._env.observation_space, "spaces")
        self._obs_key = obs_key
        self._act_key = act_key
        self._size = size
        self._gray = False

    def __getattr__(self, name):
        if name.startswith("__"):
            raise AttributeError(name)
        try:
            return getattr(self._env, name)
        except AttributeError:
            raise ValueError(name)

    @property
    def observation_space(self):
        if self._obs_is_dict:
            spaces = self._env.observation_space.spaces.copy()

        else:
            spaces = {self._obs_key: self._env.observation_space}
        return gym.spaces.Dict(
            {
                **spaces,
                "is_first": gym.spaces.Box(0, 1, (), dtype=bool),
                "is_last": gym.spaces.Box(0, 1, (), dtype=bool),
                "is_terminal": gym.spaces.Box(0, 1, (), dtype=bool),
            }
        )


    @property
    def action_space(self):
        space = self._env.action_space
        space.discrete = True
        return space



    def step(self, action):
        obs, reward, terminated, truncated, info = self._env.step(action)
        if not self._obs_is_dict:
            obs = {self._obs_key: obs}
        obs["is_first"] = False
        obs["is_last"] = terminated or truncated
        obs["is_terminal"] = terminated
        done = terminated or truncated
        return obs, reward, done, info


    def reset(self):
        obs, info = self._env.reset()
        if not self._obs_is_dict:
            obs = {self._obs_key: obs}
        obs["is_first"] = True
        obs["is_last"] = False
        obs["is_terminal"] = False
        return obs



