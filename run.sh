#!/bin/bash
# Viral Video Lab — Workflow Runner
# Usage: ./run.sh [command]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Activate virtual environment if it exists
if [ -d "../youtube-autopilot/.venv" ]; then
    source ../youtube-autopilot/.venv/bin/activate
fi

# Add local bin to PATH
export PATH="$HOME/.local/bin:$PATH"

case "${1:-help}" in
    "daily")
        echo "🚀 Running daily workflow..."
        python3 workflow_orchestrator.py --mode=daily
        ;;
    "single")
        echo "🎬 Processing single video..."
        python3 workflow_orchestrator.py --mode=single
        ;;
    "test")
        echo "🧪 Running test workflow..."
        python3 workflow_orchestrator.py --mode=test
        ;;
    "post")
        echo "📤 Posting to social media..."
        python3 social_media_poster.py
        ;;
    "instructions")
        echo "📋 Generating upload instructions..."
        python3 social_media_poster.py --generate-instructions
        ;;
    "revenue")
        echo "💰 Tracking revenue..."
        python3 revenue_tracker.py --track
        ;;
    "report")
        echo "📊 Generating report..."
        python3 revenue_tracker.py --report "${2:-$(date +%Y-%m)}"
        ;;
    "payouts")
        echo "💸 Processing payouts..."
        python3 revenue_tracker.py --payouts "${2:-50}"
        ;;
    "config")
        echo "⚙️ Current configuration:"
        python3 config.py
        ;;
    "status")
        echo "📊 Workflow Status"
        echo "================="
        echo ""
        echo "📁 Queue:"
        ls -la queue/ 2>/dev/null | tail -5 || echo "  (empty)"
        echo ""
        echo "📤 Posted:"
        ls -la posted/ 2>/dev/null | tail -5 || echo "  (empty)"
        echo ""
        echo "💰 Revenue:"
        ls -la revenue/ 2>/dev/null | tail -5 || echo "  (empty)"
        ;;
    "help"|*)
        echo "Viral Video Lab — Workflow Runner"
        echo ""
        echo "Usage: ./run.sh [command]"
        echo ""
        echo "Commands:"
        echo "  daily        - Run daily automation workflow"
        echo "  single       - Process a single video"
        echo "  test         - Run test workflow"
        echo "  post         - Post videos to social media"
        echo "  instructions - Generate upload instructions"
        echo "  revenue      - Track revenue from platforms"
        echo "  report       - Generate monthly revenue report"
        echo "  payouts      - Process creator payouts"
        echo "  config       - Show current configuration"
        echo "  status       - Show workflow status"
        echo ""
        echo "Examples:"
        echo "  ./run.sh daily"
        echo "  ./run.sh report 2026-07"
        echo "  ./run.sh payouts 100"
        ;;
esac
