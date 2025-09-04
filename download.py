import yt_dlp
import os
import subprocess
import argparse

def download(url, output_dir="downloads"):
    os.remove("audio.wav")
    """
    Download YouTube video and convert to mono 16kHz audio
    
    Args:
        url (str): YouTube URL
        output_dir (str): Directory to save files
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # yt-dlp options
    ydl_opts = {
        'format': 'bestaudio/best',  # Select best audio quality
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
        }],
        'quiet': False,
        'no_warnings': True
    }

    try:
        # Download audio using yt-dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            downloaded_file = ydl.prepare_filename(info).replace('.webm', '.wav')
            
        # Convert to mono 16kHz using ffmpeg
        output_file = "audio.wav"
        conversion_command = [
            'ffmpeg', '-i', downloaded_file,
            '-acodec', 'pcm_s16le',  # 16-bit PCM
            '-ac', '1',              # mono
            '-ar', '16000',          # 16kHz sample rate
            '-y',                    # Overwrite output file if exists
            output_file
        ]
        
        subprocess.run(conversion_command, check=True)
        
        # Remove original downloaded file
        os.remove(downloaded_file)
        
        print(f"Successfully downloaded and converted: {output_file}")
        return output_file
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download YouTube video and convert to mono 16kHz audio')
    parser.add_argument('url', help='YouTube URL')
    parser.add_argument('--output-dir', default='downloads', help='Output directory')
    
    args = parser.parse_args()
    download(args.url, args.output_dir)