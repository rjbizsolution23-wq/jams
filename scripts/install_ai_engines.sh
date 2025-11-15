#!/bin/bash
# Jukeyman Autonomous Media Station (JAMS) - Install All AI Generation Engines
# Run this after install_infrastructure.sh

set -e

echo "🤖 JAMS (Jukeyman Autonomous Media Station) - Installing AI Generation Engines"
echo "============================================================================="

cd ~/jams

# Clone all repositories
echo "📥 Cloning AI generation repositories..."

# Image Generation
echo "🖼️ Installing Image Generation Engines..."
[ ! -d "ComfyUI" ] && git clone https://github.com/comfyanonymous/ComfyUI.git || echo "✅ ComfyUI already cloned"
[ ! -d "stable-diffusion-webui" ] && git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git || echo "✅ AUTOMATIC1111 already cloned"

# Video Generation
echo "🎬 Installing Video Generation Engines..."
[ ! -d "Open-Sora" ] && git clone https://github.com/hpcaitech/Open-Sora.git || echo "✅ Open-Sora already cloned"
[ ! -d "generative-models" ] && git clone https://github.com/Stability-AI/generative-models.git || echo "✅ Stable Video Diffusion already cloned"
[ ! -d "AnimateDiff" ] && git clone https://github.com/guoyww/AnimateDiff.git || echo "✅ AnimateDiff already cloned"

# Audio/Voice Generation
echo "🎙️ Installing Audio/Voice Generation Engines..."
[ ! -d "TTS" ] && git clone https://github.com/coqui-ai/TTS.git || echo "✅ Coqui TTS already cloned"
[ ! -d "audiocraft" ] && git clone https://github.com/facebookresearch/audiocraft.git || echo "✅ AudioCraft already cloned"
[ ! -d "bark" ] && git clone https://github.com/suno-ai/bark.git || echo "✅ Bark already cloned"

# Post-Production
echo "✨ Installing Post-Production Tools..."
[ ! -d "Real-ESRGAN" ] && git clone https://github.com/xinntao/Real-ESRGAN.git || echo "✅ Real-ESRGAN already cloned"
[ ! -d "Wav2Lip" ] && git clone https://github.com/Rudrabha/Wav2Lip.git || echo "✅ Wav2Lip already cloned"

# LLM
echo "🧠 Installing LLM Engines..."
[ ! -d "llama.cpp" ] && git clone https://github.com/ggerganov/llama.cpp.git || echo "✅ llama.cpp already cloned"
[ ! -d "text-generation-webui" ] && git clone https://github.com/oobabooga/text-generation-webui.git || echo "✅ Text-Gen-WebUI already cloned"

# Install ComfyUI
echo ""
echo "🎨 Setting up ComfyUI..."
cd ~/jams/ComfyUI
python3.11 -m pip install -r requirements.txt
mkdir -p models/checkpoints models/loras models/controlnet models/vae models/upscale_models

# Install ComfyUI custom nodes
echo "📦 Installing ComfyUI custom nodes..."
cd custom_nodes
[ ! -d "ComfyUI-AnimateDiff-Evolved" ] && git clone https://github.com/Kosinkadink/ComfyUI-AnimateDiff-Evolved.git || echo "✅ AnimateDiff node already installed"
[ ! -d "ComfyUI-Manager" ] && git clone https://github.com/ltdrdata/ComfyUI-Manager.git || echo "✅ ComfyUI-Manager already installed"
cd ..

# Install Coqui TTS
echo ""
echo "🎤 Setting up Coqui TTS..."
cd ~/jams/TTS
python3.11 -m pip install -e .

# Install AudioCraft
echo ""
echo "🎵 Setting up AudioCraft..."
cd ~/jams/audiocraft
python3.11 -m pip install -e .

# Install Bark
echo ""
echo "🐕 Setting up Bark..."
cd ~/jams/bark
python3.11 -m pip install -e .

# Install Real-ESRGAN
echo ""
echo "🚀 Setting up Real-ESRGAN..."
cd ~/jams/Real-ESRGAN
python3.11 -m pip install basicsr facexlib gfpgan realesrgan
python3.11 -m pip install -r requirements.txt
python3.11 setup.py develop

# Install Wav2Lip
echo ""
echo "💋 Setting up Wav2Lip..."
cd ~/jams/Wav2Lip
python3.11 -m pip install -r requirements.txt

# Build llama.cpp with CUDA support
echo ""
echo "🦙 Building llama.cpp with CUDA..."
cd ~/jams/llama.cpp
make clean
make LLAMA_CUBLAS=1 -j$(nproc)

# Install Open-Sora
echo ""
echo "📹 Setting up Open-Sora..."
cd ~/jams/Open-Sora
python3.11 -m pip install -e .

# Install Stable Video Diffusion
echo ""
echo "🎞️ Setting up Stable Video Diffusion..."
cd ~/jams/generative-models
python3.11 -m pip install -e .

# Install AnimateDiff
echo ""
echo "🎭 Setting up AnimateDiff..."
cd ~/jams/AnimateDiff
python3.11 -m pip install -r requirements.txt

# Install MoviePy for video editing
echo ""
echo "🎬 Installing MoviePy..."
python3.11 -m pip install moviepy

# Install additional Python packages
echo ""
echo "📦 Installing additional Python packages..."
python3.11 -m pip install \
    torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121 \
    transformers \
    diffusers \
    accelerate \
    xformers \
    opencv-python \
    pillow \
    numpy \
    scipy \
    librosa \
    soundfile

echo ""
echo "✅ AI Generation Engines Installation Complete!"
echo ""
echo "Installed Engines:"
echo "=================="
echo "✅ ComfyUI (SDXL/FLUX image generation)"
echo "✅ AUTOMATIC1111 (backup image generation)"
echo "✅ Open-Sora (text-to-video)"
echo "✅ Stable Video Diffusion (image-to-video)"
echo "✅ AnimateDiff (video animation)"
echo "✅ Coqui TTS (voice cloning)"
echo "✅ AudioCraft (music/SFX)"
echo "✅ Bark (expressive voice)"
echo "✅ Real-ESRGAN (4K upscaling)"
echo "✅ Wav2Lip (lip sync)"
echo "✅ llama.cpp (uncensored LLMs)"
echo "✅ MoviePy (video editing)"
echo ""
echo "Next step: Run scripts/download_models.sh to download AI models"

