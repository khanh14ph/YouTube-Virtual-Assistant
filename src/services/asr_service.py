import torch
import numpy as np
from typing import List, Tuple, Optional
from multiprocessing import get_context
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC

from src.core.config import config
from src.core.exceptions import ASRError


class ASRService:
    def __init__(self):
        self.config = config
        self.processor = None
        self.model = None
        self.decoder = None
        self._initialize_model()
        
    def _initialize_model(self):
        """Initialize the ASR model and processor"""
        try:
            # Load processor and model
            self.processor = Wav2Vec2Processor.from_pretrained(self.config.asr_model)
            self.model = Wav2Vec2ForCTC.from_pretrained(self.config.asr_model)
            
            # Set target language
            # self.processor.tokenizer.set_target_lang(self.config.asr_language)
            # self.model.load_adapter(self.config.asr_language)
            
            # Move model to GPU if available
            if torch.cuda.is_available():
                self.model = self.model.to("cuda")
            
            self.model.eval()
            
            # Initialize decoder (you'll need to implement or import this)
            # For now, we'll use basic decoding without beam search
            
        except Exception as e:
            raise ASRError(f"Failed to initialize ASR model: {str(e)}")
    
    def transcribe_batch(self, speech_segments: List[Tuple[np.ndarray, float]]) -> List[str]:
        """
        Transcribe a batch of speech segments
        
        Args:
            speech_segments: List of (audio_array, duration) tuples
            
        Returns:
            List of transcriptions
            
        Raises:
            ASRError: If transcription fails
        """
        try:
            if not speech_segments:
                return []
            
            # Extract audio arrays from segments
            speech_batch = [segment[0] for segment in speech_segments]
            
            # Process inputs
            inputs = self.processor(
                speech_batch, 
                return_tensors="pt", 
                padding="longest",
                sampling_rate=self.config.sample_rate
            )
            
            # Move to GPU if available
            device = "cuda" if torch.cuda.is_available() else "cpu"
            inputs = {k: v.to(device) for k, v in inputs.items()}
            
            # Get logits
            with torch.no_grad():
                logits = self.model(**inputs).logits
            
            # Decode predictions
            if hasattr(self, 'decoder') and self.decoder:
                # Use beam search decoder if available
                logits_cpu = logits.cpu().numpy()
                with get_context("fork").Pool(processes=self.config.num_processes) as pool:
                    results = self.decoder.decode_beams_batch(
                        logits_list=logits_cpu, 
                        pool=pool, 
                        beam_width=self.config.beam_width
                    )
                transcriptions = [result[0][0] for result in results]
            else:
                # Use simple argmax decoding
                predicted_ids = torch.argmax(logits, dim=-1)
                transcriptions = self.processor.batch_decode(predicted_ids)
            
            return transcriptions
            
        except Exception as e:
            raise ASRError(f"ASR transcription failed: {str(e)}")
    
    def transcribe_single(self, audio_array: np.ndarray) -> str:
        """
        Transcribe a single audio segment
        
        Args:
            audio_array: Audio data as numpy array
            
        Returns:
            Transcription text
        """
        return self.transcribe_batch([(audio_array, 0.0)])[0]
    
    def combine_transcripts(self, transcripts: List[str]) -> str:
        """
        Combine individual transcripts into a single text
        
        Args:
            transcripts: List of transcript segments
            
        Returns:
            Combined transcript text
        """
        return ". ".join(transcript.strip() for transcript in transcripts if transcript.strip())