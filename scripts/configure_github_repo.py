#!/usr/bin/env python3
"""
JAMS - Complete GitHub Repository Configuration (Python)
This script configures topics, pages, and creates the first release
"""

import os
import sys
import json
import requests
from typing import Dict, Any

# Configuration
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
REPO_OWNER = "rjbizsolution23-wq"
REPO_NAME = "jams"
API_BASE = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}"

# Headers
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
    "Content-Type": "application/json"
}

# Colors
GREEN = "\033[0;32m"
BLUE = "\033[0;34m"
YELLOW = "\033[1;33m"
RED = "\033[0;31m"
NC = "\033[0m"  # No Color


def print_step(step_num: int, title: str):
    """Print a step header"""
    print(f"\n{BLUE}📌 Step {step_num}: {title}...{NC}")


def print_success(message: str):
    """Print success message"""
    print(f"{GREEN}✅ {message}{NC}")


def print_warning(message: str):
    """Print warning message"""
    print(f"{YELLOW}⚠️  {message}{NC}")


def print_error(message: str):
    """Print error message"""
    print(f"{RED}❌ {message}{NC}")


def add_topics() -> bool:
    """Add repository topics"""
    print_step(1, "Adding repository topics")
    
    topics = [
        "ai",
        "content-generation",
        "fastapi",
        "multi-tenant",
        "uncensored",
        "jams",
        "docker",
        "postgresql",
        "celery",
        "open-source",
        "production-ready"
    ]
    
    url = f"{API_BASE}/topics"
    data = {"names": topics}
    
    try:
        response = requests.put(url, headers=HEADERS, json=data)
        
        if response.status_code == 200:
            print_success("Topics added successfully!")
            print(f"   Topics: {', '.join(topics)}")
            return True
        else:
            print_warning(f"Topics update returned HTTP {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print_error(f"Failed to add topics: {e}")
        return False


def enable_pages() -> bool:
    """Enable GitHub Pages"""
    print_step(2, "Enabling GitHub Pages")
    
    url = f"{API_BASE}/pages"
    data = {
        "source": {
            "branch": "main",
            "path": "/docs"
        }
    }
    
    try:
        # Try POST first (for new pages)
        response = requests.post(url, headers=HEADERS, json=data)
        
        if response.status_code in [200, 201]:
            print_success("GitHub Pages enabled!")
            print(f"   Source: main branch, /docs folder")
            print(f"   URL: https://{REPO_OWNER}.github.io/{REPO_NAME}/")
            return True
        
        # Try PUT (for existing pages)
        if response.status_code == 409:  # Already exists
            response = requests.put(url, headers=HEADERS, json=data)
            if response.status_code == 200:
                print_success("GitHub Pages updated!")
                return True
        
        print_warning(f"GitHub Pages configuration returned HTTP {response.status_code}")
        print("   Note: You may need to enable Pages manually in Settings → Pages")
        print(f"   Response: {response.text}")
        return False
    except Exception as e:
        print_error(f"Failed to enable Pages: {e}")
        return False


def create_release() -> bool:
    """Create first release (v1.0.0)"""
    print_step(3, "Creating first release (v1.0.0)")
    
    release_body = """# 🎉 Jukeyman Autonomous Media Station (JAMS) v1.0.0 - Initial Release

## What's New

- ✅ Complete multi-tenant AI content generation platform
- ✅ 100-agent swarm system across 10 departments
- ✅ 12+ integrated AI engines (ComfyUI, Open-Sora, Coqui TTS, etc.)
- ✅ Enterprise-grade security with Row-Level Security
- ✅ Cloudflare R2 storage and CDN integration
- ✅ Stripe payment processing
- ✅ Production-ready Docker deployment
- ✅ Comprehensive documentation

## Installation

See [README.md](README.md) for installation instructions.

## Documentation

- [Full Documentation](https://rjbizsolution23-wq.github.io/jams/)
- [API Reference](http://localhost:8000/docs)
- [Cloudflare Setup Guide](docs/CLOUDFLARE_SETUP.md)

## Built By

**RJ Business Solutions**  
**Architect: Rick Jefferson - AI Systems Architect**

📞 (505) 502-5054 | 1-877-561-8001  
🌐 [rjbusinesssolutions.org](https://rjbusinesssolutions.org/)

---

## Technical Highlights

### Multi-Tenant Architecture
- PostgreSQL with Row-Level Security (RLS)
- Complete tenant isolation
- Scalable to thousands of tenants

### AI Generation Engines
- **Image**: ComfyUI (SDXL), Stable Diffusion
- **Video**: Open-Sora, Stable Video Diffusion, CogVideo
- **Audio**: Coqui TTS (XTTS-v2), AudioCraft, Bark
- **Text**: LocalGPT, GPT4All, llama.cpp

### Post-Production
- Real-ESRGAN (4x upscaling)
- Wav2Lip (lip sync)
- MoviePy (video editing)

### Infrastructure
- FastAPI backend
- Next.js 15 frontend
- Docker & Docker Compose
- Cloudflare CDN & R2 storage
- Celery task queue
- Redis caching

---

**Full Changelog**: See [CHANGELOG.md](CHANGELOG.md)"""
    
    url = f"{API_BASE}/releases"
    data = {
        "tag_name": "v1.0.0",
        "name": "Jukeyman Autonomous Media Station (JAMS) v1.0.0 - Initial Release",
        "body": release_body,
        "draft": False,
        "prerelease": False
    }
    
    try:
        response = requests.post(url, headers=HEADERS, json=data)
        
        if response.status_code == 201:
            release_data = response.json()
            release_url = release_data.get("html_url", "")
            print_success("Release v1.0.0 created successfully!")
            print(f"   Release URL: {release_url}")
            return True
        else:
            error_msg = response.text
            if "already_exists" in error_msg.lower():
                print_warning("Release v1.0.0 may already exist")
            else:
                print_warning(f"Release creation returned HTTP {response.status_code}")
                print(f"   Response: {error_msg}")
            return False
    except Exception as e:
        print_error(f"Failed to create release: {e}")
        return False


def show_social_preview_instructions():
    """Show instructions for social preview (must be done manually)"""
    print_step(4, "Social Preview Configuration")
    print_warning("Social preview must be configured manually via GitHub UI")
    print()
    print("To configure social preview:")
    print(f"1. Go to: https://github.com/{REPO_OWNER}/{REPO_NAME}/settings")
    print("2. Scroll to 'Social preview' section")
    print("3. Click 'Edit'")
    print("4. Upload logo from: https://storage.googleapis.com/msgsndr/qQnxRHDtyx0uydPd5sRl/media/67eb83c5e519ed689430646b.jpeg")
    print("5. Save changes")


def main():
    """Main function"""
    print("🚀 Configuring JAMS GitHub Repository")
    print("======================================")
    
    # Verify token
    if not GITHUB_TOKEN or GITHUB_TOKEN == "your_github_token_here":
        print_error("GitHub token not set!")
        print("Set GITHUB_TOKEN environment variable or update the script")
        sys.exit(1)
    
    results = {
        "topics": add_topics(),
        "pages": enable_pages(),
        "release": create_release()
    }
    
    show_social_preview_instructions()
    
    # Summary
    print("\n" + "=" * 50)
    print(f"{GREEN}✅ GitHub Repository Configuration Complete!{NC}")
    print()
    print(f"Repository: https://github.com/{REPO_OWNER}/{REPO_NAME}")
    print(f"Topics: {'✅ Added' if results['topics'] else '⚠️  Failed'}")
    print(f"Pages: {'✅ Enabled' if results['pages'] else '⚠️  Failed'}")
    print(f"Release: {'✅ Created' if results['release'] else '⚠️  Failed'}")
    print("Social Preview: ⚠️  Manual configuration required")
    print()
    print("Next Steps:")
    print("1. Configure social preview manually (see instructions above)")
    print(f"2. Visit your repository: https://github.com/{REPO_OWNER}/{REPO_NAME}")
    print(f"3. Check GitHub Pages: https://{REPO_OWNER}.github.io/{REPO_NAME}/")
    print(f"4. View release: https://github.com/{REPO_OWNER}/{REPO_NAME}/releases/tag/v1.0.0")
    print()


if __name__ == "__main__":
    main()

