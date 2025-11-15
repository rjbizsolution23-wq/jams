"""
Jukeyman Autonomous Media Station (JAMS) - Generation API Routes
"""
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID
import logging

from app.core.database import get_db, set_tenant_context
from app.core.security import get_current_user, get_current_tenant
from app.models.user import User
from app.models.tenant import Tenant
from app.models.generation import Generation
from app.services.comfyui_service import comfyui_service
from app.services.storage_service import storage_service
from app.tasks.generation_tasks import generate_image_task

logger = logging.getLogger(__name__)

router = APIRouter()


# Request Models
class ImageGenerationRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=5000)
    negative_prompt: Optional[str] = Field(None, max_length=5000)
    model: Optional[str] = None
    width: int = Field(1024, ge=512, le=2048)
    height: int = Field(1024, ge=512, le=2048)
    steps: int = Field(30, ge=1, le=150)
    cfg: float = Field(7.0, ge=1.0, le=30.0)
    sampler: str = Field("euler_ancestral")
    scheduler: str = Field("normal")
    seed: int = Field(-1)
    batch_size: int = Field(1, ge=1, le=4)


class VideoGenerationRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=5000)
    duration: int = Field(10, ge=1, le=60)
    fps: int = Field(24, ge=15, le=60)
    resolution: str = Field("720p", pattern="^(480p|720p|1080p)$")


class VoiceGenerationRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=10000)
    voice_model: str = Field("xtts_v2")
    language: str = Field("en")
    reference_audio_url: Optional[str] = None


class TextGenerationRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=10000)
    model: str = Field("dolphin-2.6-mistral-7b")
    max_tokens: int = Field(2000, ge=1, le=4000)
    temperature: float = Field(0.7, ge=0.0, le=2.0)


# Response Models
class GenerationResponse(BaseModel):
    id: UUID
    status: str
    type: str
    prompt: str
    output_url: Optional[str]
    created_at: str


# Routes

