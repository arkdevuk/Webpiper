#!/bin/bash
# set current directory to CURRENT_DIR
CURRENT_DIR=$(cd "$(dirname "$0")" && pwd)
echo export OUTPUT_PATH="$CURRENT_DIR/output"
echo export VOICE_PATH="$CURRENT_DIR/voices"
echo export VOICE_PATH="$CURRENT_DIR/chattervoices"
echo "Current directory: $CURRENT_DIR"
# CD current directory && uvicorn server
#cd $CURRENT_DIR/app  && uvicorn piper_tts_server:app --host 0.0.0.0 --port 8098

# docker build -t arkdevuk/webpiper:cuda-v1 .