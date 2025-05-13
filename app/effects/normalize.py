import numpy as np


def apply_normalize(
        audio: np.ndarray,
        framerate: int,
        max_amplitude: float = 32767.0  # PCM 16-bit peak
) -> np.ndarray:
    """
    Normalizes audio by removing DC offset and scaling to target amplitude.

    Args:
        audio (np.ndarray): Input audio signal (float32 array, raw PCM range [-32768, 32767]).
        framerate (int): Sampling rate in Hz (unused but kept for API consistency).
        max_amplitude (float): Target peak amplitude (default: 32767.0 for PCM 16-bit).

    Returns:
        np.ndarray: Normalized audio signal.
    """
    # Remove DC offset
    mean_value = np.mean(audio)
    audio_centered = audio - mean_value

    # Avoid divide-by-zero for silent signals
    current_peak = np.max(np.abs(audio_centered))
    if current_peak < 1e-9:
        return audio_centered  # Already silence

    # Scale to desired peak amplitude
    scaling_factor = max_amplitude / current_peak
    normalized_audio = audio_centered * scaling_factor

    return normalized_audio
