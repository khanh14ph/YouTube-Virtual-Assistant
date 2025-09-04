#!/usr/bin/env python3
"""
YouTube Virtual Assistant - Main Entry Point

This application allows users to:
1. Input YouTube video URLs
2. Download and process video audio
3. Extract speech segments using Voice Activity Detection (VAD)  
4. Transcribe speech using Automatic Speech Recognition (ASR)
5. Ask questions about the video content using a local LLM

Usage:
    # Run GUI
    python -m src.main gui
    
    # Run CLI
    python -m src.main cli <youtube_url>
    
    # Run with custom configuration
    LLM_BASE_URL=http://localhost:8080 python -m src.main gui
"""

import argparse
import sys
import logging
from typing import Optional

from src.core.video_processor import VideoProcessor
from src.core.exceptions import YouTubeAssistantError
from src.utils.logging_utils import setup_logging


def run_gui():
    """Run the Streamlit GUI application"""
    try:
        import streamlit.web.cli as stcli
        from src.gui.streamlit_app import main
        
        # Run Streamlit app
        sys.argv = ["streamlit", "run", __file__.replace("main.py", "gui/streamlit_app.py")]
        stcli.main()
        
    except ImportError:
        print("Streamlit not installed. Please install it with: pip install streamlit")
        sys.exit(1)


def run_cli(youtube_url: str, llm_type: str = "local", interactive: bool = True):
    """
    Run the CLI version of the application
    
    Args:
        youtube_url: YouTube video URL to process
        llm_type: Type of LLM service to use
        interactive: Whether to run in interactive mode
    """
    logger = logging.getLogger(__name__)
    
    try:
        # Initialize processor
        print("Initializing YouTube Virtual Assistant...")
        processor = VideoProcessor(llm_service_type=llm_type)
        
        # Process video
        print(f"Processing video: {youtube_url}")
        transcript = processor.process_video(youtube_url)
        
        print(f"\n✅ Video processed successfully!")
        print(f"📝 Transcript length: {len(transcript)} characters")
        
        if not interactive:
            print(f"\nTranscript:\n{transcript}")
            return
        
        # Interactive Q&A session
        print("\n🤖 You can now ask questions about the video. Type 'quit' to exit.")
        
        while True:
            try:
                question = input("\n❓ Your question: ").strip()
                
                if question.lower() in ['quit', 'exit', 'q']:
                    break
                
                if not question:
                    continue
                
                print("🤔 Thinking...")
                response = processor.ask_question(question)
                print(f"🤖 Assistant: {response}")
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Error: {str(e)}")
        
        print("\n👋 Goodbye!")
        
    except YouTubeAssistantError as e:
        logger.error(f"Application error: {str(e)}")
        print(f"❌ Error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        print(f"❌ Unexpected error: {str(e)}")
        sys.exit(1)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="YouTube Virtual Assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        "mode",
        choices=["gui", "cli"],
        help="Run mode: gui (Streamlit interface) or cli (command line)"
    )
    
    parser.add_argument(
        "url",
        nargs="?",
        help="YouTube URL (required for CLI mode)"
    )
    
    parser.add_argument(
        "--llm-type",
        choices=["local", "openai"],
        default="local",
        help="LLM service type (default: local)"
    )
    
    parser.add_argument(
        "--non-interactive",
        action="store_true",
        help="Run CLI in non-interactive mode (just show transcript)"
    )
    
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Logging level (default: INFO)"
    )
    
    parser.add_argument(
        "--log-file",
        help="Log file path (optional)"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(level=args.log_level, log_file=args.log_file)
    
    # Validate arguments
    if args.mode == "cli" and not args.url:
        parser.error("YouTube URL is required for CLI mode")
    
    # Run application
    if args.mode == "gui":
        run_gui()
    else:
        run_cli(
            youtube_url=args.url,
            llm_type=args.llm_type,
            interactive=not args.non_interactive
        )


if __name__ == "__main__":
    main()