#!/bin/bash
# Jukeyman Autonomous Media Station (JAMS) - Start All Services
# Run this after installation and configuration

set -e

echo "🚀 JAMS (Jukeyman Autonomous Media Station) - Starting All Services"
echo "==================================================================="

cd ~/jams

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ Error: .env file not found"
    echo "Please copy .env.example to .env and configure it"
    exit 1
fi

# Load environment variables
source .env

echo "📦 Starting Docker services..."
docker-compose up -d postgres redis
sleep 10

echo "✅ Database and Redis started"

echo ""
echo "🤖 Starting AI Services (in background)..."

# Start ComfyUI
cd ~/jams/ComfyUI
nohup python main.py --listen 0.0.0.0 --port 8188 > /tmp/comfyui.log 2>&1 &
echo $! > /tmp/comfyui.pid
echo "✅ ComfyUI started (PID: $(cat /tmp/comfyui.pid))"

# Start llama.cpp
cd ~/jams/llama.cpp
nohup ./server \
    -m models/dolphin-2.6-mistral-7b.Q5_K_M.gguf \
    --host 0.0.0.0 \
    --port 8080 \
    --ctx-size 4096 \
    > /tmp/llama-cpp.log 2>&1 &
echo $! > /tmp/llama-cpp.pid
echo "✅ llama.cpp started (PID: $(cat /tmp/llama-cpp.pid))"

# Start Coqui TTS
cd ~/jams/TTS
nohup tts-server --model_name tts_models/multilingual/multi-dataset/xtts_v2 --port 5002 \
    > /tmp/tts.log 2>&1 &
echo $! > /tmp/tts.pid
echo "✅ Coqui TTS started (PID: $(cat /tmp/tts.pid))"

# Wait for AI services to be ready
echo ""
echo "⏳ Waiting for AI services to be ready..."
sleep 15

# Start backend services
cd ~/jams
echo ""
echo "🔧 Starting Backend services..."
docker-compose up -d backend celery-worker celery-flower n8n prometheus grafana

echo ""
echo "✅ All services started!"
echo ""
echo "📊 Service Status:"
echo "=================="
docker-compose ps

echo ""
echo "🌐 Access URLs:"
echo "==============="
echo "Backend API:      http://localhost:8000"
echo "API Docs:         http://localhost:8000/docs"
echo "ComfyUI:          http://localhost:8188"
echo "llama.cpp:        http://localhost:8080"
echo "Coqui TTS:        http://localhost:5002"
echo "Celery Flower:    http://localhost:5555"
echo "n8n:              http://localhost:5678"
echo "Prometheus:       http://localhost:9090"
echo "Grafana:          http://localhost:3002"
echo ""
echo "📝 Logs:"
echo "========"
echo "ComfyUI:          tail -f /tmp/comfyui.log"
echo "llama.cpp:        tail -f /tmp/llama-cpp.log"
echo "Coqui TTS:        tail -f /tmp/tts.log"
echo "Backend:          docker-compose logs -f backend"
echo "Celery:           docker-compose logs -f celery-worker"
echo ""
echo "🛑 To stop all services: ./scripts/stop_all_services.sh"
echo ""
echo "✨ JAMS (Jukeyman Autonomous Media Station) is ready!"

