#!/bin/bash

# Test script for Local LLM services
# Tests both Ollama and LM Studio configurations

echo "🧪 Testing Local LLM Services..."

# Test Ollama (port 11434)
echo ""
echo "1️⃣  Testing Ollama (localhost:11434)..."
if curl -s --max-time 5 http://localhost:11434/api/version > /dev/null; then
    echo "✅ Ollama is running!"
    
    # Test chat completion
    echo "🗣️  Testing chat completion with llama2:7b..."
    OLLAMA_RESPONSE=$(curl -s --max-time 10 http://localhost:11434/v1/chat/completions \
        -H "Content-Type: application/json" \
        -d '{
            "model": "llama2:7b",
            "messages": [{"role": "user", "content": "Hello! Say hi back in one word."}],
            "max_tokens": 10
        }' | jq -r '.choices[0].message.content // "No response"' 2>/dev/null)
    
    if [ "$OLLAMA_RESPONSE" != "No response" ] && [ -n "$OLLAMA_RESPONSE" ]; then
        echo "✅ Ollama chat test successful!"
        echo "   Response: $OLLAMA_RESPONSE"
        echo ""
        echo "📋 Use these settings in YouTube Assistant:"
        echo "   LLM Service: local"
        echo "   Base URL: http://localhost:11434"
        echo "   Model: llama2:7b"
    else
        echo "⚠️  Ollama is running but chat failed. Make sure llama2:7b model is installed:"
        echo "   ollama pull llama2:7b"
    fi
else
    echo "❌ Ollama not running. Start with: ollama serve"
fi

echo ""
echo "2️⃣  Testing LM Studio (localhost:1234)..."
if curl -s --max-time 5 http://localhost:1234/v1/models > /dev/null; then
    echo "✅ LM Studio is running!"
    
    # Test chat completion
    echo "🗣️  Testing chat completion..."
    LM_RESPONSE=$(curl -s --max-time 10 http://localhost:1234/v1/chat/completions \
        -H "Content-Type: application/json" \
        -d '{
            "model": "local-model",
            "messages": [{"role": "user", "content": "Hello! Say hi back in one word."}],
            "max_tokens": 10
        }' | jq -r '.choices[0].message.content // "No response"' 2>/dev/null)
    
    if [ "$LM_RESPONSE" != "No response" ] && [ -n "$LM_RESPONSE" ]; then
        echo "✅ LM Studio chat test successful!"
        echo "   Response: $LM_RESPONSE"
        echo ""
        echo "📋 Use these settings in YouTube Assistant:"
        echo "   LLM Service: local"
        echo "   Base URL: http://localhost:1234"
        echo "   Model: local-model"
    else
        echo "⚠️  LM Studio is running but chat failed. Make sure a model is loaded and server is started."
    fi
else
    echo "❌ LM Studio not running. Open LM Studio and start the local server."
fi

echo ""
echo "3️⃣  Testing OpenAI API (if configured)..."
if [ -n "$OPENAI_API_KEY" ]; then
    echo "🔑 OpenAI API key found, testing connection..."
    OPENAI_RESPONSE=$(curl -s --max-time 10 https://api.openai.com/v1/chat/completions \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $OPENAI_API_KEY" \
        -d '{
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": "Hello! Say hi back in one word."}],
            "max_tokens": 10
        }' | jq -r '.choices[0].message.content // "No response"' 2>/dev/null)
    
    if [ "$OPENAI_RESPONSE" != "No response" ] && [ -n "$OPENAI_RESPONSE" ]; then
        echo "✅ OpenAI API test successful!"
        echo "   Response: $OPENAI_RESPONSE"
        echo ""
        echo "📋 Use these settings in YouTube Assistant:"
        echo "   LLM Service: openai"
        echo "   API Key: [Your API key]"
        echo "   Model: gpt-3.5-turbo"
        echo ""
        echo "💡 Make sure you have the latest OpenAI package:"
        echo "   pip install openai>=1.0.0"
    else
        echo "❌ OpenAI API test failed. Check your API key and network connection."
        echo "💡 Also ensure you have: pip install openai>=1.0.0"
    fi
else
    echo "ℹ️  No OpenAI API key found (set OPENAI_API_KEY to test)"
fi

echo ""
echo "🎯 Summary:"
echo "   Now run: python -m src.main gui"
echo "   Configure LLM settings in the sidebar based on test results above"