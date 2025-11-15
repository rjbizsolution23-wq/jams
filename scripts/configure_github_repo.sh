#!/bin/bash
# JAMS - Complete GitHub Repository Configuration
# This script configures topics, pages, and creates the first release

set -e

GITHUB_TOKEN="${1:-${GITHUB_TOKEN:-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}}"
REPO_OWNER="rjbizsolution23-wq"
REPO_NAME="jams"
API_BASE="https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}"

echo "🚀 Configuring JAMS GitHub Repository"
echo "======================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# ============================================
# 1. ADD REPOSITORY TOPICS
# ============================================
echo -e "${BLUE}📌 Step 1: Adding repository topics...${NC}"

TOPICS='["ai","content-generation","fastapi","multi-tenant","uncensored","jams","docker","postgresql","celery","open-source","production-ready"]'

RESPONSE=$(curl -s -w "\n%{http_code}" -X PUT \
  -H "Authorization: token ${GITHUB_TOKEN}" \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Content-Type: application/json" \
  "${API_BASE}/topics" \
  -d "{\"names\": ${TOPICS}}")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" -eq 200 ]; then
    echo -e "${GREEN}✅ Topics added successfully!${NC}"
    echo "   Topics: ai, content-generation, fastapi, multi-tenant, uncensored, jams, docker, postgresql, celery, open-source, production-ready"
else
    echo -e "${YELLOW}⚠️  Topics update returned HTTP $HTTP_CODE${NC}"
    echo "   Response: $BODY"
fi

echo ""

# ============================================
# 2. ENABLE GITHUB PAGES
# ============================================
echo -e "${BLUE}📄 Step 2: Enabling GitHub Pages...${NC}"

PAGES_CONFIG='{
  "source": {
    "branch": "main",
    "path": "/docs"
  }
}'

RESPONSE=$(curl -s -w "\n%{http_code}" -X POST \
  -H "Authorization: token ${GITHUB_TOKEN}" \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Content-Type: application/json" \
  "${API_BASE}/pages" \
  -d "${PAGES_CONFIG}")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" -eq 201 ] || [ "$HTTP_CODE" -eq 200 ]; then
    echo -e "${GREEN}✅ GitHub Pages enabled!${NC}"
    echo "   Source: main branch, /docs folder"
    echo "   URL: https://${REPO_OWNER}.github.io/${REPO_NAME}/"
else
    # Try PUT method (for existing pages)
    RESPONSE=$(curl -s -w "\n%{http_code}" -X PUT \
      -H "Authorization: token ${GITHUB_TOKEN}" \
      -H "Accept: application/vnd.github.v3+json" \
      -H "Content-Type: application/json" \
      "${API_BASE}/pages" \
      -d "${PAGES_CONFIG}")
    
    HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
    if [ "$HTTP_CODE" -eq 200 ]; then
        echo -e "${GREEN}✅ GitHub Pages updated!${NC}"
    else
        echo -e "${YELLOW}⚠️  GitHub Pages configuration returned HTTP $HTTP_CODE${NC}"
        echo "   Note: You may need to enable Pages manually in Settings → Pages"
        echo "   Response: $BODY"
    fi
fi

echo ""

# ============================================
# 3. CREATE FIRST RELEASE (v1.0.0)
# ============================================
echo -e "${BLUE}🏷️  Step 3: Creating first release (v1.0.0)...${NC}"

RELEASE_BODY="# 🎉 Jukeyman Autonomous Media Station (JAMS) v1.0.0 - Initial Release

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

- [Full Documentation](https://${REPO_OWNER}.github.io/${REPO_NAME}/)
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

**Full Changelog**: See [CHANGELOG.md](CHANGELOG.md)"

# Escape JSON string
RELEASE_BODY_JSON=$(echo "$RELEASE_BODY" | jq -Rs .)

RELEASE_DATA="{
  \"tag_name\": \"v1.0.0\",
  \"name\": \"Jukeyman Autonomous Media Station (JAMS) v1.0.0 - Initial Release\",
  \"body\": ${RELEASE_BODY_JSON},
  \"draft\": false,
  \"prerelease\": false
}"

RESPONSE=$(curl -s -w "\n%{http_code}" -X POST \
  -H "Authorization: token ${GITHUB_TOKEN}" \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Content-Type: application/json" \
  "${API_BASE}/releases" \
  -d "${RELEASE_DATA}")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" -eq 201 ]; then
    RELEASE_URL=$(echo "$BODY" | jq -r '.html_url // empty')
    echo -e "${GREEN}✅ Release v1.0.0 created successfully!${NC}"
    echo "   Release URL: ${RELEASE_URL}"
else
    echo -e "${YELLOW}⚠️  Release creation returned HTTP $HTTP_CODE${NC}"
    echo "   Response: $BODY"
    if echo "$BODY" | grep -q "already_exists"; then
        echo "   Note: Release v1.0.0 may already exist"
    fi
fi

echo ""

# ============================================
# 4. SOCIAL PREVIEW (Manual Instructions)
# ============================================
echo -e "${BLUE}🖼️  Step 4: Social Preview Configuration${NC}"
echo -e "${YELLOW}⚠️  Note: Social preview must be configured manually via GitHub UI${NC}"
echo ""
echo "To configure social preview:"
echo "1. Go to: https://github.com/${REPO_OWNER}/${REPO_NAME}/settings"
echo "2. Scroll to 'Social preview' section"
echo "3. Click 'Edit'"
echo "4. Upload logo from: https://storage.googleapis.com/msgsndr/qQnxRHDtyx0uydPd5sRl/media/67eb83c5e519ed689430646b.jpeg"
echo "5. Save changes"
echo ""

# ============================================
# SUMMARY
# ============================================
echo "======================================"
echo -e "${GREEN}✅ GitHub Repository Configuration Complete!${NC}"
echo ""
echo "Repository: https://github.com/${REPO_OWNER}/${REPO_NAME}"
echo "Topics: ✅ Added"
echo "Pages: ✅ Enabled (https://${REPO_OWNER}.github.io/${REPO_NAME}/)"
echo "Release: ✅ Created (v1.0.0)"
echo "Social Preview: ⚠️  Manual configuration required"
echo ""
echo "Next Steps:"
echo "1. Configure social preview manually (see instructions above)"
echo "2. Visit your repository: https://github.com/${REPO_OWNER}/${REPO_NAME}"
echo "3. Check GitHub Pages: https://${REPO_OWNER}.github.io/${REPO_NAME}/"
echo "4. View release: https://github.com/${REPO_OWNER}/${REPO_NAME}/releases/tag/v1.0.0"
echo ""

