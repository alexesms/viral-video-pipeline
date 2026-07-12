#!/usr/bin/env python3
"""
Viral Video Lab — Complete Automation Workflow
From submission to posting: find, create, dub, subtitle, post, track revenue

Usage: python3 workflow_orchestrator.py [--mode=daily|single|test]
"""

import os
import json
import sqlite3
import subprocess
import asyncio
import requests
from datetime import datetime, timedelta
from pathlib import Path

# Configuration
BASE_DIR = os.path.expanduser("~/viral-video-lab-workflow")
DB_PATH = os.path.expanduser("~/viral-video-portal/database.db")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
QUEUE_DIR = os.path.join(BASE_DIR, "queue")
POSTED_DIR = os.path.join(BASE_DIR, "posted")

# API Keys (from environment or config)
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
COOLIFY_TOKEN = os.environ.get("COOLIFY_TOKEN", "")
COOLIFY_URL = "https://devops.extrasolid.com"

# Target languages for dubbing
TARGET_LANGUAGES = {
    "vi": {"voice": "vi-VN-NamMinhNeural", "name": "Vietnamese", "platforms": ["tiktok", "youtube"]},
    "zh": {"voice": "zh-CN-YunxiNeural", "name": "Chinese", "platforms": ["bilibili", "douyin", "youtube"]},
    "ja": {"voice": "ja-JP-KeitaNeural", "name": "Japanese", "platforms": ["tiktok", "youtube"]},
    "ko": {"voice": "ko-KR-InJoonNeural", "name": "Korean", "platforms": ["tiktok", "youtube"]},
    "es": {"voice": "es-ES-AlvaroNeural", "name": "Spanish", "platforms": ["tiktok", "youtube"]},
    "pt": {"voice": "pt-BR-AntonioNeural", "name": "Portuguese", "platforms": ["tiktok", "youtube"]},
    "ar": {"voice": "ar-SA-HamedNeural", "name": "Arabic", "platforms": ["tiktok", "youtube"]},
    "hi": {"voice": "hi-IN-MadhurNeural", "name": "Hindi", "platforms": ["tiktok", "youtube"]},
    "fr": {"voice": "fr-FR-HenriNeural", "name": "French", "platforms": ["tiktok", "youtube"]},
    "de": {"voice": "de-DE-ConradNeural", "name": "German", "platforms": ["tiktok", "youtube"]},
}

# Search queries for finding viral content
SEARCH_QUERIES = [
    "funny robot fails 2026",
    "AI comedy moments",
    "unexpected funny technology",
    "hilarious product demo",
    "viral comedy shorts",
    "funny AI interactions",
    "tech fails compilation",
    "comedy gold viral",
]

