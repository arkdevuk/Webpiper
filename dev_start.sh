#!/bin/bash
# set current directory to CURRENT_DIR
CURRENT_DIR=$(cd "$(dirname "$0")" && pwd)
export OUTPUT_PATH=$CURRENT_DIR/output
export VOICE_PATH=$CURRENT_DIR/voice
# CD current directory && uvicorn server
cd $CURRENT_DIR/app  && uvicorn piper_tts_server:app --host 0.0.0.0 --port 8098
