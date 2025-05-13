import numpy as np
import math
import time

def apply_flanger(
    audio: np.ndarray,
    framerate: int,
    rate: float = 0.15,
    min_delay: float = 0.0025,
    max_delay: float = 0.0035,
    feedback: float = 0.9,
    t_offset: float = 0,
    t_offset_func=None,
    dry: float = 0.5,
    wet: float = 0.5
) -> np.ndarray:
    num_samples = len(audio)
    delay_buffer_size = int(max_delay * framerate) + 2
    delay_buffer = np.zeros(delay_buffer_size, dtype=np.float32)

    output = np.zeros(num_samples, dtype=np.float32)

    if t_offset_func is None:
        t_offset_func = lambda: time.time()

    for n in range(num_samples):
        lfo_phase = 2 * math.pi * rate * (n / framerate + t_offset + t_offset_func())
        delay_time = min_delay + (max_delay - min_delay) * (0.5 * (1 + math.sin(lfo_phase)))

        delay_samples = int(delay_time * framerate)

        # Circular buffer indices
        read_index = (n - delay_samples) % delay_buffer_size
        write_index = n % delay_buffer_size

        delayed_sample = delay_buffer[read_index]

        # Write current sample to buffer (with feedback)
        delay_buffer[write_index] = audio[n] + feedback * delayed_sample

        # Mix dry and wet signals
        output[n] = dry * audio[n] + wet * delayed_sample

    return output
