#!/usr/bin/env python3
"""
Dashboard Launcher for Telegram Analysis Results
Simple script to launch the Streamlit dashboard

Author: Chaos
Date: August 2025
"""

import os
import sys
import subprocess

def main():
    print("🚀 Launching Telegram Analysis Dashboard...")
    print("📊 Loading your analysis results...")
    
    # Check if analysis results exist - try combined results first
    combined_csv = "../combined_analysis_results/coded_messages_detailed.csv"
    combined_json = "../combined_analysis_results/analysis_summary.json"
    single_csv = "../telegram_analysis_results/coded_messages_detailed.csv"
    single_json = "../telegram_analysis_results/analysis_summary.json"
    
    if os.path.exists(combined_csv) and os.path.exists(combined_json):
        print("✅ Combined analysis results found (12,000 messages)!")
    elif os.path.exists(single_csv) and os.path.exists(single_json):
        print("✅ Single dataset analysis results found (6,000 messages)!")
    else:
        print("❌ Error: Analysis results not found!")
        print("Please run the telegram_codebook_analyzer.py first to generate results.")
        sys.exit(1)
    print("🌐 Starting dashboard server...")
    print("\n" + "="*50)
    print("📍 Dashboard will open in your browser automatically")
    print("🔗 Manual URL: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the dashboard")
    print("="*50 + "\n")
    
    try:
        # Launch Streamlit dashboard
        subprocess.run([
            "streamlit", "run", "telegram_analysis_dashboard.py",
            "--server.headless", "false",
            "--server.port", "8501",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Dashboard stopped by user")
    except Exception as e:
        print(f"❌ Error launching dashboard: {e}")

if __name__ == "__main__":
    main()
