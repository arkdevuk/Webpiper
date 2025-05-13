import wave
import audioop
from pathlib import Path

def to_portable_file(input_path: Path, output_path: Path) -> None:
    """
    Converts a WAV file to 16-bit mono.
    Args:
        input_path (Path): Path to the input WAV file.
        output_path (Path): Path where the converted WAV file will be saved.
    """
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    with wave.open(str(input_path), 'rb') as wf:
        params = wf.getparams()
        nchannels, sampwidth, framerate, nframes, comptype, compname = params

        print(f"Original: Channels={nchannels}, SampleWidth={sampwidth*8}bit, FrameRate={framerate}, Frames={nframes}")

        frames = wf.readframes(nframes)

        # Convert to mono if stereo
        if nchannels != 1:
            frames = audioop.tomono(frames, sampwidth, 0.5, 0.5)
            nchannels = 1

        # Convert to 16-bit sample width if needed
        if sampwidth != 2:
            frames = audioop.lin2lin(frames, sampwidth, 2)
            sampwidth = 2

    # Write the new WAV file
    with wave.open(str(output_path), 'wb') as wf_out:
        wf_out.setnchannels(nchannels)
        wf_out.setsampwidth(sampwidth)
        wf_out.setframerate(framerate)
        wf_out.writeframes(frames)

    print(f"Converted to 16-bit mono: {output_path}")

