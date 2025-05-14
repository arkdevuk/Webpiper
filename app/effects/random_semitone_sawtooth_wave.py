import numpy as np
from dataclasses import dataclass, field
from random import Random

def sawtooth_wave(radians: np.ndarray) -> np.ndarray:
    """
    Pure numpy sawtooth wave equivalent to scipy.signal.sawtooth.
    """
    return 2 * (radians / (2 * np.pi) - np.floor(0.5 + radians / (2 * np.pi)))

@dataclass
class RandomSemitoneSawtoothWave:
    min_freq: float
    max_semitones: int
    pitch_duration: float
    wet: float = 0.5  # Wet mix level (0 to 1)
    rng: Random = field(default_factory=Random)

    def generate_modulation(self, length: int, framerate: int) -> np.ndarray:
        times = np.arange(length) / framerate
        dt = times[1] - times[0]
        chunk_size = round(self.pitch_duration / dt)

        modulation = np.zeros_like(times, dtype=np.float32)

        for i in range(0, len(times), chunk_size):
            semitones = self.rng.randint(0, self.max_semitones)
            freq = self.min_freq * 2 ** (semitones / 12)

            time_chunk = times[i:i + chunk_size]
            radians = 2 * np.pi * freq * time_chunk
            modulation[i:i + chunk_size] = sawtooth_wave(radians)

        return modulation

    def apply(self, audio: np.ndarray, framerate: int) -> np.ndarray:
        modulation = self.generate_modulation(len(audio), framerate)

        # Apply as amplitude modulation, scaled by wet
        modulated_audio = (audio * modulation * self.wet) + (audio * (1 - self.wet))

        # Ensure float32 type to avoid overflow errors
        return modulated_audio.astype(np.float32)

def apply_effect(
    audio: np.ndarray,
    framerate: int,
    min_freq: float,
    max_semitones: int,
    pitch_duration: float,
    wet: float = 0.5
) -> np.ndarray:
    """
    Apply RandomSemitoneSawtoothWave modulation with dry/wet mix.

    Args:
        audio (np.ndarray): Input audio.
        framerate (int): Sample rate.
        min_freq (float): Base frequency.
        max_semitones (int): Random semitone range.
        pitch_duration (float): Duration of each pitch step.
        wet (float): Wet mix level (0-1).

    Returns:
        np.ndarray: Modulated audio.
    """
    effect = RandomSemitoneSawtoothWave(
        min_freq=min_freq,
        max_semitones=max_semitones,
        pitch_duration=pitch_duration,
        wet=wet
    )
    return effect.apply(audio, framerate)
