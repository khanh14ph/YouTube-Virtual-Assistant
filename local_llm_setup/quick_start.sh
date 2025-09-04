#!/bin/bash

# Quick Start Script for Local LLM Setup
# Choose your preferred LLM backend and get started quickly

echo "🎬 YouTube Virtual Assistant - LLM Quick Start"
echo "=============================================="

echo ""
echo "Choose your LLM setup option:"
echo ""
echo "1️⃣  Ollama (Recommended - Easy, Native)"
echo "2️⃣  LM Studio (GUI Interface)" 
echo "3️⃣  Docker Setup (Advanced)"
echo "4️⃣  Test existing setup"
echo "5️⃣  Exit"
echo ""

read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        echo ""
        echo "🚀 Starting Ollama setup..."
        chmod +x ollama_setup.sh
        ./ollama_setup.sh
        ;;
    2)
        echo ""
        echo "📱 LM Studio Setup Instructions:"
        echo ""
        echo "1. Download LM Studio from: https://lmstudio.ai"
        echo "2. Install and open LM Studio"
        echo "3. Go to the search/browse tab and download a model like:"
        echo "   - TheBloke/Llama-2-7b-Chat-GGUF"
        echo "   - Microsoft/DialoGPT-medium"
        echo "4. Go to 'Local Server' tab"
        echo "5. Select your downloaded model"
        echo "6. Click 'Start Server'"
        echo ""
        echo "Then use these settings in YouTube Assistant:"
        echo "   LLM Service: local"
        echo "   Base URL: http://localhost:1234"
        echo "   Model: local-model"
        echo ""
        read -p "Press Enter when you've completed the setup..."
        echo ""
        echo "🧪 Testing LM Studio connection..."
        chmod +x test_llm.sh
        ./test_llm.sh
        ;;
    3)
        echo ""
        echo "🐳 Docker Setup:"
        echo ""
        echo "Available profiles:"
        echo "  - ollama: Docker version of Ollama"
        echo "  - webui: Text Generation WebUI with advanced features"
        echo "  - simple: Simple API server"
        echo ""
        read -p "Enter profile name (ollama/webui/simple): " profile
        
        if [[ "$profile" =~ ^(ollama|webui|simple)$ ]]; then
            echo "Starting Docker setup with profile: $profile"
            docker-compose --profile $profile up -d
            
            if [ "$profile" = "ollama" ]; then
                echo "Waiting for Ollama to start..."
                sleep 5
                echo "Pulling llama2:7b model..."
                docker exec youtube-assistant-ollama ollama pull llama2:7b
                echo ""
                echo "Use these settings:"
                echo "   LLM Service: local"
                echo "   Base URL: http://localhost:11434"  
                echo "   Model: llama2:7b"
            elif [ "$profile" = "webui" ]; then
                echo ""
                echo "Web interface available at: http://localhost:7860"
                echo "API endpoint: http://localhost:5000"
                echo ""
                echo "Use these settings:"
                echo "   LLM Service: local"
                echo "   Base URL: http://localhost:5000"
                echo "   Model: your-model-name"
            else
                echo ""
                echo "API endpoint: http://localhost:8080"
                echo ""
                echo "Use these settings:"
                echo "   LLM Service: local"
                echo "   Base URL: http://localhost:8080"
                echo "   Model: local-model"
            fi
        else
            echo "Invalid profile. Please choose: ollama, webui, or simple"
        fi
        ;;
    4)
        echo ""
        echo "🧪 Testing existing LLM setups..."
        chmod +x test_llm.sh
        ./test_llm.sh
        ;;
    5)
        echo "👋 Goodbye!"
        exit 0
        ;;
    *)
        echo "❌ Invalid choice. Please run the script again."
        exit 1
        ;;
esac

echo ""
echo "🎯 Next steps:"
echo "1. Run: python -m src.main gui"
echo "2. Configure LLM settings in the sidebar"
echo "3. Test with a YouTube video!"
echo ""
echo "💡 Tip: Start with a short (2-3 minute) video for testing"