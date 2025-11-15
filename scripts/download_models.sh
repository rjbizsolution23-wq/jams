#!/bin/bash
# Jukeyman Autonomous Media Station (JAMS) - Download All AI Models (Uncensored)
# Run this after install_ai_engines.sh
# WARNING: This will download approximately 50GB of models

set -e

echo "📥 JAMS (Jukeyman Autonomous Media Station) - Downloading AI Models"
echo "==================================================================="
echo "⚠️  This will download ~50GB of data"
echo ""

cd ~/jams

# Create model directories
mkdir -p models_storage

# Download Uncensored SDXL Models for ComfyUI
echo "🎨 Downloading Uncensored SDXL Models..."
cd ~/jams/ComfyUI/models/checkpoints

if [ ! -f "RealVisXL_V4.0.safetensors" ]; then
    echo "Downloading RealVisXL V4.0..."
    wget --content-disposition "https://civitai.com/api/download/models/361593" -O RealVisXL_V4.0.safetensors
fi

if [ ! -f "JuggernautXL_v9.safetensors" ]; then
    echo "Downloading JuggernautXL v9..."
    wget --content-disposition "https://civitai.com/api/download/models/456194" -O JuggernautXL_v9.safetensors
fi

if [ ! -f "PonyXL_v6.safetensors" ]; then
    echo "Downloading PonyXL v6 (uncensored anime/realistic)..."
    wget --content-disposition "https://civitai.com/api/download/models/290640" -O PonyXL_v6.safetensors
fi

# Download VAE
echo "📦 Downloading SDXL VAE..."
cd ~/jams/ComfyUI/models/vae
if [ ! -f "sdxl_vae.safetensors" ]; then
    wget https://huggingface.co/stabilityai/sdxl-vae/resolve/main/sdxl_vae.safetensors
fi

# Download Uncensored LLM Models
echo "🧠 Downloading Uncensored LLM Models..."
cd ~/jams/llama.cpp

mkdir -p models

if [ ! -f "models/dolphin-2.6-mistral-7b.Q5_K_M.gguf" ]; then
    echo "Downloading Dolphin 2.6 Mistral 7B (fully uncensored)..."
    wget -O models/dolphin-2.6-mistral-7b.Q5_K_M.gguf \
        "https://huggingface.co/TheBloke/dolphin-2.6-mistral-7B-GGUF/resolve/main/dolphin-2.6-mistral-7b.Q5_K_M.gguf"
fi

if [ ! -f "models/mythomax-l2-13b.Q5_K_M.gguf" ]; then
    echo "Downloading MythoMax L2 13B (uncensored)..."
    wget -O models/mythomax-l2-13b.Q5_K_M.gguf \
        "https://huggingface.co/TheBloke/MythoMax-L2-13B-GGUF/resolve/main/mythomax-l2-13b.Q5_K_M.gguf"
fi

# Download Real-ESRGAN Models
echo "🚀 Downloading Real-ESRGAN Upscaling Models..."
cd ~/jams/Real-ESRGAN/weights

if [ ! -f "RealESRGAN_x4plus.pth" ]; then
    wget https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth
fi

if [ ! -f "RealESRGAN_x4plus_anime_6B.pth" ]; then
    wget https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth
fi

# Download Wav2Lip Models
echo "💋 Downloading Wav2Lip Models..."
cd ~/jams/Wav2Lip/checkpoints

if [ ! -f "wav2lip.pth" ]; then
    echo "Downloading Wav2Lip checkpoint..."
    wget "https://github.com/Rudrabha/Wav2Lip/releases/download/v1.0/wav2lip.pth"
fi

if [ ! -f "wav2lip_gan.pth" ]; then
    echo "Downloading Wav2Lip GAN checkpoint..."
    wget "https://github.com/Rudrabha/Wav2Lip/releases/download/v1.0/wav2lip_gan.pth"
fi

# Download face detection model for Wav2Lip
cd ~/jams/Wav2Lip/face_detection/detection/sfd
if [ ! -f "s3fd.pth" ]; then
    wget "https://www.adrianbulat.com/downloads/python-fan/s3fd-619a316812.pth" -O s3fd.pth
fi

# Download AnimateDiff Motion Modules
echo "🎭 Downloading AnimateDiff Motion Modules..."
cd ~/jams/AnimateDiff
mkdir -p models/Motion_Module

if [ ! -f "models/Motion_Module/mm_sdxl_v10_beta.ckpt" ]; then
    wget -O models/Motion_Module/mm_sdxl_v10_beta.ckpt \
        "https://huggingface.co/guoyww/animatediff/resolve/main/mm_sdxl_v10_beta.ckpt"
fi

# Download ControlNet Models
echo "🎮 Downloading ControlNet Models..."
cd ~/jams/ComfyUI/models/controlnet

if [ ! -f "control_v11p_sd15_openpose.pth" ]; then
    wget https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_openpose.pth
fi

if [ ! -f "control_v11f1p_sd15_depth.pth" ]; then
    wget https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11f1p_sd15_depth.pth
fi

# Download Coqui TTS Models (will auto-download on first use, but we can pre-download)
echo "🎤 Coqui TTS models will auto-download on first use"

# Download AudioCraft Models (will auto-download on first use)
echo "🎵 AudioCraft models will auto-download on first use"

# Download Bark Models (will auto-download on first use)
echo "🐕 Bark models will auto-download on first use"

echo ""
echo "✅ Model Download Complete!"
echo ""
echo "Downloaded Models:"
echo "=================="
echo "✅ RealVisXL V4.0 (uncensored SDXL)"
echo "✅ JuggernautXL v9 (uncensored SDXL)"
echo "✅ PonyXL v6 (uncensored anime/realistic)"
echo "✅ Dolphin 2.6 Mistral 7B (uncensored LLM)"
echo "✅ MythoMax L2 13B (uncensored LLM)"
echo "✅ Real-ESRGAN Upscalers (4x, anime)"
echo "✅ Wav2Lip (lip sync)"
echo "✅ AnimateDiff Motion Modules"
echo "✅ ControlNet Models (pose, depth)"
echo ""
echo "Storage used: ~50GB"
echo ""
echo "Next step: Setup backend with scripts/setup_backend.sh"

