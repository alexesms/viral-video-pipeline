#!/usr/bin/env python3
"""
Social Media Posting Automation
Posts dubbed videos to YouTube, TikTok, Bilibili, etc.
"""

import os
import json
import requests
from datetime import datetime
from pathlib import Path

# Platform configurations
PLATFORMS = {
    "youtube": {
        "name": "YouTube",
        "api_base": "https://www.googleapis.com/youtube/v3",
        "upload_url": "https://www.googleapis.com/upload/youtube/v3/videos",
        "max_size_gb": 128,
        "formats": ["mp4", "mov", "avi"],
        "requirements": {
            "subscribers": 0,  # No minimum for uploading
            "watch_hours": 0,  # No minimum for uploading
            "monetization": {"subscribers": 1000, "watch_hours": 4000}
        }
    },
    "tiktok": {
        "name": "TikTok",
        "api_base": "https://open.tiktokapis.com/v2",
        "max_size_gb": 4,
        "formats": ["mp4", "mov"],
        "requirements": {
            "followers": 0,
            "monetization": {"followers": 10000, "views_30d": 100000}
        }
    },
    "bilibili": {
        "name": "Bilibili",
        "api_base": "https://member.bilibili.com/x/vu/client",
        "max_size_gb": 8,
        "formats": ["mp4", "flv", "avi"],
        "requirements": {
            "fans": 0,
            "monetization": {"fans": 1000, "views": 100000}
        }
    },
    "douyin": {
        "name": "Douyin",
        "api_base": "https://open.douyin.com/api",
        "max_size_gb": 4,
        "formats": ["mp4", "mov"],
        "requirements": {
            "followers": 0,
            "monetization": {"followers": 10000}
        }
    },
    "instagram": {
        "name": "Instagram Reels",
        "api_base": "https://graph.instagram.com/v18.0",
        "max_size_gb": 4,
        "formats": ["mp4", "mov"],
        "requirements": {
            "followers": 0,
            "monetization": "invite_only"
        }
    }
}

