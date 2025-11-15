"""
Jukeyman Autonomous Media Station (JAMS) - Configuration
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import validator


class Settings(BaseSettings):
    # App Info
    APP_NAME: str = "Jukeyman Autonomous Media Station"
    APP_SHORT_NAME: str = "JAMS"
    APP_VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = False
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database
    DATABASE_URL: str
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 40
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_CACHE_TTL: int = 3600  # 1 hour
    
    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/1"
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS
    CORS_ORIGINS: list = ["*"]
    
    # Cloudflare R2
    R2_ACCESS_KEY_ID: str
    R2_SECRET_ACCESS_KEY: str
    R2_BUCKET_NAME: str
    R2_ENDPOINT_URL: str
    R2_PUBLIC_URL: str
    CLOUDFLARE_ACCOUNT_ID: str
    
    # AI Services URLs
    COMFYUI_URL: str = "http://localhost:8188"
    LLAMA_CPP_URL: str = "http://localhost:8080"
    TTS_URL: str = "http://localhost:5002"
    
    # API Keys
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    OPENROUTER_API_KEY: Optional[str] = None
    ELEVENLABS_API_KEY: Optional[str] = None
    
    # Stripe
    STRIPE_SECRET_KEY: str
    STRIPE_WEBHOOK_SECRET: str
    STRIPE_PUBLISHABLE_KEY: str
    
    # Social Media
    TWITTER_API_KEY: Optional[str] = None
    TWITTER_API_SECRET: Optional[str] = None
    TWITTER_ACCESS_TOKEN: Optional[str] = None
    TWITTER_ACCESS_TOKEN_SECRET: Optional[str] = None
    TWITTER_BEARER_TOKEN: Optional[str] = None
    
    REDDIT_CLIENT_ID: Optional[str] = None
    REDDIT_CLIENT_SECRET: Optional[str] = None
    REDDIT_USER_AGENT: Optional[str] = None
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_HOUR: int = 1000
    
    # Generation Defaults
    DEFAULT_IMAGE_WIDTH: int = 1024
    DEFAULT_IMAGE_HEIGHT: int = 1024
    DEFAULT_VIDEO_DURATION: int = 10
    MAX_IMAGE_WIDTH: int = 2048
    MAX_IMAGE_HEIGHT: int = 2048
    MAX_VIDEO_DURATION: int = 60
    
    # Tenant IDs (from seed data)
    FETISHVERSE_TENANT_ID: str = "11111111-1111-1111-1111-111111111111"
    SAAS_TENANT_ID: str = "22222222-2222-2222-2222-222222222222"
    
    # Monitoring
    SENTRY_DSN: Optional[str] = None
    PROMETHEUS_PORT: int = 9090
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        
    @validator("DATABASE_URL", pre=True)
    def validate_database_url(cls, v):
        if not v:
            raise ValueError("DATABASE_URL must be set")
        return v
    
    @validator("SECRET_KEY", pre=True)
    def validate_secret_key(cls, v):
        if not v or len(v) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters")
        return v


# Global settings instance
settings = Settings()


# Tenant Configuration
TENANT_CONFIG = {
    settings.FETISHVERSE_TENANT_ID: {
        "name": "FetishVerse",
        "domain": "fetishverse.com",
        "content_policy": "uncensored",
        "allow_nsfw": True,
        "safety_checker_enabled": False,
        "default_models": {
            "image": "RealVisXL_V4.0.safetensors",
            "video": "Open-Sora",
            "voice": "xtts_v2",
            "llm": "dolphin-2.6-mistral-7b"
        }
    },
    settings.SAAS_TENANT_ID: {
        "name": "AI Content Studio",
        "domain": "aicontent.studio",
        "content_policy": "moderated",
        "allow_nsfw": False,
        "safety_checker_enabled": True,
        "default_models": {
            "image": "JuggernautXL_v9.safetensors",
            "video": "Stable-Video-Diffusion",
            "voice": "xtts_v2",
            "llm": "qwen3-coder"
        }
    }
}


def get_tenant_config(tenant_id: str) -> dict:
    """Get configuration for a specific tenant"""
    return TENANT_CONFIG.get(tenant_id, TENANT_CONFIG[settings.SAAS_TENANT_ID])

