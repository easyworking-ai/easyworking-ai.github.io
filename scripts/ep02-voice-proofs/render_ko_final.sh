#!/bin/bash
set -e
cd /Users/macbook/easyworking-ai.github.io/scripts/ep02-voice-proofs

VOXCPM="/Users/macbook/.venvs/voxcpm2/bin/voxcpm"
IRO_CONTROL="A natural clear Korean female voice, late twenties, bright and clean tone, smooth conversational delivery like talking naturally to a friend, relaxed pace with organic pauses, crisp pronunciation, studio quality recording, no breathiness, no muffle, no noise"
LOOP_CONTROL="A polished Korean male voice, calm and trustworthy, well-modulated radio host delivery, smooth and even, clean diction, moderate pace, professional broadcast quality, reassuring and competent"

echo "=== Rendering KO IRO final (15 lines) ==="
mkdir -p ko_iro_final
$VOXCPM batch \
  --input iro_lines_final.txt \
  --output-dir ko_iro_final \
  --control "$IRO_CONTROL" \
  --cfg-value 2.0 \
  --inference-timesteps 30 \
  --normalize \
  --denoise

echo "=== Rendering KO LOOP final (15 lines) ==="
mkdir -p ko_loop_final
$VOXCPM batch \
  --input loop_lines_final.txt \
  --output-dir ko_loop_final \
  --control "$LOOP_CONTROL" \
  --cfg-value 2.0 \
  --inference-timesteps 30 \
  --normalize \
  --denoise

echo "=== KO final batch done ==="
ls -la ko_iro_final/ ko_loop_final/
