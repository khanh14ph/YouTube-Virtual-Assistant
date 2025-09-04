# 🎬 YouTube Virtual Assistant

An AI-powered assistant that processes YouTube videos to extract transcripts and answer questions about the content using Voice Activity Detection (VAD), Automatic Speech Recognition (ASR), and Large Language Models (LLM).

## ✨ Features

- **🎥 YouTube Video Processing**: Download and process audio from YouTube URLs
- **🗣️ Voice Activity Detection**: Identify speech segments in audio
- **📝 Speech Recognition**: Convert speech to text with timestamps
- **🤖 AI Q&A**: Ask questions about video content using local or cloud LLMs
- **🎨 Modern GUI**: Clean Streamlit interface with real-time chat
- **⚙️ Flexible Configuration**: Support for multiple LLM backends

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/your-username/YouTube-Virtual-Assistant.git
cd YouTube-Virtual-Assistant

# Install dependencies
pip install streamlit torch transformers yt-dlp soundfile numpy requests

# For OpenAI support
pip install openai>=1.0.0
```

### 2. Set up LLM Service

Choose one of the following options:

#### Option A: OpenAI (Easiest)
```bash
export OPENAI_API_KEY="your-api-key-here"
```

#### Option B: Local LLM (Recommended)
```bash
cd local_llm_setup
./quick_start.sh
# Follow the interactive setup
```

### 3. Run the Application

#### GUI Mode (Recommended)
```bash
python -m src.main gui
```
Open http://localhost:8501 in your browser.

#### CLI Mode
```bash
# Interactive mode
python -m src.main cli "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Non-interactive (just transcript)
python -m src.main cli "https://youtube.com/watch?v=..." --non-interactive
```

## 📋 Usage Guide

### Using the GUI

1. **Configure LLM Service:**
   - Open sidebar
   - Choose "openai" or "local"
   - Enter API key or local server details
   - Click "Initialize Assistant"

2. **Process Video:**
   - Paste YouTube URL
   - Click "Process Video"
   - Wait for transcription (may take a few minutes)

3. **Ask Questions:**
   - Use the chat interface
   - Ask about video content
   - Get AI-powered responses

### Using the CLI

```bash
# With OpenAI
OPENAI_API_KEY="sk-..." python -m src.main cli "https://youtube.com/watch?v=..." --llm-type openai

# With local LLM
python -m src.main cli "https://youtube.com/watch?v=..." --llm-type local
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file:

```bash
# LLM Configuration
OPENAI_API_KEY=your-openai-key
LLM_BASE_URL=http://localhost:11434  # For local LLM
LLM_MODEL=llama2:7b

# Audio Settings
SAMPLE_RATE=16000
ASR_MODEL=nguyenvulebinh/wav2vec2-base-vietnamese-250h

# Processing
NUM_PROCESSES=4
BEAM_WIDTH=50
```

### LLM Backend Options

| Backend | Setup | Configuration |
|---------|--------|---------------|
| **OpenAI** | Get API key from [OpenAI](https://platform.openai.com/api-keys) | `LLM_SERVICE=openai`, `OPENAI_API_KEY=sk-...` |
| **Ollama** | Run `./local_llm_setup/ollama_setup.sh` | `LLM_BASE_URL=http://localhost:11434`, `LLM_MODEL=llama2:7b` |
| **LM Studio** | Download from [lmstudio.ai](https://lmstudio.ai) | `LLM_BASE_URL=http://localhost:1234`, `LLM_MODEL=local-model` |

## 🔧 Advanced Setup

### Local LLM with Ollama

1. **Automatic Setup:**
   ```bash
   cd local_llm_setup
   ./ollama_setup.sh
   ```

2. **Manual Setup:**
   ```bash
   # Install Ollama
   brew install ollama  # macOS
   # or curl -fsSL https://ollama.ai/install.sh | sh  # Linux
   
   # Start service
   ollama serve
   
   # Pull model
   ollama pull llama2:7b
   ```

3. **Test Setup:**
   ```bash
   cd local_llm_setup
   ./test_llm.sh
   ```

### Docker Deployment

```bash
cd local_llm_setup

# Start Ollama container
docker-compose --profile ollama up -d

# Or advanced WebUI
docker-compose --profile webui up -d
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Import Errors
```bash
# Fix relative imports
export PYTHONPATH=$PWD:$PYTHONPATH
```

#### 2. CUDA/GPU Issues
```bash
# Check CUDA availability
python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"
```

#### 3. YouTube Download Issues
```bash
# Update yt-dlp
pip install --upgrade yt-dlp
```

#### 4. LLM Connection Issues
```bash
# Test local LLM
curl http://localhost:11434/api/version  # Ollama
curl http://localhost:1234/v1/models    # LM Studio
```

### Error Solutions

| Error | Solution |
|-------|----------|
| `ModuleNotFoundError` | Install missing dependencies: `pip install package-name` |
| `Connection refused` | Ensure LLM server is running |
| `CUDA out of memory` | Use CPU or smaller model |
| `Rate limit exceeded` | Check OpenAI API limits |
| `openai.ChatCompletion` not supported | Update OpenAI: `pip install openai>=1.0.0` |
| `Failed to generate response` | Check API key and model name |

## 📁 Project Structure

```
YouTube-Virtual-Assistant/
├── src/
│   ├── core/
│   │   ├── config.py          # Configuration management
│   │   ├── exceptions.py      # Custom exceptions
│   │   └── video_processor.py # Main processing pipeline
│   ├── services/
│   │   ├── downloader.py      # YouTube downloader
│   │   ├── vad_service.py     # Voice Activity Detection
│   │   ├── asr_service.py     # Speech Recognition
│   │   └── llm_service.py     # LLM integration
│   ├── gui/
│   │   └── streamlit_app.py   # Web interface
│   ├── utils/
│   │   └── logging_utils.py   # Logging utilities
│   └── main.py                # Main entry point
├── local_llm_setup/           # LLM setup scripts
├── main.py                    # Legacy compatibility
└── README.md                  # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🆘 Support

- **Issues**: Report bugs on [GitHub Issues](https://github.com/your-username/YouTube-Virtual-Assistant/issues)
- **Documentation**: Check `/local_llm_setup/README.md` for LLM setup details
- **Testing**: Use `./local_llm_setup/test_llm.sh` to verify configuration

## 🏷️ Version

Current version: 2.0.0 (Refactored Architecture)

---

**Happy video processing!** 🎬✨
