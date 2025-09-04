#!/usr/bin/env python3
"""
Legacy main.py - Redirects to new modular architecture

This file maintains backward compatibility while directing users to the new structure.
For the full-featured application, use: python -m src.main
"""

import sys
import os

# Add src to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.main import main as new_main

def main(youtube_url=None):
    """
    Legacy function - redirects to new architecture
    
    For the new modular system, use:
        python -m src.main gui    # For GUI
        python -m src.main cli <url>  # For CLI
    """
    print("⚠️  Using legacy main.py")
    print("💡 For the full-featured application, use:")
    print("   python -m src.main gui    # For GUI interface")
    print("   python -m src.main cli <youtube_url>  # For CLI interface")
    
    if youtube_url:
        print(f"\n🔄 Redirecting to new CLI with URL: {youtube_url}")
        sys.argv = ["src.main", "cli", youtube_url]
        new_main()
    else:
        print(f"\n🔄 Starting GUI interface...")
        sys.argv = ["src.main", "gui"]
        new_main()

if __name__ == "__main__":
    # Handle command line arguments
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
