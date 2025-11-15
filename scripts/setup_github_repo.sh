#!/bin/bash
# Jukeyman Autonomous Media Station (JAMS) - GitHub Repository Setup Script
# This script helps you create and push to GitHub

set -e

echo "🚀 JAMS (Jukeyman Autonomous Media Station) - GitHub Repository Setup"
echo "====================================================================="
echo ""

# Configuration
GITHUB_TOKEN="${GITHUB_TOKEN:-your_github_personal_access_token_here}"
REPO_NAME="jams"
REPO_OWNER="rjbizsolution23-wq"
REPO_DESCRIPTION="Jukeyman Autonomous Media Station (JAMS) - The World's Most Advanced Multi-Tenant AI Content Generation Platform - Built by RJ Business Solutions"
REPO_URL="https://github.com/${REPO_OWNER}/${REPO_NAME}.git"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}Step 1: Checking Git Status${NC}"
if [ ! -d ".git" ]; then
    echo "Initializing Git repository..."
    git init
    git branch -M main
else
    echo "Git repository already initialized"
fi

echo ""
echo -e "${BLUE}Step 2: Adding All Files${NC}"
git add .

echo ""
echo -e "${BLUE}Step 3: Creating Initial Commit${NC}"
git commit -m "feat: Initial release of Jukeyman Autonomous Media Station (JAMS) v1.0.0

- Complete multi-tenant AI content generation platform
- 100-agent swarm system across 10 departments
- 12+ integrated AI engines (ComfyUI, Open-Sora, Coqui TTS, etc.)
- Enterprise-grade security with Row-Level Security
- Cloudflare R2 storage and CDN integration
- Stripe payment processing
- Production-ready Docker deployment
- Comprehensive documentation

Built by RJ Business Solutions
Architect: Rick Jefferson - AI Systems Architect"

echo ""
echo -e "${YELLOW}Step 4: Creating GitHub Repository${NC}"
echo "Repository will be created at: ${REPO_URL}"
echo ""

# Create repository using GitHub API
RESPONSE=$(curl -s -X POST \
  -H "Authorization: token ${GITHUB_TOKEN}" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/user/repos \
  -d "{
    \"name\": \"${REPO_NAME}\",
    \"description\": \"${REPO_DESCRIPTION}\",
    \"private\": false,
    \"has_issues\": true,
    \"has_projects\": true,
    \"has_wiki\": true,
    \"has_downloads\": true,
    \"auto_init\": false
  }")

# Check if repo was created or already exists
if echo "$RESPONSE" | grep -q "already exists"; then
    echo -e "${YELLOW}Repository already exists. Continuing...${NC}"
elif echo "$RESPONSE" | grep -q "Bad credentials"; then
    echo -e "${YELLOW}⚠️  GitHub token may be invalid. Please check and update the token in this script.${NC}"
    echo "You can still push manually:"
    echo "  git remote add origin ${REPO_URL}"
    echo "  git push -u origin main"
    exit 1
else
    echo -e "${GREEN}✅ Repository created successfully!${NC}"
fi

echo ""
echo -e "${BLUE}Step 5: Adding Remote Origin${NC}"
if git remote | grep -q "origin"; then
    echo "Remote 'origin' already exists. Updating..."
    git remote set-url origin ${REPO_URL}
else
    git remote add origin ${REPO_URL}
fi

echo ""
echo -e "${BLUE}Step 6: Pushing to GitHub${NC}"
echo "This will push all files to GitHub..."
echo ""

read -p "Do you want to push now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    git push -u origin main
    echo ""
    echo -e "${GREEN}✅ Successfully pushed to GitHub!${NC}"
    echo ""
    echo "Repository URL: ${REPO_URL}"
    echo ""
    echo "Next steps:"
    echo "1. Visit ${REPO_URL}"
    echo "2. Enable GitHub Pages in repository settings"
    echo "3. Configure GitHub Actions for CI/CD"
    echo "4. Add repository topics: ai, content-generation, fastapi, multi-tenant, uncensored"
else
    echo "Skipping push. You can push manually later with:"
    echo "  git push -u origin main"
fi

echo ""
echo -e "${GREEN}✅ GitHub repository setup complete!${NC}"
echo ""
echo "Repository Details:"
echo "==================="
echo "Name: ${REPO_NAME}"
echo "Owner: ${REPO_OWNER}"
echo "URL: ${REPO_URL}"
echo "Description: ${REPO_DESCRIPTION}"
echo ""
echo "To enable GitHub Pages:"
echo "1. Go to Settings > Pages"
echo "2. Select 'main' branch and '/docs' folder"
echo "3. Save and visit: https://${REPO_OWNER}.github.io/${REPO_NAME}/"

