#!/usr/bin/env python3
"""
YEAP Dashboard - Quick Start Script (Python Version)
Usage: Run this script directly in your IDE, or execute 'python start_dashboard.py' in command line
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def print_banner():
    """Print startup banner"""
    print("=" * 50)
    print("YEAP Dashboard - Quick Start Script")
    print("=" * 50)
    print()

def check_environment():
    """Check runtime environment"""
    # Check if we're in the correct directory
    if not Path("streamlit").exists():
        print("❌ Error: Please run this script from the YEAP-9-19 project root directory")
        print(f"Current directory: {os.getcwd()}")
        input("Press Enter to exit...")
        sys.exit(1)
    
    # Check if streamlit_app.py exists
    streamlit_app = Path("streamlit/streamlit_app.py")
    if not streamlit_app.exists():
        print("❌ Error: streamlit_app.py not found in streamlit directory")
        input("Press Enter to exit...")
        sys.exit(1)
    
    print("✅ Environment check passed")

def check_dependencies():
    """Check if dependencies are installed"""
    try:
        import streamlit
        print("✅ Streamlit is installed")
        return True
    except ImportError:
        print("❌ Streamlit is not installed")
        print("Please install it using: pip install streamlit")
        return False

def start_streamlit():
    """Start Streamlit application"""
    print()
    print("🚀 Starting YEAP Dashboard...")
    print()
    print("📱 The dashboard will open in your default browser automatically.")
    print("🌐 If it doesn't open, please visit: http://localhost:8501")
    print()
    print("⏹️  To stop the server, press Ctrl+C in this window.")
    print("=" * 50)
    print()
    
    # Change to streamlit directory
    os.chdir("streamlit")
    
    try:
        # Start Streamlit application
        subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"], check=True)
    except subprocess.CalledProcessError as e:
        print()
        print("=" * 50)
        print("❌ Error: Failed to start Streamlit")
        print()
        print(f"Error details: {e}")
        print()
        print("Possible solutions:")
        print("1. Make sure Python is installed and in PATH")
        print("2. Install Streamlit: pip install streamlit")
        print("3. Install project dependencies: pip install -r requirements.txt")
        print("4. Check if port 8501 is already in use")
        print("=" * 50)
        input("Press Enter to exit...")
        sys.exit(1)
    except KeyboardInterrupt:
        print()
        print("🛑 Dashboard stopped by user")
        print("👋 Goodbye!")

def main():
    """Main function"""
    print_banner()
    check_environment()
    
    if not check_dependencies():
        input("Press Enter to exit...")
        sys.exit(1)
    
    start_streamlit()

if __name__ == "__main__":
    main()