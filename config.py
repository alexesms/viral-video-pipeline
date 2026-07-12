#!/usr/bin/env python3
"""
Configuration for Viral Video Lab Workflow
"""

import os
import json

# Paths
BASE_DIR = os.path.expanduser("~/viral-video-lab-workflow")
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")

# Default configuration
DEFAULT_CONFIG = {
    "workflow": {
        "mode": "daily",
        "max_videos_per_day": 3,
        "languages": ["vi", "zh", "ja", "ko", "es"],
        "platforms": ["youtube", "tiktok", "bilibili"]
    },
    "video": {
        "max_duration_seconds": 60,
        "resolution": "1080p",
        "format": "mp4"
    },
    "dubbing": {
        "tts_provider": "edge-tts",
        "default_voice": "en-US-GuyNeural",
        "voices": {
            "vi": "vi-VN-NamMinhNeural",
            "zh": "zh-CN-YunxiNeural",
            "ja": "ja-JP-KeitaNeural",
            "ko": "ko-KR-InJoonNeural",
            "es": "es-ES-AlvaroNeural",
            "pt": "pt-BR-AntonioNeural",
            "ar": "ar-SA-HamedNeural",
            "hi": "hi-IN-MadhurNeural",
            "fr": "fr-FR-HenriNeural",
            "de": "de-DE-ConradNeural"
        }
    },
    "revenue": {
        "creator_share": 0.30,
        "platform_share": 0.70,
        "minimum_payout": 50,
        "payout_frequency": "monthly"
    },
    "api_keys": {
        "openrouter": "",
        "elevenlabs": "",
        "sync_labs": ""
    }
}

def load_config():
    """Load configuration from file or create default"""
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH) as f:
            return json.load(f)
    
    # Create default config
    save_config(DEFAULT_CONFIG)
    return DEFAULT_CONFIG

def save_config(config):
    """Save configuration to file"""
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=2)

def update_config(key, value):
    """Update a specific config value"""
    config = load_config()
    
    # Support nested keys like "dubbing.tts_provider"
    keys = key.split('.')
    current = config
    for k in keys[:-1]:
        current = current[k]
    current[keys[-1]] = value
    
    save_config(config)
    return config

def get_config(key=None, default=None):
    """Get config value"""
    config = load_config()
    
    if key is None:
        return config
    
    # Support nested keys
    keys = key.split('.')
    current = config
    for k in keys:
        if isinstance(current, dict) and k in current:
            current = current[k]
        else:
            return default
    
    return current

def main():
    """Show current configuration"""
    config = load_config()
    print(json.dumps(config, indent=2))

if __name__ == "__main__":
    main()