class SocialMediaPoster:
    def __init__(self):
        self.queue_dir = os.path.expanduser("~/viral-video-lab-workflow/queue")
        self.posted_dir = os.path.expanduser("~/viral-video-lab-workflow/posted")
        self.credentials = self.load_credentials()
    
    def load_credentials(self):
        """Load platform credentials from config"""
        config_path = os.path.expanduser("~/viral-video-lab-workflow/credentials.json")
        
        if os.path.exists(config_path):
            with open(config_path) as f:
                return json.load(f)
        
        # Return empty credentials
        return {
            "youtube": {"api_key": "", "channel_id": ""},
            "tiktok": {"access_token": ""},
            "bilibili": {"sessdata": "", "bili_jct": ""},
            "douyin": {"access_token": ""},
            "instagram": {"access_token": "", "user_id": ""}
        }
    
    def save_credentials(self):
        """Save credentials to config"""
        config_path = os.path.expanduser("~/viral-video-lab-workflow/credentials.json")
        with open(config_path, 'w') as f:
            json.dump(self.credentials, f, indent=2)
    
    def get_pending_posts(self):
        """Get videos ready for posting"""
        pending = []
        
        if not os.path.exists(self.queue_dir):
            return pending
        
        for json_file in Path(self.queue_dir).glob("*.json"):
            with open(json_file) as f:
                metadata = json.load(f)
            
            if metadata.get('status') == 'ready':
                pending.append({
                    "metadata": metadata,
                    "metadata_path": str(json_file)
                })
        
        return pending
    
    def post_to_all_platforms(self, metadata):
        """Post video to all configured platforms"""
        results = {}
        
        for platform in metadata.get('platforms', []):
            if platform in PLATFORMS:
                print(f"  📤 Posting to {PLATFORMS[platform]['name']}...")
                
                result = self.post_to_platform(platform, metadata)
                results[platform] = result
                
                if result['success']:
                    print(f"    ✓ Posted: {result.get('url', 'N/A')}")
                else:
                    print(f"    ✗ Failed: {result.get('error', 'Unknown')}")
        
        return results
    
    def post_to_platform(self, platform, metadata):
        """Post video to a specific platform"""
        platform_config = PLATFORMS.get(platform, {})
        
        # Check if we have credentials
        if not self.credentials.get(platform, {}).get('api_key') and \
           not self.credentials.get(platform, {}).get('access_token'):
            return {
                "success": False,
                "error": f"No credentials for {platform}",
                "action": "manual_upload"
            }
        
        # Platform-specific posting logic
        if platform == "youtube":
            return self.post_to_youtube(metadata)
        elif platform == "tiktok":
            return self.post_to_tiktok(metadata)
        elif platform == "bilibili":
            return self.post_to_bilibili(metadata)
        elif platform == "douyin":
            return self.post_to_douyin(metadata)
        elif platform == "instagram":
            return self.post_to_instagram(metadata)
        else:
            return {"success": False, "error": f"Unknown platform: {platform}"}
    
    def post_to_youtube(self, metadata):
        """Post to YouTube using YouTube Data API v3"""
        # This would require OAuth2 authentication
        # For now, return manual upload instructions
        
        return {
            "success": False,
            "error": "YouTube API requires OAuth2 setup",
            "action": "manual_upload",
            "instructions": {
                "url": "https://studio.youtube.com",
                "title": metadata.get('title'),
                "description": metadata.get('description'),
                "tags": metadata.get('tags', []),
                "video_path": metadata.get('video_path')
            }
        }
    
    def post_to_tiktok(self, metadata):
        """Post to TikTok using TikTok Content Posting API"""
        # TikTok API requires OAuth2 and business account
        
        return {
            "success": False,
            "error": "TikTok API requires business account setup",
            "action": "manual_upload",
            "instructions": {
                "url": "https://www.tiktok.com/upload",
                "title": metadata.get('title'),
                "description": metadata.get('description'),
                "video_path": metadata.get('video_path')
            }
        }
    
    def post_to_bilibili(self, metadata):
        """Post to Bilibili using their API"""
        # Bilibili API requires login cookies
        
        return {
            "success": False,
            "error": "Bilibili API requires login cookies",
            "action": "manual_upload",
            "instructions": {
                "url": "https://member.bilibili.com/platform/upload/video/frame",
                "title": metadata.get('title'),
                "description": metadata.get('description'),
                "video_path": metadata.get('video_path')
            }
        }
    
    def post_to_douyin(self, metadata):
        """Post to Douyin using their API"""
        # Douyin API requires OAuth2
        
        return {
            "success": False,
            "error": "Douyin API requires OAuth2 setup",
            "action": "manual_upload",
            "instructions": {
                "url": "https://creator.douyin.com",
                "title": metadata.get('title'),
                "description": metadata.get('description'),
                "video_path": metadata.get('video_path')
            }
        }
    
    def post_to_instagram(self, metadata):
        """Post to Instagram using Instagram Graph API"""
        # Instagram API requires Facebook Business account
        
        return {
            "success": False,
            "error": "Instagram API requires Facebook Business setup",
            "action": "manual_upload",
            "instructions": {
                "url": "https://www.instagram.com/reels/create",
                "title": metadata.get('title'),
                "video_path": metadata.get('video_path')
            }
        }
    
    def generate_upload_instructions(self):
        """Generate step-by-step upload instructions for manual posting"""
        pending = self.get_pending_posts()
        
        if not pending:
            print("✅ No videos pending upload!")
            return
        
        instructions_path = os.path.join(self.posted_dir, f"upload_instructions_{datetime.now().strftime('%Y%m%d')}.md")
        
        with open(instructions_path, 'w') as f:
            f.write("# 📤 Upload Instructions\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
            f.write(f"**Videos to upload:** {len(pending)}\n\n")
            
            for item in pending:
                metadata = item['metadata']
                
                f.write(f"## {metadata.get('title', 'Untitled')}\n\n")
                f.write(f"**Language:** {metadata.get('language', 'unknown')}\n")
                f.write(f"**Video:** `{metadata.get('video_path', 'N/A')}`\n\n")
                
                f.write("### Platforms\n\n")
                for platform in metadata.get('platforms', []):
                    if platform in PLATFORMS:
                        f.write(f"#### {PLATFORMS[platform]['name']}\n")
                        f.write(f"1. Go to: {PLATFORMS[platform].get('upload_url', PLATFORMS[platform].get('api_base', ''))}\n")
                        f.write(f"2. Upload: `{metadata.get('video_path')}`\n")
                        f.write(f"3. Title: {metadata.get('title')}\n")
                        f.write(f"4. Description:\n```\n{metadata.get('description', '')}\n```\n")
                        f.write(f"5. Tags: {', '.join(metadata.get('tags', []))}\n\n")
                
                f.write("---\n\n")
        
        print(f"📄 Instructions saved: {instructions_path}")
        return instructions_path

def main():
    """Main function"""
    import sys
    
    poster = SocialMediaPoster()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--generate-instructions":
        poster.generate_upload_instructions()
    else:
        # Post all pending videos
        pending = poster.get_pending_posts()
        print(f"📤 Found {len(pending)} videos pending upload\n")
        
        for item in pending:
            metadata = item['metadata']
            print(f"🎬 {metadata.get('title', 'Untitled')}")
            
            results = poster.post_to_all_platforms(metadata)
            
            # Update status
            metadata['status'] = 'posted'
            metadata['posted_at'] = datetime.now().isoformat()
            metadata['results'] = results
            
            with open(item['metadata_path'], 'w') as f:
                json.dump(metadata, f, indent=2)

if __name__ == "__main__":
    main()
