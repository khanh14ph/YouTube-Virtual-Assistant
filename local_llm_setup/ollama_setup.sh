#!/bin/bash

# Ollama Setup Script for YouTube Virtual Assistant
# This script automates the Ollama installation and setup process

set -e

echo "🚀 Setting up Ollama for YouTube Virtual Assistant..."

# Check if running on macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "📱 Detected macOS"
    
    # Check if Homebrew is installed
    if ! command -v brew &> /dev/null; then
        echo "❌ Homebrew not found. Please install Homebrew first:"
        echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
        exit 1
    fi
    
    # Install Ollama
    echo "📦 Installing Ollama via Homebrew..."
    brew install ollama
    
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "🐧 Detected Linux"
    
    # Install Ollama for Linux
    echo "📦 Installing Ollama..."
    curl -fsSL https://ollama.ai/install.sh | sh
    
else
    echo "❌ Unsupported operating system: $OSTYPE"
    echo "Please visit https://ollama.ai for manual installation"
    exit 1
fi

echo "✅ Ollama installed successfully!"

# Start Ollama service in background
echo "🔧 Starting Ollama service..."
ollama serve &
OLLAMA_PID=$!

# Wait a moment for service to start
sleep 5

# Pull recommended model
echo "📥 Downloading recommended model (llama2:7b)..."
echo "This may take a while depending on your internet connection..."
ollama pull llama2:7b

echo "🎉 Setup complete!"
echo ""
echo "📋 Configuration for YouTube Virtual Assistant:"
echo "   LLM Service: local"
echo "   Base URL: http://localhost:11434"
echo "   Model: llama2:7b"
echo ""
echo "🔧 Environment variables (optional):"
echo "   export LLM_BASE_URL=\"http://localhost:11434\""
echo "   export LLM_MODEL=\"llama2:7b\""
echo ""
echo "🧪 Test your setup:"
echo "   ./test_llm.sh"
echo ""
echo "⚠️  Note: Ollama service is running in background (PID: $OLLAMA_PID)"
echo "   To stop: kill $OLLAMA_PID"
echo "   To restart: ollama serve"