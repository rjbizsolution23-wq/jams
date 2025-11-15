#!/bin/bash
# JAMS - Upload to GitHub Script
# This script will upload the repository to GitHub

set -e

GITHUB_TOKEN="YOUR_GITHUB_PERSONAL_ACCESS_TOKEN"
REPO_NAME="jams"
REPO_OWNER="rickjefferson"
REPO_URL="https://github.com/${REPO_OWNER}/${REPO_NAME}.git"

echo "🚀 Uploading JAMS to GitHub..."
echo "Repository: ${REPO_URL}"
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "Initializing git repository..."
    git init
    git branch -M main
fi

# Check if files are committed
if [ -z "$(git log --oneline 2>/dev/null)" ]; then
    echo "Adding and committing files..."
    git add .
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
fi

# Add remote
echo "Setting up remote..."
git remote remove origin 2>/dev/null || true
git remote add origin ${REPO_URL}

# Try to create repository if it doesn't exist
echo "Checking if repository exists..."
REPO_EXISTS=$(curl -s -o /dev/null -w "%{http_code}" \
  -H "Authorization: token ${GITHUB_TOKEN}" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME})

if [ "$REPO_EXISTS" != "200" ]; then
    echo "Creating repository on GitHub..."
    curl -X POST \
      -H "Authorization: token ${GITHUB_TOKEN}" \
      -H "Accept: application/vnd.github.v3+json" \
      https://api.github.com/user/repos \
      -d "{
        \"name\": \"${REPO_NAME}\",
        \"description\": \"Jukeyman Autonomous Media Station (JAMS) - The World's Most Advanced Multi-Tenant AI Content Generation Platform\",
        \"private\": false,
        \"has_issues\": true,
        \"has_projects\": true,
        \"has_wiki\": true
      }" || echo "Repository may already exist or creation failed"
fi

# Push to GitHub
echo ""
echo "Pushing to GitHub..."
echo "You may be prompted for credentials."
echo "Username: ${REPO_OWNER}"
echo "Password: Use your GitHub Personal Access Token"
echo ""

git push -u origin main || {
    echo ""
    echo "⚠️  Push failed. Trying with token authentication..."
    git remote set-url origin https://${GITHUB_TOKEN}@github.com/${REPO_OWNER}/${REPO_NAME}.git
    git push -u origin main
}

echo ""
echo "✅ Upload complete!"
echo ""
echo "Repository URL: ${REPO_URL}"
echo ""
echo "Next steps:"
echo "1. Visit ${REPO_URL}"
echo "2. Add repository topics: ai, content-generation, fastapi, multi-tenant, jams"
echo "3. Enable GitHub Pages in Settings → Pages"
echo "4. Create first release (v1.0.0)"

