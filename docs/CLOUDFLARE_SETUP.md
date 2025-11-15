# Cloudflare Setup Guide

Complete guide to setting up Cloudflare Tunnel and R2 storage for Jukeyman Autonomous Media Station (JAMS).

## Prerequisites

- Cloudflare account
- Domain registered with Cloudflare (or transferred to Cloudflare)
- `cloudflared` CLI installed (done by install_infrastructure.sh)

## 1. Cloudflare R2 Storage Setup

### Create R2 Bucket

1. Log in to Cloudflare Dashboard
2. Navigate to **R2 Object Storage**
3. Click **Create bucket**
4. Name: `ai-empire-content`
5. Location: **Automatic** (recommended)
6. Click **Create bucket**

### Generate R2 API Keys

1. In R2 dashboard, click **Manage R2 API Tokens**
2. Click **Create API token**
3. Token name: `AI Empire Backend`
4. Permissions: **Admin Read & Write**
5. TTL: **Forever** (or custom)
6. Click **Create API Token**

7. Copy the credentials:
   ```
   Access Key ID: xxxxxxxxxxxxxxxxxxxxx
   Secret Access Key: yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy
   ```

### Get R2 Endpoint URL

Your R2 endpoint URL format:
```
https://<ACCOUNT_ID>.r2.cloudflarestorage.com
```

Get your Account ID from Cloudflare Dashboard → R2 → Settings

### Setup R2 Public URL (Optional CDN)

1. Go to your bucket settings
2. Click **Settings** → **Public access**
3. Option A: **Allow access** (direct R2 URLs)
4. Option B: **Custom domain** (recommended)
   - Click **Connect domain**
   - Enter: `cdn.yourdomain.com`
   - Add CNAME record to your DNS
   - Wait for SSL certificate

Your public URL will be:
- Direct: `https://pub-xxxxxxxxx.r2.dev`
- Custom: `https://cdn.yourdomain.com`

### Update .env

```bash
R2_ACCESS_KEY_ID=your-access-key
R2_SECRET_ACCESS_KEY=your-secret-key
R2_BUCKET_NAME=ai-empire-content
R2_ENDPOINT_URL=https://your-account-id.r2.cloudflarestorage.com
R2_PUBLIC_URL=https://cdn.yourdomain.com  # or pub-xxxxx.r2.dev
CLOUDFLARE_ACCOUNT_ID=your-account-id
```

## 2. Cloudflare Tunnel Setup

### Login to Cloudflare

```bash
cloudflared login
```

This opens a browser. Select your domain and authorize.

### Create Tunnel

```bash
cloudflared tunnel create ai-empire
```

Output:
```
Created tunnel ai-empire with id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

### Copy Tunnel Credentials

Credentials are saved to:
```
~/.cloudflared/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx.json
```

### Create Tunnel Configuration

Create `~/.cloudflared/config.yml`:

```yaml
tunnel: ai-empire
credentials-file: /root/.cloudflared/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx.json

ingress:
  # Backend API
  - hostname: api.yourdomain.com
    service: http://localhost:8000
  
  # ComfyUI Interface
  - hostname: comfyui.yourdomain.com
    service: http://localhost:8188
  
  # FetishVerse Frontend
  - hostname: fetishverse.com
    service: http://localhost:3000
  
  # AI Content Studio Frontend
  - hostname: aicontent.studio
    service: http://localhost:3001
  
  # Admin Dashboard
  - hostname: admin.yourdomain.com
    service: http://localhost:3002
  
  # n8n Automation
  - hostname: n8n.yourdomain.com
    service: http://localhost:5678
  
  # Grafana Monitoring
  - hostname: grafana.yourdomain.com
    service: http://localhost:3002
  
  # Catch-all rule (required)
  - service: http_status:404
```

### Configure DNS Routes

```bash
cloudflared tunnel route dns ai-empire api.yourdomain.com
cloudflared tunnel route dns ai-empire comfyui.yourdomain.com
cloudflared tunnel route dns ai-empire fetishverse.com
cloudflared tunnel route dns ai-empire aicontent.studio
cloudflared tunnel route dns ai-empire admin.yourdomain.com
cloudflared tunnel route dns ai-empire n8n.yourdomain.com
cloudflared tunnel route dns ai-empire grafana.yourdomain.com
```

### Test Tunnel

```bash
cloudflared tunnel run ai-empire
```

Visit https://api.yourdomain.com/health to test.

### Install as System Service

```bash
sudo cloudflared service install
sudo systemctl enable cloudflared
sudo systemctl start cloudflared
```

Check status:
```bash
sudo systemctl status cloudflared
```

View logs:
```bash
sudo journalctl -u cloudflared -f
```

## 3. DNS Configuration

### Update Tenant Domains in Database

Edit `database/seed_tenants.sql`:

```sql
-- Update FetishVerse domain
UPDATE tenants 
SET domain = 'fetishverse.com'
WHERE id = '11111111-1111-1111-1111-111111111111';

