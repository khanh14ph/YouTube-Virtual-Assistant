import logging
from typing import List, Dict, Optional, Any
import numpy as np

from src.services.downloader import YouTubeDownloader
from src.services.vad_service import VADService
from src.services.asr_service import ASRService
from src.services.llm_service import BaseLLMService, create_llm_service
from .config import config
from .exceptions import YouTubeAssistantError, DownloadError, VADError, ASRError, LLMError


logger = logging.getLogger(__name__)


class VideoProcessor:
    """Main processor class that orchestrates the entire pipeline"""
    
    def __init__(self, llm_service_type: str = "local", llm_kwargs: Optional[Dict] = None):
        """
        Initialize the video processor
        
        Args:
            llm_service_type: Type of LLM service to use ("local" or "openai")
            llm_kwargs: Additional arguments for LLM service
        """
        self.config = config
        
        # Initialize services
        self.downloader = YouTubeDownloader()
        self.vad_service = VADService()
        self.asr_service = ASRService()
        
        # Initialize LLM service
        llm_kwargs = llm_kwargs or {}
        self.llm_service = create_llm_service(llm_service_type, **llm_kwargs)
        
        # Store processed data
        self.transcript = ""
        self.conversation_history: List[Dict[str, str]] = []
        
    def process_video(self, youtube_url: str) -> str:
        """
        Process a YouTube video through the complete pipeline
        
        Args:
            youtube_url: YouTube video URL
            
        Returns:
            Complete transcript of the video
            
        Raises:
            YouTubeAssistantError: If any step in the pipeline fails
        """
        try:
            logger.info(f"Starting video processing for: {youtube_url}")
            
            # Step 1: Download video
            logger.info("Downloading video...")
            audio_file = self.downloader.download(youtube_url)
            
            # Step 2: Voice Activity Detection
            logger.info("Performing voice activity detection...")
            wav, speech_timestamps = self.vad_service.process_audio(audio_file)
            
            # Step 3: Extract speech segments
            logger.info("Extracting speech segments...")
            speech_segments = self.vad_service.extract_speech_segments(wav, speech_timestamps)
            
            if not speech_segments:
                logger.warning("No speech segments found in the audio")
                return "No speech detected in the video."
            
            # Step 4: Automatic Speech Recognition
            logger.info(f"Transcribing {len(speech_segments)} speech segments...")
            transcripts = self.asr_service.transcribe_batch(speech_segments)
            
            # Step 5: Combine transcripts
            self.transcript = self.asr_service.combine_transcripts(transcripts)
            
            # Clean up
            self.downloader.cleanup()
            
            logger.info("Video processing completed successfully")
            return self.transcript
            
        except (DownloadError, VADError, ASRError) as e:
            logger.error(f"Pipeline error: {str(e)}")
            self.downloader.cleanup()  # Clean up on error
            raise
        except Exception as e:
            logger.error(f"Unexpected error during video processing: {str(e)}")
            self.downloader.cleanup()  # Clean up on error
            raise YouTubeAssistantError(f"Video processing failed: {str(e)}")
    
    def ask_question(self, question: str) -> str:
        """
        Ask a question about the processed video
        
        Args:
            question: User's question
            
        Returns:
            Assistant's response
            
        Raises:
            YouTubeAssistantError: If no transcript is available or LLM fails
        """
        if not self.transcript:
            raise YouTubeAssistantError("No video has been processed yet. Please process a video first.")
        print("self.transcript",self.transcript)
        try:
            response, self.conversation_history = self.llm_service.chat(
                prompt=question,
                context=self.transcript,
                conversation_history=self.conversation_history
            )
            return response
            
        except LLMError as e:
            logger.error(f"LLM error: {str(e)}")
            raise YouTubeAssistantError(f"Failed to generate response: {str(e)}")
    
    def reset_conversation(self):
        """Reset the conversation history"""
        self.conversation_history = []
        logger.info("Conversation history reset")
    
    def get_transcript(self) -> str:
        """Get the current transcript"""
        return self.transcript
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get the current conversation history"""
        return self.conversation_history.copy()
    
    def is_ready(self) -> bool:
        """Check if a video has been processed and is ready for questions"""
        return bool(self.transcript)