import numpy as np

def apply_speed_change(
    audio: np.ndarray,
    framerate: int,
    speed: float = 0.0
) -> np.ndarray:
    """
    Changes the playback speed of the audio.

    Args:
        audio (np.ndarray): Mono audio samples.
        framerate (int): Sample rate (Hz).
        speed (float): Speed change factor:
            - 0.0 = no change
            - positive = faster (e.g., 0.25 = 25% faster)
            - negative = slower (e.g., -0.25 = 25% slower)

    Returns:
        np.ndarray: Speed-adjusted audio (duration changes with speed).
    """
    if speed == 0.0:
        return audio.copy()

    # Compute speed factor
    speed_factor = 1.0 + speed
    if speed_factor <= 0:
        raise ValueError("Speed factor must be > 0")

    original_indices = np.arange(len(audio))
    new_length = int(len(audio) / speed_factor)
    new_indices = np.linspace(0, len(audio) - 1, new_length)

    # Interpolate to get new audio
    stretched_audio = np.interp(new_indices, original_indices, audio)

    return stretched_audio.astype(np.float32)
