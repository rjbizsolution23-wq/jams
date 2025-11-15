# 🚀 JAMS Complete Implementation Guide

## 📋 Overview

This guide covers the complete implementation of:
1. ✅ Next.js 15 FetishVerse Marketplace Frontend
2. ✅ Next.js 15 General AI SaaS Frontend
3. ✅ Supabase Authentication with Multi-Tenant RLS
4. ✅ n8n Workflow Automation
5. ✅ Twitter/Reddit API Integration

---

## 🏗️ Architecture Summary

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTENDS (Next.js 15)                │
│  • FetishVerse Marketplace (Port 3000)                  │
│  • AI SaaS Tool (Port 3001)                             │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│              SUPABASE (Auth + Database)                  │
│  • Authentication (GoTrue)                               │
│  • PostgreSQL with RLS                                   │
│  • Multi-tenant isolation                                │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│              BACKEND API (FastAPI)                       │
│  • Content generation                                    │
│  • Payment processing                                    │
│  • Social media integration                              │
└──────────────────────┬──────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
┌──────────┐    ┌──────────┐    ┌──────────┐
│   n8n    │    │ Twitter  │    │ Reddit   │
│Workflows │    │   API    │    │   API    │
└──────────┘    └──────────┘    └──────────┘
```

---

## 📦 Part 1: Supabase Setup

### Step 1.1: Create Supabase Project

1. Go to https://supabase.com
2. Create new project
3. Note your:
   - Project URL
   - Anon Key
   - Service Role Key

### Step 1.2: Run Database Migrations

```bash
# Connect to Supabase SQL Editor
# Copy and paste contents of: supabase/migrations/001_initial_schema.sql
# Execute the migration
```

Or use Supabase CLI:

```bash
supabase init
supabase db push
```

### Step 1.3: Configure Environment Variables

Create `.env.local`:

```env
# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
SUPABASE_DB_PASSWORD=your-db-password
SUPABASE_JWT_SECRET=your-jwt-secret
```

---

## 🛍️ Part 2: FetishVerse Marketplace Frontend

### Step 2.1: Install Dependencies

```bash
cd frontend/fetishverse
npm install
```

### Step 2.2: Configure Environment

Create `.env.local`:

```env
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_R2_DOMAIN=cdn.yourdomain.com
```

### Step 2.3: Run Development Server

```bash
npm run dev
```

Access at: http://localhost:3000

### Step 2.4: Key Features Implemented

- ✅ Product catalog with categories
- ✅ Shopping cart (Zustand state management)
- ✅ Checkout with Stripe
- ✅ User dashboard
- ✅ Product detail pages
- ✅ Search and filtering
- ✅ Responsive design (shadcn/ui)

---

## 🤖 Part 3: AI SaaS Frontend

### Step 3.1: Install Dependencies

```bash
cd frontend/ai-saas
npm install
```

### Step 3.2: Configure Environment

Create `.env.local`:

```env
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

### Step 3.3: Run Development Server

```bash
npm run dev
```

Access at: http://localhost:3001

### Step 3.4: Key Features Implemented

- ✅ Image generation interface
- ✅ Video generation interface
- ✅ Text generation interface
- ✅ Voice generation interface
- ✅ Real-time progress (WebSocket)
- ✅ Generation history
- ✅ API key management
- ✅ Usage analytics

---

## 🔐 Part 4: Multi-Tenant RLS Setup

### Step 4.1: Verify RLS Policies

All tables have Row-Level Security enabled. Users can only:
- See data from their own tenant
- Create data for their own tenant
- Update/delete their own data (or admin role)

### Step 4.2: Create Test Tenant

```sql
-- Insert test tenant
INSERT INTO tenants (id, name, slug, plan)
VALUES (
  '00000000-0000-0000-0000-000000000001',
  'FetishVerse',
  'fetishverse',
  'pro'
);

-- Create user and link to tenant
-- (User will be created via Supabase Auth, then linked)
```

### Step 4.3: Link User to Tenant

After user signs up via Supabase Auth:

```sql
UPDATE users
SET tenant_id = '00000000-0000-0000-0000-000000000001'
WHERE id = 'user-uuid-from-auth';
```

---

## 🔄 Part 5: n8n Workflow Setup

### Step 5.1: Start n8n

```bash
docker-compose -f docker-compose.frontend.yml up n8n
```

Access at: http://localhost:5678

### Step 5.2: Import Workflows

1. Go to n8n dashboard
2. Click "Workflows" → "Import from File"
3. Import:
   - `n8n/workflows/auto-post-twitter.json`
   - `n8n/workflows/auto-post-reddit.json`

### Step 5.3: Configure Credentials

#### Twitter Credentials:
1. Go to https://developer.twitter.com
2. Create app and get:
   - Consumer Key
   - Consumer Secret
   - Access Token
   - Access Token Secret
3. Add to n8n credentials

#### Reddit Credentials:
1. Go to https://www.reddit.com/prefs/apps
2. Create app (script type)
3. Get:
   - Client ID
   - Client Secret
4. Add username and password
5. Add to n8n credentials

### Step 5.4: Activate Workflows

1. Open each workflow
2. Click "Active" toggle
3. Workflows will listen for webhooks

