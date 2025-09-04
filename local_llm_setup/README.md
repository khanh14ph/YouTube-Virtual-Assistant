# Local LLM Setup Guide

This guide helps you set up a local LLM service that works with the YouTube Virtual Assistant.

## Quick Start Options

### Option 1: Ollama (Recommended - Easiest)
1. **Install Ollama:**
   ```bash
   # macOS
   brew install ollama
   
   # Or download from: https://ollama.ai
   ```

2. **Start Ollama service:**
   ```bash
   ollama serve
   ```

3. **Pull a model:**
   ```bash
   # Lightweight model (7B parameters)
   ollama pull llama2:7b
   
   # Or a more capable model
   ollama pull llama2:13b
   ```

4. **Configure YouTube Assistant:**
   - LLM Service: `local`
   - Base URL: `http://localhost:11434`
   - Model: `llama2:7b`

### Option 2: LM Studio (GUI Interface)
1. **Download LM Studio:** https://lmstudio.ai
2. **Install and open LM Studio**
3. **Download a model from the browser tab**
4. **Start local server:**
   - Go to "Local Server" tab
   - Click "Start Server"
   - Note the port (usually 1234)

5. **Configure YouTube Assistant:**
   - LLM Service: `local`
   - Base URL: `http://localhost:1234`
   - Model: `local-model`

### Option 3: OpenAI-Compatible Server (Advanced)
Use the provided Docker setup or manual installation scripts.

## Configuration Examples

### For Ollama:
```bash
export LLM_BASE_URL="http://localhost:11434"
export LLM_MODEL="llama2:7b"
```

### For LM Studio:
```bash
export LLM_BASE_URL="http://localhost:1234" 
export LLM_MODEL="local-model"
```

## Troubleshooting

### Common Issues:
1. **Connection refused:** Make sure your LLM server is running
2. **Model not found:** Ensure the model name matches what you downloaded
3. **Slow responses:** Try a smaller model or increase timeout

### Test your setup:
```bash
# Test Ollama
curl http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "llama2:7b", "messages": [{"role": "user", "content": "Hello!"}]}'

# Test LM Studio  
curl http://localhost:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "local-model", "messages": [{"role": "user", "content": "Hello!"}]}'
```

## Next Steps

1. Choose your preferred option above
2. Start the LLM service
3. Run the YouTube Assistant: `python -m src.main gui`
4. Configure the LLM settings in the sidebar
5. Test with a short YouTube video

For more detailed setup instructions, see the specific guides in this folder.