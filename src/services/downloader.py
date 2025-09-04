import os
import subprocess
from typing import Optional
import yt_dlp

from src.core.config import config
from src.core.exceptions import DownloadError


class YouTubeDownloader:
    def __init__(self):
        self.config = config
        
    def download(self, url: str, output_dir: Optional[str] = None) -> str:
        """
        Download YouTube video and convert to mono 16kHz audio
        
        Args:
            url: YouTube URL
            output_dir: Directory to save files (optional)
            
        Returns:
            Path to the processed audio file
            
        Raises:
            DownloadError: If download or conversion fails
        """
        if output_dir is None:
            output_dir = self.config.download_dir
            
        try:
            # Clean up previous audio file
            if os.path.exists(self.config.temp_audio_file):
                os.remove(self.config.temp_audio_file)
            
            # Create output directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)
            
            # Configure yt-dlp options
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': self.config.audio_format,
                }],
                'quiet': True,
                'no_warnings': True
            }

            # Download audio using yt-dlp
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                downloaded_file = ydl.prepare_filename(info).replace('.webm', f'.{self.config.audio_format}')
                
            # Convert to specified format and sample rate
            output_file = self.config.temp_audio_file
            conversion_command = [
                'ffmpeg', '-i', downloaded_file,
                '-acodec', 'pcm_s16le',
                '-ac', str(self.config.channels),
                '-ar', str(self.config.sample_rate),
                '-y',
                output_file
            ]
            
            subprocess.run(conversion_command, check=True, capture_output=True)
            
            # Clean up original downloaded file
            if os.path.exists(downloaded_file):
                os.remove(downloaded_file)
            
            return output_file
            
        except subprocess.CalledProcessError as e:
            raise DownloadError(f"Audio conversion failed: {e.stderr.decode()}")
        except Exception as e:
            raise DownloadError(f"Download failed: {str(e)}")
    
    def cleanup(self):
        """Clean up temporary files"""
        if os.path.exists(self.config.temp_audio_file):
            os.remove(self.config.temp_audio_file)