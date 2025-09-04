import streamlit as st
import logging
import sys
import os
from typing import Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.core.video_processor import VideoProcessor
from src.core.exceptions import YouTubeAssistantError
from src.utils.logging_utils import setup_logging


# Setup logging
setup_logging(level="INFO")
logger = logging.getLogger(__name__)


class YouTubeAssistantGUI:
    """Streamlit GUI for YouTube Virtual Assistant"""
    
    def __init__(self):
        self.setup_page()
        self.initialize_session_state()
    
    def setup_page(self):
        """Setup Streamlit page configuration"""
        st.set_page_config(
            page_title="YouTube Virtual Assistant",
            page_icon="🎥",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    
    def initialize_session_state(self):
        """Initialize Streamlit session state variables"""
        if "processor" not in st.session_state:
            st.session_state.processor = None
        
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        if "video_processed" not in st.session_state:
            st.session_state.video_processed = False
        
        if "current_url" not in st.session_state:
            st.session_state.current_url = ""
        
        if "transcript" not in st.session_state:
            st.session_state.transcript = ""
    
    def render_sidebar(self):
        """Render the sidebar with configuration options"""
        with st.sidebar:
            st.title("Configuration")
            
            # LLM Service Selection
            llm_type = st.selectbox(
                "LLM Service",
                options=["local", "openai"],
                index=0,
                help="Select the type of LLM service to use"
            )
            
            # LLM Configuration
            if llm_type == "local":
                base_url = st.text_input(
                    "Local LLM Base URL",
                    value="http://localhost:8080",
                    help="Base URL for your local LLM API"
                )
                model_name = st.text_input(
                    "Model Name",
                    value="local-model",
                    help="Name of the local model"
                )
                llm_kwargs = {"base_url": base_url, "model": model_name}
            
            elif llm_type == "openai":
                api_key = st.text_input(
                    "OpenAI API Key",
                    type="password",
                    help="Your OpenAI API key"
                )
                model_name = st.selectbox(
                    "OpenAI Model",
                    options=["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"],
                    index=0
                )
                llm_kwargs = {"api_key": api_key, "model": model_name}
            
            # Initialize processor button
            if st.button("Initialize Assistant", type="primary"):
                try:
                    st.session_state.processor = VideoProcessor(
                        llm_service_type=llm_type,
                        llm_kwargs=llm_kwargs
                    )
                    st.success("Assistant initialized successfully!")
                    logger.info(f"Initialized processor with {llm_type} LLM service")
                except Exception as e:
                    st.error(f"Failed to initialize assistant: {str(e)}")
                    logger.error(f"Failed to initialize processor: {str(e)}")
            
            # Reset conversation
            if st.session_state.processor and st.button("Reset Conversation"):
                st.session_state.processor.reset_conversation()
                st.session_state.messages = []
                st.success("Conversation reset!")
    
    def render_main_content(self):
        """Render the main content area"""
        st.title("🎥 YouTube Virtual Assistant")
        st.markdown("Process YouTube videos and ask questions about their content!")
        
        if not st.session_state.processor:
            st.warning("Please initialize the assistant using the sidebar configuration.")
            return
        
        # URL Input Section
        st.header("1. Enter YouTube URL")
        youtube_url = st.text_input(
            "YouTube URL",
            placeholder="https://www.youtube.com/watch?v=...",
            help="Paste the YouTube video URL you want to analyze"
        )
        
        # Process Video Button
        if st.button("Process Video", type="primary", disabled=not youtube_url):
            if youtube_url != st.session_state.current_url:
                self.process_video(youtube_url)
            else:
                st.info("This video has already been processed!")
        
        # Show transcript if available
        if st.session_state.transcript:
            st.header("2. Video Transcript")
            with st.expander("View Full Transcript", expanded=False):
                st.text_area(
                    "Transcript",
                    value=st.session_state.transcript,
                    height=200,
                    disabled=True
                )
        
        # Chat Interface
        if st.session_state.video_processed:
            st.header("3. Ask Questions")
            self.render_chat_interface()
    
    def process_video(self, url: str):
        """Process a YouTube video"""
        with st.spinner("Processing video... This may take a few minutes."):
            try:
                transcript = st.session_state.processor.process_video(url)
                st.session_state.transcript = transcript
                st.session_state.video_processed = True
                st.session_state.current_url = url
                st.session_state.messages = []  # Reset messages for new video
                
                st.success("Video processed successfully!")
                logger.info(f"Successfully processed video: {url}")
                
            except YouTubeAssistantError as e:
                st.error(f"Failed to process video: {str(e)}")
                logger.error(f"Failed to process video {url}: {str(e)}")
            except Exception as e:
                st.error(f"Unexpected error: {str(e)}")
                logger.error(f"Unexpected error processing {url}: {str(e)}")
    
    def render_chat_interface(self):
        """Render the chat interface"""
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask a question about the video..."):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate assistant response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        response = st.session_state.processor.ask_question(prompt)
                        st.markdown(response)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                    except YouTubeAssistantError as e:
                        error_msg = f"Error: {str(e)}"
                        st.error(error_msg)
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})
    
    def run(self):
        """Run the Streamlit application"""
        self.render_sidebar()
        self.render_main_content()


def main():
    """Main function to run the Streamlit app"""
    app = YouTubeAssistantGUI()
    app.run()


if __name__ == "__main__":
    main()