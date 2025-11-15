# 🏗️ JAMS Frontend Architecture - Complete Implementation Plan

## 📋 Overview

JAMS (Jukeyman Autonomous Media Station) requires **two separate Next.js 15 frontends**:

1. **FetishVerse Marketplace** - Adult content marketplace for NSFW content packs
2. **General AI SaaS** - Commercial AI content generation tool for any industry

Both frontends share:
- Supabase authentication
- Multi-tenant RLS (Row-Level Security)
- Same backend API
- Unified design system

---

## 🎯 Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    CLOUDFLARE PAGES/CDN                     │
│  • Global CDN distribution                                   │
│  • SSL/TLS termination                                      │
│  • DDoS protection                                           │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│  FetishVerse │ │  AI SaaS    │ │   Admin      │
│  Marketplace │ │  Frontend   │ │   Dashboard  │
│  (Next.js)   │ │  (Next.js)  │ │  (Next.js)   │
│              │ │              │ │              │
│  Port: 3000  │ │  Port: 3001  │ │  Port: 3002  │
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       │                │                │
       └────────────────┼────────────────┘
                        │
                        ▼
        ┌───────────────────────────────┐
        │     SUPABASE (Auth + RLS)      │
        │  • Authentication              │
        │  • Row-Level Security          │
        │  • Multi-tenant isolation      │
        │  • Real-time subscriptions     │
        └───────────────┬─────────────────┘
                        │
                        ▼
        ┌───────────────────────────────┐
        │     FASTAPI BACKEND            │
        │  • Content generation API       │
        │  • Payment processing          │
        │  • Job queue management        │
        └───────────────┬─────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
┌──────────┐    ┌──────────┐    ┌──────────┐
│  n8n     │    │ Twitter  │    │ Reddit   │
│Workflows │    │   API    │    │   API    │
└──────────┘    └──────────┘    └──────────┘
```

---

## 🛍️ Frontend 1: FetishVerse Marketplace

### Purpose
Adult content marketplace for selling NSFW content packs (images, videos, voice packs)

### Key Features
- Product catalog with categories (fetish types)
- Shopping cart and checkout
- User dashboard (purchases, favorites)
- Content preview (blurred/watermarked)
- Payment integration (Stripe/LemonSqueezy)
- Content download after purchase
- User reviews and ratings
- Search and filtering

### Tech Stack
- **Framework:** Next.js 15 (App Router)
- **UI:** shadcn/ui + Tailwind CSS
- **State:** Zustand
- **Forms:** React Hook Form + Zod
- **Auth:** Supabase Auth
- **Payments:** Stripe Elements
- **Storage:** Cloudflare R2 (content delivery)

### Pages Structure
```
/fetishverse/
├── / (homepage - featured products)
├── /products (catalog)
├── /products/[id] (product detail)
├── /cart (shopping cart)
├── /checkout (payment)
├── /dashboard (user dashboard)
│   ├── /purchases
│   ├── /favorites
│   └── /settings
├── /auth (login/signup)
└── /api (API routes)
```

---

## 🤖 Frontend 2: General AI SaaS

### Purpose
Commercial AI content generation tool for businesses (images, videos, text, voice)

### Key Features
- Content generation interface
- Real-time generation progress
- Generation history
- API key management
- Usage analytics and billing
- Team/organization management
- Template library
- Batch processing

### Tech Stack
- **Framework:** Next.js 15 (App Router)
- **UI:** shadcn/ui + Tailwind CSS
- **State:** Zustand
- **Forms:** React Hook Form + Zod
- **Auth:** Supabase Auth
- **WebSockets:** Real-time updates
- **Charts:** Recharts

### Pages Structure
```
/ai-saas/
├── / (dashboard)
├── /generate
│   ├── /image
│   ├── /video
│   ├── /text
│   └── /voice
├── /history (generation history)
├── /api-keys (API management)
├── /analytics (usage stats)
├── /billing (subscription)
├── /team (organization)
├── /templates
└── /settings
```

---

## 🔐 Supabase Multi-Tenant Setup

### Database Schema
```sql
-- Tenants table
CREATE TABLE tenants (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  slug TEXT UNIQUE NOT NULL,
  plan TEXT DEFAULT 'free',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Users table (extends Supabase auth.users)
CREATE TABLE public.users (
  id UUID PRIMARY KEY REFERENCES auth.users(id),
  tenant_id UUID REFERENCES tenants(id),
  email TEXT,
  role TEXT DEFAULT 'user',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Products table (FetishVerse)
CREATE TABLE products (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID REFERENCES tenants(id),
  name TEXT NOT NULL,
  description TEXT,
  price DECIMAL(10,2),
  category TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Generations table (AI SaaS)
CREATE TABLE generations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID REFERENCES tenants(id),
  user_id UUID REFERENCES users(id),
  type TEXT, -- 'image', 'video', 'text', 'voice'
  prompt TEXT,
  status TEXT, -- 'pending', 'processing', 'completed', 'failed'
  result_url TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Row-Level Security Policies
```sql
-- Users can only see their tenant's data
CREATE POLICY "Users see own tenant data"
  ON products FOR SELECT
  USING (
    tenant_id IN (
      SELECT tenant_id FROM users WHERE id = auth.uid()
    )
  );

-- Users can only create for their tenant
CREATE POLICY "Users create for own tenant"
  ON products FOR INSERT
  WITH CHECK (
    tenant_id IN (
      SELECT tenant_id FROM users WHERE id = auth.uid()
    )
  );
```

---

## 🔄 n8n Workflows

### Workflow 1: Auto-Post to Twitter
- **Trigger:** New product published (webhook)
- **Actions:**
  1. Generate tweet text with product details
  2. Upload product image to Twitter
  3. Post tweet with hashtags
  4. Log to database

### Workflow 2: Auto-Post to Reddit
- **Trigger:** New product published (webhook)
- **Actions:**
  1. Select appropriate subreddit
  2. Format post (title + description)
  3. Upload image/video
  4. Post to subreddit
  5. Monitor comments

### Workflow 3: Content Generation Pipeline
- **Trigger:** User submits generation request
- **Actions:**
  1. Queue job in Celery
  2. Monitor progress
  3. Upload result to R2
  4. Notify user via email/WebSocket
  5. Update database

---

## 📦 Implementation Order

1. ✅ **Supabase Setup** (Database + Auth + RLS)
2. ✅ **Shared Components** (Design system, auth hooks)
3. ✅ **FetishVerse Frontend** (Marketplace)
4. ✅ **AI SaaS Frontend** (Generation tool)
5. ✅ **n8n Workflows** (Automation)
6. ✅ **API Integrations** (Twitter/Reddit)
7. ✅ **Docker Compose** (Full stack)
8. ✅ **Documentation** (Deployment guides)

---

## 🚀 Next Steps

See individual implementation files:
- `frontend/fetishverse/` - Marketplace frontend
- `frontend/ai-saas/` - AI SaaS frontend
- `supabase/` - Database setup and migrations
- `n8n/` - Workflow definitions
- `integrations/` - Twitter/Reddit API clients

