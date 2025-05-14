import numpy as np
from typing import List, Dict, Any
from .flanger import apply_flanger
from .normalize import apply_normalize
from .pitch_shift import apply_pitch_shift
from .random_semitone_sawtooth_wave import apply_effect


class EffectChainProcessor:
    def __init__(self):
        # Mapping from effect name to its corresponding module & function
        self.effect_map = {
            "flanger": apply_flanger,
            "normalize": apply_normalize,
            "pitch_shift": apply_pitch_shift,
            "random_semitone_sawtooth_wave": apply_effect,
        }

    def apply_chain(self, audio: np.ndarray, framerate: int, chain: List[Dict[str, Any]]) -> np.ndarray:
        """
        Applies a sequence of effects to audio.

        Args:
            audio (np.ndarray): Input audio signal.
            framerate (int): Sample rate in Hz.
            chain (List[Dict]): List of effect dicts with 'name' and 'params'.

        Returns:
            np.ndarray: Processed audio.
        """
        for effect_conf in chain:
            effect_name = effect_conf.get("name")
            params = effect_conf.get("params", {})

            if effect_name not in self.effect_map:
                raise ValueError(f"Unknown effect: {effect_name}")

            effect_func = self.effect_map[effect_name]

            print(f"Applying effect: {effect_name} with params {params}")
            audio = effect_func(audio, framerate, **params)

        return audio
