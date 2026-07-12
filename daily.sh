#!/bin/bash
# Daily content generation - simplified
set -e

echo "🎬 Daily Content Generation"
echo "=========================="
echo ""

# Activate venv
source ~/youtube-autopilot/.venv/bin/activate
export PATH="$HOME/.local/bin:$PATH"

# Run the workflow
python3 workflow_orchestrator.py --mode=daily

echo ""
echo "✅ Done! Check queue/ for videos ready to upload"
echo ""
echo "Next steps:"
echo "1. Review videos in queue/"
echo "2. Upload to YouTube, TikTok, Bilibili"
echo "3. Track views and revenue"
