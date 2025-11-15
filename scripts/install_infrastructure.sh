#!/bin/bash
# Jukeyman Autonomous Media Station (JAMS) - Infrastructure Setup Script
# Run this on a fresh Ubuntu 22.04 GPU server

set -e

echo "🚀 JAMS (Jukeyman Autonomous Media Station) - Infrastructure Setup"
echo "==================================================================="

# Update system
echo "📦 Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install essential tools
echo "🔧 Installing essential tools..."
sudo apt-get install -y \
    wget \
    curl \
    git \
    build-essential \
    software-properties-common \
    apt-transport-https \
    ca-certificates \
    gnupg \
    lsb-release

# Install NVIDIA drivers and CUDA 12.1
echo "🎮 Installing NVIDIA drivers and CUDA 12.1..."
if ! command -v nvidia-smi &> /dev/null; then
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.0-1_all.deb
    sudo dpkg -i cuda-keyring_1.0-1_all.deb
    sudo apt-get update
    sudo apt-get -y install cuda-12-1
    echo 'export PATH=/usr/local/cuda-12.1/bin:$PATH' >> ~/.bashrc
    echo 'export LD_LIBRARY_PATH=/usr/local/cuda-12.1/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
    source ~/.bashrc
else
    echo "✅ NVIDIA drivers already installed"
    nvidia-smi
fi

# Install Docker
echo "🐳 Installing Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    echo "✅ Docker installed. You may need to log out and back in for group changes."
else
    echo "✅ Docker already installed"
    docker --version
fi

# Install Docker Compose
echo "📦 Installing Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
else
    echo "✅ Docker Compose already installed"
    docker-compose --version
fi

# Install NVIDIA Container Toolkit
echo "🎮 Installing NVIDIA Container Toolkit..."
if ! command -v nvidia-container-toolkit &> /dev/null; then
    distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
    curl -s -L https://nvidia.github.io/libnvidia-container/gpgkey | sudo apt-key add -
    curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
    sudo apt-get update
    sudo apt-get install -y nvidia-container-toolkit
    sudo systemctl restart docker
else
    echo "✅ NVIDIA Container Toolkit already installed"
fi

# Install Python 3.11
echo "🐍 Installing Python 3.11..."
if ! command -v python3.11 &> /dev/null; then
    sudo add-apt-repository -y ppa:deadsnakes/ppa
    sudo apt-get update
    sudo apt-get install -y python3.11 python3.11-venv python3.11-dev python3-pip
    sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
else
    echo "✅ Python 3.11 already installed"
    python3.11 --version
fi

# Install pip for Python 3.11
sudo curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11

# Install Node.js 20 (for Next.js frontends)
echo "📗 Installing Node.js 20..."
if ! command -v node &> /dev/null; then
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
    sudo apt-get install -y nodejs
else
    echo "✅ Node.js already installed"
    node --version
fi

# Install FFmpeg (for video processing)
echo "🎬 Installing FFmpeg..."
sudo apt-get install -y ffmpeg

# Install PostgreSQL client tools
echo "🐘 Installing PostgreSQL client..."
sudo apt-get install -y postgresql-client

# Install Cloudflare Tunnel
echo "☁️ Installing Cloudflare Tunnel..."
if ! command -v cloudflared &> /dev/null; then
    wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
    sudo dpkg -i cloudflared-linux-amd64.deb
else
    echo "✅ Cloudflare Tunnel already installed"
    cloudflared --version
fi

# Create project directory
echo "📁 Creating project directory..."
mkdir -p ~/jams
cd ~/jams

echo ""
echo "✅ Infrastructure setup complete!"
echo ""
echo "Next steps:"
echo "1. Log out and back in for Docker group changes to take effect"
echo "2. Run scripts/install_ai_engines.sh to install AI generation engines"
echo "3. Configure Cloudflare Tunnel with your credentials"
echo ""
echo "System Information:"
echo "==================="
python3.11 --version
docker --version
docker-compose --version
node --version
nvidia-smi | head -n 10

