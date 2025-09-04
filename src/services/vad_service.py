import torch
from typing import List, Dict, Tuple, Any
import numpy as np

from src.core.config import config
from src.core.exceptions import VADError


class VADService:
    def __init__(self):
        self.config = config
        self.model = None
        self.utils = None
        self._initialize_model()
        
    def _initialize_model(self):
        """Initialize the VAD model"""
        try:
            torch.set_num_threads(1)
            self.model, self.utils = torch.hub.load(
                repo_or_dir=self.config.vad_model, 
                model="silero_vad"
            )
        except Exception as e:
            raise VADError(f"Failed to load VAD model: {str(e)}")
    
    def process_audio(self, filepath: str) -> Tuple[np.ndarray, List[Dict[str, int]]]:
        """
        Process audio file to detect speech segments
        
        Args:
            filepath: Path to the audio file
            
        Returns:
            Tuple of (audio_array, speech_timestamps)
            
        Raises:
            VADError: If processing fails
        """
        try:
            if self.utils is None:
                raise VADError("VAD model not initialized")
                
            get_speech_timestamps, _, read_audio, _, _ = self.utils
            
            # Read audio file
            wav = read_audio(filepath)
            
            # Get speech timestamps
            speech_timestamps = get_speech_timestamps(wav, self.model)
            
            return wav, speech_timestamps
            
        except Exception as e:
            raise VADError(f"VAD processing failed: {str(e)}")
    
    def extract_speech_segments(self, wav: np.ndarray, timestamps: List[Dict[str, int]]) -> List[Tuple[np.ndarray, float]]:
        """
        Extract speech segments with durations
        
        Args:
            wav: Audio array
            timestamps: List of speech timestamps
            
        Returns:
            List of (speech_segment, duration) tuples
        """
        speech_segments = []
        
        for timestamp in timestamps:
            start_idx = timestamp["start"]
            end_idx = timestamp["end"]
            
            # Extract segment
            segment = wav[start_idx:end_idx]
            
            # Calculate duration in seconds
            duration = (end_idx - start_idx) / self.config.sample_rate
            
            speech_segments.append((segment.numpy(), duration))
            
        return speech_segments