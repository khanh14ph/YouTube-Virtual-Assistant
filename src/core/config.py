import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    # Audio settings
    sample_rate: int = 16000
    audio_format: str = "wav"
    channels: int = 1
    
    # Processing settings
    download_dir: str = "downloads"
    temp_audio_file: str = "audio.wav"
    
    # Model settings
    vad_model: str = "snakers4/silero-vad"
    asr_model: str = "facebook/mms-1b-all"
    asr_language: str = "eng"
    
    # LLM settings
    llm_model: Optional[str] = None
    llm_api_key: Optional[str] = None
    llm_base_url: Optional[str] = None
    
    # Processing settings
    beam_width: int = 50
    num_processes: int = 4
    
    @classmethod
    def from_env(cls) -> "Config":
        return cls(
            sample_rate=int(os.getenv("SAMPLE_RATE", 16000)),
            audio_format=os.getenv("AUDIO_FORMAT", "wav"),
            channels=int(os.getenv("CHANNELS", 1)),
            download_dir=os.getenv("DOWNLOAD_DIR", "downloads"),
            temp_audio_file=os.getenv("TEMP_AUDIO_FILE", "audio.wav"),
            vad_model=os.getenv("VAD_MODEL", "snakers4/silero-vad"),
            asr_model=os.getenv("ASR_MODEL", "nguyenvulebinh/wav2vec2-base-vietnamese-250h"),
            asr_language=os.getenv("ASR_LANGUAGE", "eng"),
            llm_model=os.getenv("LLM_MODEL"),
            llm_api_key=os.getenv("LLM_API_KEY"),
            llm_base_url=os.getenv("LLM_BASE_URL"),
            beam_width=int(os.getenv("BEAM_WIDTH", 50)),
            num_processes=int(os.getenv("NUM_PROCESSES", 4)),
        )


config = Config.from_env()