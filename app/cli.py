import argparse
import time

from chatter import ChatterWrapper
from tts import synthesize_text
from audio_utils import to_portable_file
from audio_file_utils import AudioFileUtils
from effects.chain_processor import EffectChainProcessor
import json

def main():
    parser = argparse.ArgumentParser(description="Test TTS Synthesis with Piper")
    parser.add_argument("text", help="Text to synthesize")

    parser.add_argument("--model", default="piper", help="Model used to generate audio (default: Piper) - options: piper, chatterbox")

    # parameters  for Piper
    parser.add_argument("--local", default="fr_FR", help="Local voice file (default: fr_FR)")
    parser.add_argument("--voice", default="siwis-medium", help="Voice model (default: siwis-medium)")
    parser.add_argument("--silence", type=int, default=1, help="Silence length (default: 1)")
    parser.add_argument("--speed", type=float, default=1.0, help="Speech speed (default: 1.0)")
    parser.add_argument("--noise_w", type=float, default=0.8, help="Noise weight (default: 0.8)")


    # parameters for Chatterbox exaggeration float 0-1 (default: 0.5), cfg_weight float 0-1 (default: 0.5), prompt string (default: None)
    parser.add_argument("--exaggeration", type=float, default=0.5, help="Exaggeration factor (default: 0.5)")
    parser.add_argument("--cfg_weight", type=float, default=0.5, help="CFG weight (default: 0.5)")
    parser.add_argument("--prompt", type=str, default=None, help="Prompt for Chatterbox (default: None) - Value must be a path to a wav file.")

    # add a param --lite-file without value
    parser.add_argument("--lite-file", action='store_true', help="Convert to portable file format")
    # optionnal param of json data called --effects
    parser.add_argument("--effects", type=str, default=None, help="Effects to apply to the audio")


    args = parser.parse_args()

    try:
        if args.model == "chatterbox":
            # generate random file name
            chatter_wrapper = ChatterWrapper()
            output_file = chatter_wrapper.run_synchronously(
                text=args.text,
                exaggeration=args.exaggeration,
                cfg_weight=args.cfg_weight,
                voice=args.prompt
            )
        else:
            output_file = synthesize_text(
                text=args.text,
                local=args.local,
                voice=args.voice,
                silence=args.silence,
                speed=args.speed,
                noise_w=args.noise_w
            )

        if args.effects:
            # Parse effects JSON
            effects_data = json.loads(args.effects)
            if not isinstance(effects_data, list):
                raise ValueError("Effects should be a JSON array of effect steps")

            # Load audio
            audio, framerate = AudioFileUtils.wav_to_audio(output_file)

            # Process chain
            processor = EffectChainProcessor()
            audio = processor.apply_chain(audio, framerate, effects_data)

            # Save result
            AudioFileUtils.audio_to_wav(audio, framerate, output_file)

        if args.lite_file:
            to_portable_file(output_file, output_file)




        print(f"Audio file generated: {output_file}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
