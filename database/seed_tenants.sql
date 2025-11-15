-- Jukeyman Autonomous Media Station (JAMS) - Seed Data for Tenants
-- Creates FetishVerse (uncensored) and General AI SaaS (moderated) tenants

-- Insert FetishVerse Tenant (Adult Content Marketplace - Uncensored)
INSERT INTO tenants (id, name, domain, content_policy, settings) VALUES
(
    '11111111-1111-1111-1111-111111111111', -- Fixed UUID for easy reference
    'FetishVerse',
    'fetishverse.com',
    'uncensored',
    '{
        "allow_nsfw": true,
        "content_filters_enabled": false,
        "safety_checker_enabled": false,
        "max_generation_size": "unlimited",
        "supported_content_types": ["adult", "fetish", "nsfw", "explicit"],
        "age_verification_required": true,
        "default_credits_per_generation": {
            "image": 1,
            "video": 5,
            "voice": 2,
            "text": 1
        }
    }'::jsonb
) ON CONFLICT (id) DO UPDATE SET
    name = EXCLUDED.name,
    domain = EXCLUDED.domain,
    content_policy = EXCLUDED.content_policy,
    settings = EXCLUDED.settings;

-- Insert General AI SaaS Tenant (Moderated for Business Use)
INSERT INTO tenants (id, name, domain, content_policy, settings) VALUES
(
    '22222222-2222-2222-2222-222222222222', -- Fixed UUID for easy reference
    'AI Content Studio',
    'aicontent.studio',
    'moderated',
    '{
        "allow_nsfw": false,
        "content_filters_enabled": true,
        "safety_checker_enabled": true,
        "max_generation_size": "4k",
        "supported_content_types": ["business", "marketing", "creative", "professional"],
        "age_verification_required": false,
        "default_credits_per_generation": {
            "image": 1,
            "video": 10,
            "voice": 2,
            "text": 1
        }
    }'::jsonb
) ON CONFLICT (id) DO UPDATE SET
    name = EXCLUDED.name,
    domain = EXCLUDED.domain,
    content_policy = EXCLUDED.content_policy,
    settings = EXCLUDED.settings;

-- Create admin users for each tenant
-- Password for both: Admin123! (hashed with bcrypt)
-- Hash: $2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5ygPMl1c0K7nq

-- FetishVerse Admin
INSERT INTO users (id, tenant_id, email, hashed_password, role, credits, email_verified) VALUES
(
    'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
    '11111111-1111-1111-1111-111111111111',
    'admin@fetishverse.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5ygPMl1c0K7nq',
    'admin',
    10000,
    true
) ON CONFLICT (tenant_id, email) DO UPDATE SET
    hashed_password = EXCLUDED.hashed_password,
    role = EXCLUDED.role;

-- AI Content Studio Admin
INSERT INTO users (id, tenant_id, email, hashed_password, role, credits, email_verified) VALUES
(
    'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb',
    '22222222-2222-2222-2222-222222222222',
    'admin@aicontent.studio',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5ygPMl1c0K7nq',
    'admin',
    10000,
    true
) ON CONFLICT (tenant_id, email) DO UPDATE SET
    hashed_password = EXCLUDED.hashed_password,
    role = EXCLUDED.role;

-- Create demo creator users
INSERT INTO users (tenant_id, email, hashed_password, role, credits, email_verified) VALUES
(
    '11111111-1111-1111-1111-111111111111',
    'creator@fetishverse.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5ygPMl1c0K7nq',
    'creator',
    5000,
    true
) ON CONFLICT (tenant_id, email) DO NOTHING;

INSERT INTO users (tenant_id, email, hashed_password, role, credits, email_verified) VALUES
(
    '22222222-2222-2222-2222-222222222222',
    'creator@aicontent.studio',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5ygPMl1c0K7nq',
    'creator',
    5000,
    true
) ON CONFLICT (tenant_id, email) DO NOTHING;

-- Create subscription plans
INSERT INTO subscriptions (tenant_id, user_id, plan, status, credits_per_month) VALUES
(
    '11111111-1111-1111-1111-111111111111',
    'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
    'enterprise',
    'active',
    100000
) ON CONFLICT DO NOTHING;

INSERT INTO subscriptions (tenant_id, user_id, plan, status, credits_per_month) VALUES
(
    '22222222-2222-2222-2222-222222222222',
    'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb',
    'enterprise',
    'active',
    100000
) ON CONFLICT DO NOTHING;

-- Create audit log entries
INSERT INTO audit_logs (tenant_id, user_id, action, resource_type, details) VALUES
(
    '11111111-1111-1111-1111-111111111111',
    'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
    'TENANT_CREATED',
    'tenant',
    '{"message": "FetishVerse tenant initialized"}'::jsonb
);

INSERT INTO audit_logs (tenant_id, user_id, action, resource_type, details) VALUES
(
    '22222222-2222-2222-2222-222222222222',
    'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb',
    'TENANT_CREATED',
    'tenant',
    '{"message": "AI Content Studio tenant initialized"}'::jsonb
);

-- Display tenant information
SELECT 
    id,
    name,
    domain,
    content_policy,
    settings->>'allow_nsfw' as allows_nsfw,
    settings->>'content_filters_enabled' as has_filters,
    created_at
FROM tenants
ORDER BY name;

-- Display admin users
SELECT 
    u.id,
    t.name as tenant_name,
    u.email,
    u.role,
    u.credits,
    u.email_verified
FROM users u
JOIN tenants t ON u.tenant_id = t.id
WHERE u.role = 'admin'
ORDER BY t.name;

