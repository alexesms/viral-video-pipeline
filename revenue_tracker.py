#!/usr/bin/env python3
"""
Revenue Tracking System
Tracks views, earnings, and calculates profit sharing
"""

import os
import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

DB_PATH = os.path.expanduser("~/viral-video-portal/database.db")

class RevenueTracker:
    def __init__(self):
        self.revenue_dir = os.path.expanduser("~/viral-video-lab-workflow/revenue")
        os.makedirs(self.revenue_dir, exist_ok=True)
    
    def track_video_performance(self, video_id, platform, views, revenue):
        """Track performance of a posted video"""
        # Save to database
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        c.execute('''
            INSERT INTO video_performance (video_id, platform, views, revenue, tracked_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (video_id, platform, views, revenue, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        
        print(f"  📊 Tracked: {video_id} on {platform} - {views} views, ${revenue:.2f}")
    
    def calculate_profit_share(self, total_revenue, creator_share=0.30):
        """Calculate profit sharing"""
        creator_amount = total_revenue * creator_share
        platform_amount = total_revenue - creator_amount
        
        return {
            "total_revenue": total_revenue,
            "creator_share": creator_amount,
            "platform_share": platform_amount,
            "creator_percentage": creator_share * 100
        }
    
    def get_creator_earnings(self, email):
        """Get total earnings for a creator"""
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        c.execute('''
            SELECT SUM(e.amount) as total_earnings
            FROM earnings e
            JOIN submissions s ON e.submission_id = s.id
            WHERE s.email = ? AND e.paid = FALSE
        ''', (email,))
        
        result = c.fetchone()
        conn.close()
        
        return result[0] if result and result[0] else 0
    
    def generate_monthly_report(self, month=None):
        """Generate monthly revenue report"""
        if month is None:
            month = datetime.now().strftime('%Y-%m')
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Get all earnings for the month
        c.execute('''
            SELECT s.email, s.idea_title, SUM(e.amount) as total_earned
            FROM earnings e
            JOIN submissions s ON e.submission_id = s.id
            WHERE strftime('%Y-%m', e.created_at) = ?
            GROUP BY s.email, s.idea_title
            ORDER BY total_earned DESC
        ''', (month,))
        
        earnings = c.fetchall()
        conn.close()
        
        # Generate report
        report_path = os.path.join(self.revenue_dir, f"report_{month}.md")
        
        with open(report_path, 'w') as f:
            f.write(f"# 💰 Revenue Report — {month}\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
            
            total_revenue = sum(e[2] for e in earnings)
            total_creator_share = total_revenue * 0.30
            
            f.write(f"## Summary\n\n")
            f.write(f"- **Total Revenue:** ${total_revenue:,.2f}\n")
            f.write(f"- **Creator Share (30%):** ${total_creator_share:,.2f}\n")
            f.write(f"- **Platform Share (70%):** ${total_revenue - total_creator_share:,.2f}\n\n")
            
            f.write(f"## Creator Earnings\n\n")
            f.write(f"| Creator | Idea | Earnings | Creator Share |\n")
            f.write(f"|---------|------|----------|---------------|\n")
            
            for email, title, earned in earnings:
                creator_share = earned * 0.30
                f.write(f"| {email} | {title} | ${earned:,.2f} | ${creator_share:,.2f} |\n")
        
        print(f"📄 Report saved: {report_path}")
        return report_path
    
    def process_payouts(self, minimum_payout=50):
        """Process payouts for creators"""
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Get creators with pending earnings
        c.execute('''
            SELECT s.email, u.name, u.paypal_email, SUM(e.amount) as total_earned
            FROM earnings e
            JOIN submissions s ON e.submission_id = s.id
            JOIN users u ON s.email = u.email
            WHERE e.paid = FALSE
            GROUP BY s.email
            HAVING total_earned >= ?
        ''', (minimum_payout,))
        
        creators = c.fetchall()
        conn.close()
        
        print(f"\n💸 Processing payouts (minimum: ${minimum_payout})")
        print(f"  Found {len(creators)} creators eligible for payout\n")
        
        for email, name, paypal, earned in creators:
            creator_share = earned * 0.30
            print(f"  👤 {name} ({email})")
            print(f"    Earnings: ${earned:,.2f}")
            print(f"    Creator Share (30%): ${creator_share:,.2f}")
            print(f"    PayPal: {paypal or 'Not set'}")
            
            if paypal:
                print(f"    ✅ Ready for payout via PayPal")
                # Here you would integrate with PayPal API
            else:
                print(f"    ⚠️ No PayPal email set")
    
    def track_platform_revenue(self):
        """Track revenue from all platforms"""
        print("\n📊 Tracking platform revenue...")
        
        # This would integrate with platform APIs
        # For now, show manual tracking instructions
        
        platforms = {
            "YouTube": {
                "url": "https://studio.youtube.com/channel/UC/monetization",
                "metrics": ["views", "watch_time", "rpm", "revenue"]
            },
            "TikTok": {
                "url": "https://www.tiktok.com/creator#/monetization",
                "metrics": ["views", "followers", "creator_fund"]
            },
            "Bilibili": {
                "url": "https://member.bilibili.com/platform/home",
                "metrics": ["views", "fans", "创作激励"]
            }
        }
        
        for platform, config in platforms.items():
            print(f"\n  📱 {platform}")
            print(f"    Dashboard: {config['url']}")
            print(f"    Track: {', '.join(config['metrics'])}")

def main():
    """Main function"""
    import sys
    
    tracker = RevenueTracker()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "--report":
            month = sys.argv[2] if len(sys.argv) > 2 else None
            tracker.generate_monthly_report(month)
        elif command == "--payouts":
            minimum = float(sys.argv[2]) if len(sys.argv) > 2 else 50
            tracker.process_payouts(minimum)
        elif command == "--track":
            tracker.track_platform_revenue()
        else:
            print(f"Unknown command: {command}")
    else:
        print("Usage:")
        print("  python3 revenue_tracker.py --report [YYYY-MM]")
        print("  python3 revenue_tracker.py --payouts [minimum]")
        print("  python3 revenue_tracker.py --track")

if __name__ == "__main__":
    main()