---

## 🐦 Part 6: Twitter Integration

### Step 6.1: Setup Twitter API

1. Apply for Twitter Developer account
2. Create app at https://developer.twitter.com
3. Get OAuth 1.0a credentials

### Step 6.2: Configure Environment

Add to `.env`:

```env
TWITTER_CONSUMER_KEY=your-consumer-key
TWITTER_CONSUMER_SECRET=your-consumer-secret
TWITTER_ACCESS_TOKEN=your-access-token
TWITTER_ACCESS_TOKEN_SECRET=your-access-token-secret
TWITTER_BEARER_TOKEN=your-bearer-token
```

### Step 6.3: Test Integration

```python
from integrations.twitter_client import get_twitter_client

client = get_twitter_client()
result = client.post_tweet("Test tweet from JAMS!")
print(result)
```

---

## 🔴 Part 7: Reddit Integration

### Step 7.1: Setup Reddit API

1. Go to https://www.reddit.com/prefs/apps
2. Click "create another app..."
3. Choose "script" type
4. Get Client ID and Secret

### Step 7.2: Configure Environment

Add to `.env`:

```env
REDDIT_CLIENT_ID=your-client-id
REDDIT_CLIENT_SECRET=your-client-secret
REDDIT_USERNAME=your-reddit-username
REDDIT_PASSWORD=your-reddit-password
REDDIT_USER_AGENT=JAMS/1.0 by rjbizsolution23-wq
```

### Step 7.3: Test Integration

```python
from integrations.reddit_client import get_reddit_client

client = get_reddit_client()
result = client.post_to_subreddit(
    subreddit_name="NSFW",
    title="Test Post",
    text="This is a test post from JAMS"
)
print(result)
```

---

## 🐳 Part 8: Docker Compose Setup

### Step 8.1: Create Environment File

Create `.env` in project root:

```env
# Supabase
SUPABASE_DB_PASSWORD=your-super-secret-password
SUPABASE_JWT_SECRET=your-super-secret-jwt-token-with-at-least-32-characters-long
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# Stripe
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...

# Cloudflare R2
R2_ACCESS_KEY_ID=your-r2-access-key
R2_SECRET_ACCESS_KEY=your-r2-secret-key
R2_BUCKET_NAME=jams-content
R2_ENDPOINT_URL=https://your-account-id.r2.cloudflarestorage.com
R2_DOMAIN=cdn.yourdomain.com

# Twitter
TWITTER_CONSUMER_KEY=...
TWITTER_CONSUMER_SECRET=...
TWITTER_ACCESS_TOKEN=...
TWITTER_ACCESS_TOKEN_SECRET=...

# Reddit
REDDIT_CLIENT_ID=...
REDDIT_CLIENT_SECRET=...
REDDIT_USERNAME=...
REDDIT_PASSWORD=...

# n8n
N8N_USER=admin
N8N_PASSWORD=changeme
N8N_HOST=localhost
```

### Step 8.2: Start All Services

```bash
docker-compose -f docker-compose.frontend.yml up -d
```

### Step 8.3: Verify Services

- FetishVerse: http://localhost:3000
- AI SaaS: http://localhost:3001
- Backend API: http://localhost:8000
- n8n: http://localhost:5678
- Supabase Auth: http://localhost:9999

---

## 📝 Part 9: Usage Examples

### Post Product to Twitter

```bash
curl -X POST http://localhost:8000/api/v1/social/twitter/post \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": "product-uuid",
    "include_image": true
  }'
```

### Post Product to Reddit

```bash
curl -X POST http://localhost:8000/api/v1/social/reddit/post \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": "product-uuid",
    "subreddit": "NSFW",
    "include_image": true
  }'
```

### Auto-Post to Multiple Platforms

```bash
curl -X POST http://localhost:8000/api/v1/social/auto-post \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": "product-uuid",
    "platforms": ["twitter", "reddit"]
  }'
```

---

## ✅ Verification Checklist

- [ ] Supabase project created and migrations run
- [ ] FetishVerse frontend running on port 3000
- [ ] AI SaaS frontend running on port 3001
- [ ] Backend API running on port 8000
- [ ] n8n running on port 5678
- [ ] Twitter credentials configured
- [ ] Reddit credentials configured
- [ ] n8n workflows imported and activated
- [ ] Test user created and linked to tenant
- [ ] RLS policies working (users can only see their tenant's data)
- [ ] Social media posting working via API

---

## 🚀 Production Deployment

### Frontend Deployment (Cloudflare Pages)

```bash
# FetishVerse
cd frontend/fetishverse
npm run build
npx wrangler pages deploy .next --project-name=fetishverse

# AI SaaS
cd frontend/ai-saas
npm run build
npx wrangler pages deploy .next --project-name=ai-saas
```

### Backend Deployment

Deploy to your GPU server (RunPod, etc.) with Docker Compose.

### Environment Variables

Set all environment variables in your deployment platform.

---

## 📞 Support

For issues or questions:
- **Email:** rick@rjbusinesssolutions.org
- **Phone:** (505) 502-5054
- **Website:** https://rjbusinesssolutions.org/

---

**All components are fully implemented and ready for production! 🎉**

