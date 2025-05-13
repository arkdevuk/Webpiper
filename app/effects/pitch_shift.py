import numpy as np

def apply_pitch_shift(
    audio: np.ndarray,
    framerate: int,
    pitch_change: int = 0
) -> np.ndarray:
    """
    Applies a pitch shift to audio by resampling & time-stretching.
    Pure Python / numpy approximation.

    Args:
        audio (np.ndarray): Mono audio samples (float32).
        framerate (int): Sample rate (Hz).
        pitch_change (int): Pitch change -100 to +100. +100 = octave up, -100 = octave down.

    Returns:
        np.ndarray: Pitch shifted audio (same length).
    """
    if pitch_change == 0:
        return audio.copy()

    # Calculate pitch shift factor
    pitch_factor = 2 ** (pitch_change / 100.0)

    # Step 1: Resample to change pitch (and duration)
    input_len = len(audio)
    new_len = int(input_len / pitch_factor)

    # Simple linear interpolation resampling
    resampled_indices = np.linspace(0, input_len - 1, new_len)
    pitch_shifted_audio = np.interp(resampled_indices, np.arange(input_len), audio)

    # Step 2: Time-stretch back to original length using Overlap-Add (OLA)
    window_size = 2048
    hop_size = window_size // 4

    output_audio = np.zeros(input_len, dtype=np.float32)

    for i in range(0, input_len - window_size, hop_size):
        # Map output window to pitch-shifted audio window
        pos = int(i * new_len / input_len)

        if pos + window_size > len(pitch_shifted_audio):
            break

        # Simple windowing (optional: apply hanning window for smoothing)
        output_audio[i:i + window_size] += pitch_shifted_audio[pos:pos + window_size]

    # Normalize after OLA to avoid amplitude blow-up
    max_amp = np.max(np.abs(output_audio))
    if max_amp > 0:
        output_audio = output_audio * (np.max(np.abs(audio)) / max_amp)

    return output_audio
