#!/bin/bash
# Jukeyman Autonomous Media Station (JAMS) - Stop All Services

echo "🛑 JAMS (Jukeyman Autonomous Media Station) - Stopping All Services"
echo "==================================================================="

cd ~/jams

# Stop Docker services
echo "📦 Stopping Docker services..."
docker-compose down

# Stop ComfyUI
if [ -f /tmp/comfyui.pid ]; then
    PID=$(cat /tmp/comfyui.pid)
    if ps -p $PID > /dev/null 2>&1; then
        echo "Stopping ComfyUI (PID: $PID)..."
        kill $PID
        rm /tmp/comfyui.pid
    fi
fi

# Stop llama.cpp
if [ -f /tmp/llama-cpp.pid ]; then
    PID=$(cat /tmp/llama-cpp.pid)
    if ps -p $PID > /dev/null 2>&1; then
        echo "Stopping llama.cpp (PID: $PID)..."
        kill $PID
        rm /tmp/llama-cpp.pid
    fi
fi

# Stop Coqui TTS
if [ -f /tmp/tts.pid ]; then
    PID=$(cat /tmp/tts.pid)
    if ps -p $PID > /dev/null 2>&1; then
        echo "Stopping Coqui TTS (PID: $PID)..."
        kill $PID
        rm /tmp/tts.pid
    fi
fi

echo ""
echo "✅ All services stopped"

