#!/bin/bash
# Quick status check

echo "📊 Viral Video Lab — Status"
echo "==========================="
echo ""

echo "📁 Output files:"
ls -la output/ 2>/dev/null | tail -5 || echo "  (none)"
echo ""

echo "📤 Queue (ready to upload):"
ls -la queue/*.json 2>/dev/null | wc -l || echo "  0 files"
echo ""

echo "✅ Posted:"
ls -la posted/ 2>/dev/null | tail -5 || echo "  (none)"
echo ""

echo "💰 Revenue:"
ls -la revenue/ 2>/dev/null | tail -5 || echo "  (none)"
echo ""

echo "🤖 Cron Jobs:"
echo "  viral-video-lab-daily: 8:00 AM daily"
echo "  autonomous-video-dubbing: 9:00 AM daily"
