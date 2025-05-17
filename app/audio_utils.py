import wave
import audioop
from pathlib import Path

def to_portable_file(input_path: Path, output_path: Path) -> None:
    """
    Converts a WAV file to mono, 16-bit, 48kHz.
    Args:
        input_path (Path): Path to the input WAV file.
        output_path (Path): Path where the converted WAV file will be saved.
    """
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    with wave.open(str(input_path), 'rb') as wf:
        nchannels, sampwidth, framerate, nframes, _, _ = wf.getparams()
        frames = wf.readframes(nframes)

        print(f"Original: Channels={nchannels}, SampleWidth={sampwidth*8}bit, FrameRate={framerate}, Frames={nframes}")

        # Convert to mono
        if nchannels != 1:
            frames = audioop.tomono(frames, sampwidth, 0.5, 0.5)
            nchannels = 1

        # Convert to 16-bit
        if sampwidth != 2:
            frames = audioop.lin2lin(frames, sampwidth, 2)
            sampwidth = 2

        # Resample to 48kHz if needed
        target_rate = 48000
        if framerate != target_rate:
            frames, _ = audioop.ratecv(frames, sampwidth, nchannels, framerate, target_rate, None)
            framerate = target_rate

    # Write converted WAV
    with wave.open(str(output_path), 'wb') as wf_out:
        wf_out.setnchannels(1)
        wf_out.setsampwidth(2)
        wf_out.setframerate(48000)
        wf_out.writeframes(frames)

    print(f"Converted to 48kHz, 16-bit mono WAV: {output_path}")