class WorkflowOrchestrator:
    def __init__(self):
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        os.makedirs(QUEUE_DIR, exist_ok=True)
        os.makedirs(POSTED_DIR, exist_ok=True)
        
    def run(self, mode="daily"):
        """Main workflow entry point"""
        print("=" * 70)
        print("🎬 VIRAL VIDEO LAB — AUTOMATION WORKFLOW")
        print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🔧 Mode: {mode}")
        print("=" * 70)
        
        if mode == "daily":
            return self.daily_workflow()
        elif mode == "single":
            return self.single_video_workflow()
        elif mode == "test":
            return self.test_workflow()
        else:
            print(f"Unknown mode: {mode}")
            return False
    
    def daily_workflow(self):
        """Daily automation workflow"""
        print("\n📋 DAILY WORKFLOW")
        print("-" * 50)
        
        # Step 1: Check for new submissions
        submissions = self.get_pending_submissions()
        print(f"📥 Found {len(submissions)} pending submissions")
        
        # Step 2: Find trending content (if no submissions)
        if not submissions:
            print("🔍 No submissions found, searching for trending content...")
            trending = self.find_trending_content()
            if trending:
                submissions = trending
        
        # Step 3: Process each submission
        results = []
        for submission in submissions[:3]:  # Process up to 3 per day
            print(f"\n{'='*50}")
            print(f"🎬 Processing: {submission.get('idea_title', 'Unknown')}")
            print(f"{'='*50}")
            
            result = self.process_submission(submission)
            results.append(result)
        
        # Step 4: Post to social media
        print("\n📤 POSTING TO SOCIAL MEDIA")
        print("-" * 50)
        self.post_to_social_media(results)
        
        # Step 5: Track revenue
        print("\n💰 TRACKING REVENUE")
        print("-" * 50)
        self.track_revenue()
        
        # Step 6: Generate report
        self.generate_report(results)
        
        return results
    
    def single_video_workflow(self):
        """Process a single video idea"""
        print("\n🎬 SINGLE VIDEO WORKFLOW")
        print("-" * 50)
        
        # Get the next pending submission
        submissions = self.get_pending_submissions()
        if not submissions:
            print("❌ No pending submissions found")
            return None
        
        submission = submissions[0]
        return self.process_submission(submission)
    
    def test_workflow(self):
        """Test workflow with sample data"""
        print("\n🧪 TEST WORKFLOW")
        print("-" * 50)
        
        test_submission = {
            "id": "test-001",
            "idea_title": "Funny Robot Dance Battle",
            "description": "Two robots having a dance battle with increasingly ridiculous moves",
            "category": "comedy",
            "email": "test@example.com"
        }
        
        return self.process_submission(test_submission)
    
    def get_pending_submissions(self):
        """Get pending submissions from database"""
        try:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("SELECT * FROM submissions WHERE status = 'pending' ORDER BY created_at DESC LIMIT 5")
            columns = [desc[0] for desc in c.description]
            submissions = [dict(zip(columns, row)) for row in c.fetchall()]
            conn.close()
            return submissions
        except Exception as e:
            print(f"⚠️ Database error: {e}")
            return []
    
    def find_trending_content(self):
        """Find trending content using Agent-Reach"""
        print("  Searching YouTube for trending funny clips...")
        
        try:
            # Use yt-dlp to search
            query = SEARCH_QUERIES[0]
            cmd = f'yt-dlp --flat-playlist --print "%(id)s %(title)s %(duration)s" "ytsearch3:{query}" 2>/dev/null'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                clips = []
                for line in result.stdout.strip().split('\n'):
                    parts = line.split(' ', 2)
                    if len(parts) >= 2:
                        clips.append({
                            "id": f"trending-{parts[0]}",
                            "idea_title": parts[1] if len(parts) > 1 else "Unknown",
                            "description": f"Trending video: {parts[1]}",
                            "category": "comedy",
                            "source_url": f"https://youtube.com/watch?v={parts[0]}",
                            "email": "system@virallab.com"
                        })
                
                print(f"  ✓ Found {len(clips)} trending clips")
                return clips
        except Exception as e:
            print(f"  ✗ Search failed: {e}")
        
        return []
    
    def process_submission(self, submission):
        """Process a single submission through the entire pipeline"""
        submission_id = submission.get('id', 'unknown')
        title = submission.get('idea_title', 'Unknown')
        
        print(f"\n📋 Processing: {title}")
        
        # Create output directory
        video_dir = os.path.join(OUTPUT_DIR, f"{submission_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        os.makedirs(video_dir, exist_ok=True)
        
        result = {
            "submission_id": submission_id,
            "title": title,
            "status": "processing",
            "videos": {},
            "posted": [],
            "errors": []
        }
        
        # Step 1: Find or create source video
        print("  📥 Step 1: Finding source video...")
        source_video = self.find_source_video(submission, video_dir)
        if not source_video:
            result["status"] = "failed"
            result["errors"].append("Failed to find source video")
            return result
        
        result["source_video"] = source_video
        
        # Step 2: Extract audio and transcribe
        print("  🎵 Step 2: Transcribing audio...")
        transcription = self.transcribe_video(source_video, video_dir)
        if not transcription:
            result["status"] = "failed"
            result["errors"].append("Failed to transcribe video")
            return result
        
        result["transcription"] = transcription
        
        # Step 3: Translate to all languages
        print("  🌍 Step 3: Translating to all languages...")
        translations = self.translate_to_all_languages(transcription, video_dir)
        result["translations"] = translations
        
        # Step 4: Generate dubbed audio for each language
        print("  🎙️ Step 4: Generating dubbed audio...")
        dubbed_videos = self.generate_dubbed_videos(source_video, translations, video_dir)
        result["videos"] = dubbed_videos
        
        # Step 5: Add subtitles
        print("  📝 Step 5: Adding subtitles...")
        subtitled_videos = self.add_subtitles(dubbed_videos, translations, video_dir)
        result["videos"] = subtitled_videos
        
        # Step 6: Prepare for posting
        print("  📦 Step 6: Preparing for posting...")
        self.prepare_for_posting(subtitled_videos, submission, video_dir)
        
        result["status"] = "ready"
        print(f"  ✅ Processing complete: {title}")
        
        return result
    
    def find_source_video(self, submission, output_dir):
        """Find or download source video"""
        source_url = submission.get('source_url')
        
        if source_url:
            # Download the specific video
            print(f"    Downloading: {source_url}")
            output_path = os.path.join(output_dir, "source.mp4")
            cmd = f'yt-dlp -f "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" -o "{output_path}" "{source_url}" 2>/dev/null'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
            
            if os.path.exists(output_path):
                print(f"    ✓ Downloaded: {output_path}")
                return output_path
        
        # Search for a video matching the idea
        idea = submission.get('idea_title', '')
        print(f"    Searching for: {idea}")
        
        cmd = f'yt-dlp --flat-playlist --print "%(id)s" "ytsearch1:{idea}" 2>/dev/null'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        
        if result.stdout.strip():
            video_id = result.stdout.strip().split('\n')[0]
            source_url = f"https://youtube.com/watch?v={video_id}"
            output_path = os.path.join(output_dir, "source.mp4")
            
            cmd = f'yt-dlp -f "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" -o "{output_path}" "{source_url}" 2>/dev/null'
            subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
            
            if os.path.exists(output_path):
                print(f"    ✓ Found and downloaded: {output_path}")
                return output_path
        
        print("    ✗ No source video found")
        return None
    
    def transcribe_video(self, video_path, output_dir):
        """Transcribe video audio"""
        audio_path = os.path.join(output_dir, "audio.wav")
        
        # Extract audio
        cmd = f'ffmpeg -y -i "{video_path}" -vn -acodec pcm_s16le -ar 16000 -ac 1 "{audio_path}" 2>/dev/null'
        subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        
        if not os.path.exists(audio_path):
            return None
        
        # Transcribe using agent-reach
        try:
            cmd = f'export PATH="$HOME/.local/bin:$PATH" && agent-reach transcribe "{audio_path}" 2>/dev/null'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
            
            if result.stdout.strip():
                transcription = result.stdout.strip()
                print(f"    ✓ Transcribed: {transcription[:100]}...")
                
                # Save transcription
                with open(os.path.join(output_dir, "transcription.txt"), 'w') as f:
                    f.write(transcription)
                
                return transcription
        except Exception as e:
            print(f"    ✗ Transcription failed: {e}")
        
        return None
    
    def translate_to_all_languages(self, text, output_dir):
        """Translate text to all target languages"""
        translations = {}
        
        for lang_code, lang_config in TARGET_LANGUAGES.items():
            print(f"    Translating to {lang_config['name']}...")
            
            translation = self.translate_text(text, lang_code)
            if translation:
                translations[lang_code] = {
                    "text": translation,
                    "voice": lang_config["voice"],
                    "name": lang_config["name"],
                    "platforms": lang_config["platforms"]
                }
                
                # Save translation
                with open(os.path.join(output_dir, f"translation_{lang_code}.txt"), 'w') as f:
                    f.write(translation)
                
                print(f"      ✓ {lang_config['name']}: {translation[:50]}...")
            else:
                print(f"      ✗ {lang_config['name']}: Translation failed")
        
        return translations
    
    def translate_text(self, text, target_lang):
        """Translate text using OpenRouter API"""
        if not OPENROUTER_API_KEY:
            print("      ⚠️ No OpenRouter API key, using mock translation")
            return f"[{target_lang}] {text}"
        
        lang_names = {
            "vi": "Vietnamese", "zh": "Chinese (Mandarin)", "ja": "Japanese",
            "ko": "Korean", "es": "Spanish", "pt": "Portuguese",
            "ar": "Arabic", "hi": "Hindi", "fr": "French", "de": "German"
        }
        
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        
        prompt = f"""Translate this English text to {lang_names.get(target_lang, target_lang)}. 
Rules:
- Keep it natural for spoken language
- Preserve comedic timing
- Output ONLY the translation, no explanations

Text: {text}"""
        
        data = {
            "model": "openai/gpt-4o-mini",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 500
        }
        
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"      ✗ API error: {e}")
        
        return None
    
    def generate_dubbed_videos(self, source_video, translations, output_dir):
        """Generate dubbed videos for each language"""
        import edge_tts
        
        dubbed_videos = {}
        
        for lang_code, translation in translations.items():
            print(f"    Generating {translation['name']} TTS...")
            
            tts_path = os.path.join(output_dir, f"tts_{lang_code}.mp3")
            
            try:
                # Generate TTS
                communicate = edge_tts.Communicate(translation["text"], translation["voice"])
                asyncio.run(communicate.save(tts_path))
                
                if os.path.exists(tts_path):
                    # Mix with video
                    output_video = os.path.join(output_dir, f"dubbed_{lang_code}.mp4")
                    
                    # Remove original audio and add TTS
                    cmd = f'ffmpeg -y -i "{source_video}" -i "{tts_path}" -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 -shortest "{output_video}" 2>/dev/null'
                    subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
                    
                    if os.path.exists(output_video):
                        dubbed_videos[lang_code] = {
                            "path": output_video,
                            "translation": translation
                        }
                        print(f"      ✓ {translation['name']}: {output_video}")
            except Exception as e:
                print(f"      ✗ {translation['name']}: {e}")
        
        return dubbed_videos
    
    def add_subtitles(self, dubbed_videos, translations, output_dir):
        """Add hardcoded subtitles to videos"""
        # This would use the subtitle burning script from the video-dubbing-pipeline skill
        # For now, return the dubbed videos as-is
        print("    ℹ️ Subtitle burning skipped (implement with moviepy)")
        return dubbed_videos
    
    def prepare_for_posting(self, videos, submission, output_dir):
        """Prepare videos for posting to social media"""
        for lang_code, video_info in videos.items():
            # Create metadata file
            metadata = {
                "submission_id": submission.get('id'),
                "language": lang_code,
                "video_path": video_info['path'],
                "title": self.generate_title(submission, lang_code),
                "description": self.generate_description(submission, lang_code),
                "tags": self.generate_tags(submission, lang_code),
                "platforms": video_info['translation']['platforms'],
                "status": "ready",
                "created_at": datetime.now().isoformat()
            }
            
            metadata_path = os.path.join(output_dir, f"metadata_{lang_code}.json")
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            # Copy to queue
            queue_path = os.path.join(QUEUE_DIR, f"{submission.get('id')}_{lang_code}.json")
            with open(queue_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            print(f"    ✓ Queued: {lang_code} - {metadata['title']}")
    
    def generate_title(self, submission, lang_code):
        """Generate SEO-optimized title"""
        title = submission.get('idea_title', 'Funny Video')
        lang_names = {"vi": "Vietnamese", "zh": "Chinese", "ja": "Japanese", "ko": "Korean", "es": "Spanish", "pt": "Portuguese", "ar": "Arabic", "hi": "Hindi", "fr": "French", "de": "German"}
        
        if lang_code == "en":
            return f"{title} 🤣 #shorts #funny #viral"
        else:
            return f"{title} 🤣 ({lang_names.get(lang_code, lang_code)} dubbed)"
    
    def generate_description(self, submission, lang_code):
        """Generate SEO-optimized description"""
        title = submission.get('idea_title', 'Funny Video')
        return f"""{title} 🤣

🔔 Subscribe for daily comedy from around the world!

🌍 Languages: English + 10 dubbed versions
📧 Business: hello@viralvideolab.com

#funny #comedy #viral #shorts #dubbed"""
    
    def generate_tags(self, submission, lang_code):
        """Generate relevant tags"""
        return ["funny", "comedy", "viral", "shorts", "dubbed", "AI", "robots", "2026"]
    
    def post_to_social_media(self, results):
        """Post videos to social media platforms"""
        for result in results:
            if result.get('status') != 'ready':
                continue
            
            for lang_code, video_info in result.get('videos', {}).items():
                metadata_path = os.path.join(os.path.dirname(video_info['path']), f"metadata_{lang_code}.json")
                
                if os.path.exists(metadata_path):
                    with open(metadata_path) as f:
                        metadata = json.load(f)
                    
                    for platform in metadata.get('platforms', []):
                        print(f"  📤 Posting to {platform}: {metadata['title']}")
                        # Platform-specific posting would go here
                        # For now, just log the action
                        self.log_posting_action(platform, metadata)
    
    def log_posting_action(self, platform, metadata):
        """Log posting action for manual review"""
        log_path = os.path.join(POSTED_DIR, f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{platform}.json")
        with open(log_path, 'w') as f:
            json.dump({
                "platform": platform,
                "title": metadata.get('title'),
                "video_path": metadata.get('video_path'),
                "status": "pending_upload",
                "timestamp": datetime.now().isoformat()
            }, f, indent=2)
        
        print(f"    ✓ Logged for {platform}")
    
    def track_revenue(self):
        """Track revenue from posted videos"""
        print("  ℹ️ Revenue tracking requires platform API integration")
        print("  📊 Manual tracking recommended until APIs are connected")
    
    def generate_report(self, results):
        """Generate daily report"""
        report_path = os.path.join(BASE_DIR, f"report_{datetime.now().strftime('%Y%m%d')}.md")
        
        with open(report_path, 'w') as f:
            f.write(f"# Viral Video Lab — Daily Report\n\n")
            f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
            f.write(f"## Summary\n\n")
            f.write(f"- **Videos Processed:** {len(results)}\n")
            f.write(f"- **Languages:** {len(TARGET_LANGUAGES)}\n")
            f.write(f"- **Platforms:** YouTube, TikTok, Bilibili, Douyin, Instagram\n\n")
            
            f.write(f"## Videos\n\n")
            for result in results:
                f.write(f"### {result.get('title', 'Unknown')}\n")
                f.write(f"- Status: {result.get('status', 'unknown')}\n")
                f.write(f"- Languages: {len(result.get('videos', {}))}\n")
                f.write(f"- Errors: {len(result.get('errors', []))}\n\n")
            
            f.write(f"## Next Steps\n\n")
            f.write(f"1. Review videos in `{QUEUE_DIR}`\n")
            f.write(f"2. Upload to social media platforms\n")
            f.write(f"3. Track engagement and revenue\n\n")
        
        print(f"\n📄 Report saved: {report_path}")

def main():
    import sys
    
    mode = "daily"
    if len(sys.argv) > 1:
        mode = sys.argv[1].replace("--mode=", "")
    
    orchestrator = WorkflowOrchestrator()
    results = orchestrator.run(mode)
    
    print(f"\n{'='*70}")
    print("✅ WORKFLOW COMPLETE")
    print(f"{'='*70}")

if __name__ == "__main__":
    main()
