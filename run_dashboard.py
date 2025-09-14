#!/usr/bin/env python3
"""
Marketing Intelligence Dashboard Runner
This script starts the Streamlit dashboard with proper configuration.
"""

import subprocess
import sys
import os

def check_requirements():
    """Check if required packages are installed."""
    try:
        import streamlit
        import pandas
        import plotly
        import numpy
        print("✅ All required packages are installed.")
        return True
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_data_files():
    """Check if data files exist."""
    data_files = [
        'data/business.csv',
        'data/Facebook.csv', 
        'data/Google.csv',
        'data/TikTok.csv'
    ]
    
    missing_files = []
    for file in data_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing data files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ All data files found.")
    return True

def main():
    """Main function to run the dashboard."""
    print("🚀 Starting Marketing Intelligence Dashboard...")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Check data files
    if not check_data_files():
        sys.exit(1)
    
    print("✅ All checks passed. Starting dashboard...")
    print("📊 Dashboard will be available at: http://localhost:8501")
    print("=" * 50)
    
    # Start Streamlit
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped by user.")
    except Exception as e:
        print(f"❌ Error starting dashboard: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
