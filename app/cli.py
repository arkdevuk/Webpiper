import argparse
from tts import synthesize_text
from audio_utils import to_portable_file
from audio_file_utils import AudioFileUtils
from effects import flanger, normalize, pitch_shift
import json



def main():
    parser = argparse.ArgumentParser(description="Test TTS Synthesis with Piper")
    parser.add_argument("text", help="Text to synthesize")
    parser.add_argument("--local", default="fr_FR", help="Local voice file (default: fr_FR)")
    parser.add_argument("--voice", default="siwis-medium", help="Voice model (default: siwis-medium)")
    parser.add_argument("--silence", type=int, default=1, help="Silence length (default: 1)")
    parser.add_argument("--speed", type=float, default=1.0, help="Speech speed (default: 1.0)")
    parser.add_argument("--noise_w", type=float, default=0.8, help="Noise weight (default: 0.8)")
    # add a param --lite-file without value
    parser.add_argument("--lite-file", action='store_true', help="Convert to portable file format")
    # optionnal param of json data called --effects
    parser.add_argument("--effects", type=str, default=None, help="Effects to apply to the audio")

    args = parser.parse_args()

    try:
        output_file = synthesize_text(
            text=args.text,
            local=args.local,
            voice=args.voice,
            silence=args.silence,
            speed=args.speed,
            noise_w=args.noise_w
        )

        if args.effects:
            # transform the json data to a dict
            effects_data = json.loads(args.effects)
            # Check if the effects are valid
            if not isinstance(effects_data, dict):
                raise ValueError("Effects should be a JSON object")
            # Load the audio file
            audio, framerate =  AudioFileUtils.wav_to_audio(output_file)
            # Apply effects
            audio = flanger.apply_flanger(audio, framerate)
            audio = normalize.apply_normalize(audio, framerate)
            audio = pitch_shift.apply_pitch_shift(audio, framerate, pitch_change=35)

            # Save result
            AudioFileUtils.audio_to_wav(audio, framerate, output_file)

        if args.lite_file:
            to_portable_file(output_file, output_file)




        print(f"Audio file generated: {output_file}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
