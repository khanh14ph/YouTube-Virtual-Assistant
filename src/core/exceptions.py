class YouTubeAssistantError(Exception):
    """Base exception for YouTube Assistant errors"""
    pass


class DownloadError(YouTubeAssistantError):
    """Raised when video download fails"""
    pass


class VADError(YouTubeAssistantError):
    """Raised when Voice Activity Detection fails"""
    pass


class ASRError(YouTubeAssistantError):
    """Raised when Automatic Speech Recognition fails"""
    pass


class LLMError(YouTubeAssistantError):
    """Raised when LLM processing fails"""
    pass


class AudioProcessingError(YouTubeAssistantError):
    """Raised when audio processing fails"""
    pass