-- Update AI Content Studio domain
UPDATE tenants 
SET domain = 'aicontent.studio'
WHERE id = '22222222-2222-2222-2222-222222222222';
```

Run migration:
```bash
docker-compose exec postgres psql -U postgres -d jams -f /docker-entrypoint-initdb.d/02-seed.sql
```

### Update .env

```bash
# Add domains to CORS origins
CORS_ORIGINS=["https://fetishverse.com", "https://aicontent.studio", "https://api.yourdomain.com"]
```

## 4. SSL Certificates

Cloudflare automatically provides SSL certificates for all tunneled domains.

Verify SSL:
```bash
curl -I https://api.yourdomain.com
```

Should show:
```
HTTP/2 200
...
```

## 5. Firewall Rules (Optional)

### Create WAF Rules

1. Cloudflare Dashboard → Security → WAF
2. Create Custom Rules:

**Block known bad bots:**
```
(cf.bot_management.score lt 30) and not (cf.client.bot)
```

**Rate limit API:**
```
(http.request.uri.path contains "/api/v1/generate") 
and (rate(1m) > 100)
```

**Protect admin:**
```
(http.host eq "admin.yourdomain.com") 
and (ip.geoip.country ne "US")
```

## 6. Testing

### Test R2 Upload

```bash
# From backend
python -c "
from app.services.storage_service import storage_service
import tempfile

# Create test file
with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
    f.write('Hello from JAMS')
    test_file = f.name

# Upload
url = storage_service.upload_file(
    test_file, 
    '11111111-1111-1111-1111-111111111111',
    'test.txt'
)
print(f'Uploaded to: {url}')
"
```

### Test Tunnel

```bash
# Test each endpoint
curl https://api.yourdomain.com/health
curl https://fetishverse.com
curl https://aicontent.studio
```

### Test Generation Pipeline

```bash
# Login
curl -X POST https://api.yourdomain.com/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@fetishverse.com",
    "password": "Admin123!",
    "tenant_domain": "fetishverse.com"
  }'

# Generate image (use token from above)
curl -X POST https://api.yourdomain.com/api/v1/generate/image \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "X-Tenant-Domain: fetishverse.com" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "beautiful sunset over mountains",
    "width": 1024,
    "height": 1024
  }'
```

## 7. Monitoring

### Cloudflare Analytics

- Dashboard → Analytics → Traffic
- Monitor: Requests, Bandwidth, Threats
- Set up alerts for anomalies

### Tunnel Metrics

```bash
# Check tunnel health
cloudflared tunnel info ai-empire

# View connections
cloudflared tunnel list
```

## 8. Troubleshooting

### Tunnel Not Connecting

```bash
# Check tunnel status
sudo systemctl status cloudflared

# Restart tunnel
sudo systemctl restart cloudflared

# View detailed logs
sudo journalctl -u cloudflared -n 100 --no-pager
```

### R2 Upload Failures

```bash
# Test R2 connection
aws s3 ls --endpoint-url $R2_ENDPOINT_URL s3://ai-empire-content

# Verify credentials
echo $R2_ACCESS_KEY_ID
echo $R2_SECRET_ACCESS_KEY
```

### DNS Not Resolving

```bash
# Check DNS propagation
dig api.yourdomain.com
nslookup api.yourdomain.com

# Verify Cloudflare tunnel routes
cloudflared tunnel route dns ai-empire api.yourdomain.com
```

### 502 Bad Gateway

- Check if backend service is running: `curl http://localhost:8000/health`
- Verify tunnel config: `cat ~/.cloudflared/config.yml`
- Check ingress rules match running services

## 9. Production Checklist

- [ ] R2 bucket created with appropriate permissions
- [ ] R2 API keys generated and added to .env
- [ ] Custom domain connected to R2 (CDN)
- [ ] Cloudflare Tunnel created and configured
- [ ] All DNS routes configured
- [ ] Tunnel running as system service
- [ ] SSL certificates auto-provisioned
- [ ] WAF rules configured
- [ ] Rate limiting enabled
- [ ] All endpoints accessible via HTTPS
- [ ] Test upload to R2 successful
- [ ] Test generation pipeline end-to-end

## 10. Cost Optimization

### R2 Pricing

- Storage: $0.015/GB/month
- Class A (PUT): $4.50/million requests
- Class B (GET): $0.36/million requests
- **No egress fees!**

### Tunnel Pricing

- **Free** for up to 50 users
- Standard plan: $5/month for more users

### Estimated Monthly Costs

For 1TB storage + 1M requests:
- Storage: $15
- Requests: ~$5
- Tunnel: Free
- **Total: ~$20/month**

## Support

For issues:
- Cloudflare Community: https://community.cloudflare.com/
- R2 Docs: https://developers.cloudflare.com/r2/
- Tunnel Docs: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/