@router.post("/image", response_model=GenerationResponse)
async def generate_image(
    request: ImageGenerationRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    current_tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Generate an image using ComfyUI
    
    - Supports uncensored generation for FetishVerse tenant
    - Uses tenant-specific model settings
    - Queues generation as background task
    """
    # Set tenant context for RLS
    await set_tenant_context(db, str(current_tenant.id), str(current_user.id))
    
    # Check tenant content policy
    tenant_settings = current_tenant.settings or {}
    safety_checker = tenant_settings.get('safety_checker_enabled', True)
    
    # Select model based on tenant config
    if not request.model:
        default_models = tenant_settings.get('default_models', {})
        request.model = default_models.get('image', 'RealVisXL_V4.0.safetensors')
    
    # Create generation record
    generation = Generation(
        tenant_id=current_tenant.id,
        user_id=current_user.id,
        type='image',
        status='queued',
        prompt=request.prompt,
        negative_prompt=request.negative_prompt,
        model=request.model,
        parameters={
            'width': request.width,
            'height': request.height,
            'steps': request.steps,
            'cfg': request.cfg,
            'sampler': request.sampler,
            'scheduler': request.scheduler,
            'seed': request.seed,
            'batch_size': request.batch_size
        },
        cost_credits=request.batch_size
    )
    
    db.add(generation)
    await db.commit()
    await db.refresh(generation)
    
    # Queue background task
    background_tasks.add_task(
        generate_image_task,
        generation_id=str(generation.id),
        tenant_id=str(current_tenant.id),
        user_id=str(current_user.id),
        prompt=request.prompt,
        negative_prompt=request.negative_prompt or "",
        model=request.model,
        width=request.width,
        height=request.height,
        steps=request.steps,
        cfg=request.cfg,
        sampler=request.sampler,
        scheduler=request.scheduler,
        seed=request.seed,
        safety_checker=safety_checker
    )
    
    logger.info(f"Queued image generation: {generation.id} for user: {current_user.id}")
    
    return GenerationResponse(
        id=generation.id,
        status=generation.status,
        type=generation.type,
        prompt=generation.prompt,
        output_url=generation.output_url,
        created_at=generation.created_at.isoformat()
    )


@router.post("/video", response_model=GenerationResponse)
async def generate_video(
    request: VideoGenerationRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    current_tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Generate a video using Open-Sora or Stable Video Diffusion
    """
    await set_tenant_context(db, str(current_tenant.id), str(current_user.id))
    
    generation = Generation(
        tenant_id=current_tenant.id,
        user_id=current_user.id,
        type='video',
        status='queued',
        prompt=request.prompt,
        model='Open-Sora',
        parameters={
            'duration': request.duration,
            'fps': request.fps,
            'resolution': request.resolution
        },
        cost_credits=request.duration  # Cost scales with duration
    )
    
    db.add(generation)
    await db.commit()
    await db.refresh(generation)
    
    # TODO: Queue video generation task
    
    logger.info(f"Queued video generation: {generation.id}")
    
    return GenerationResponse(
        id=generation.id,
        status=generation.status,
        type=generation.type,
        prompt=generation.prompt,
        output_url=generation.output_url,
        created_at=generation.created_at.isoformat()
    )


@router.post("/voice", response_model=GenerationResponse)
async def generate_voice(
    request: VoiceGenerationRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    current_tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Generate voice using Coqui TTS
    """
    await set_tenant_context(db, str(current_tenant.id), str(current_user.id))
    
    generation = Generation(
        tenant_id=current_tenant.id,
        user_id=current_user.id,
        type='voice',
        status='queued',
        prompt=request.text,
        model=request.voice_model,
        parameters={
            'language': request.language,
            'reference_audio_url': request.reference_audio_url
        },
        cost_credits=2
    )
    
    db.add(generation)
    await db.commit()
    await db.refresh(generation)
    
    # TODO: Queue voice generation task
    
    logger.info(f"Queued voice generation: {generation.id}")
    
    return GenerationResponse(
        id=generation.id,
        status=generation.status,
        type=generation.type,
        prompt=generation.prompt,
        output_url=generation.output_url,
        created_at=generation.created_at.isoformat()
    )


@router.post("/text", response_model=GenerationResponse)
async def generate_text(
    request: TextGenerationRequest,
    current_user: User = Depends(get_current_user),
    current_tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Generate text using uncensored LLM (Dolphin/MythoMax)
    """
    await set_tenant_context(db, str(current_tenant.id), str(current_user.id))
    
    generation = Generation(
        tenant_id=current_tenant.id,
        user_id=current_user.id,
        type='text',
        status='processing',
        prompt=request.prompt,
        model=request.model,
        parameters={
            'max_tokens': request.max_tokens,
            'temperature': request.temperature
        },
        cost_credits=1
    )
    
    db.add(generation)
    await db.commit()
    await db.refresh(generation)
    
    # TODO: Call LLM service directly (or queue task)
    # For now, return pending
    
    logger.info(f"Queued text generation: {generation.id}")
    
    return GenerationResponse(
        id=generation.id,
        status=generation.status,
        type=generation.type,
        prompt=generation.prompt,
        output_url=None,
        created_at=generation.created_at.isoformat()
    )


@router.get("/{generation_id}", response_model=GenerationResponse)
async def get_generation(
    generation_id: UUID,
    current_user: User = Depends(get_current_user),
    current_tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    Get generation status and result
    """
    await set_tenant_context(db, str(current_tenant.id), str(current_user.id))
    
    from sqlalchemy import select
    result = await db.execute(
        select(Generation).where(
            Generation.id == generation_id,
            Generation.tenant_id == current_tenant.id,
            Generation.user_id == current_user.id
        )
    )
    generation = result.scalar_one_or_none()
    
    if not generation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Generation not found"
        )
    
    return GenerationResponse(
        id=generation.id,
        status=generation.status,
        type=generation.type,
        prompt=generation.prompt,
        output_url=generation.output_url,
        created_at=generation.created_at.isoformat()
    )


@router.get("/", response_model=List[GenerationResponse])
async def list_generations(
    skip: int = 0,
    limit: int = 20,
    type: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    current_tenant: Tenant = Depends(get_current_tenant),
    db: AsyncSession = Depends(get_db)
):
    """
    List user's generations
    """
    await set_tenant_context(db, str(current_tenant.id), str(current_user.id))
    
    from sqlalchemy import select
    query = select(Generation).where(
        Generation.tenant_id == current_tenant.id,
        Generation.user_id == current_user.id
    )
    
    if type:
        query = query.where(Generation.type == type)
    
    query = query.order_by(Generation.created_at.desc()).offset(skip).limit(limit)
    
    result = await db.execute(query)
    generations = result.scalars().all()
    
    return [
        GenerationResponse(
            id=g.id,
            status=g.status,
            type=g.type,
            prompt=g.prompt,
            output_url=g.output_url,
            created_at=g.created_at.isoformat()
        )
        for g in generations
    ]

