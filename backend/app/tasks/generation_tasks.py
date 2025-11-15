"""
Jukeyman Autonomous Media Station (JAMS) - Celery Generation Tasks
"""
from celery import Celery
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging
import time

from app.core.config import settings
from app.services.comfyui_service import comfyui_service
from app.services.storage_service import storage_service

logger = logging.getLogger(__name__)

# Initialize Celery
celery_app = Celery(
    'jams_tasks',
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

# Configure Celery
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,  # 1 hour max
    task_soft_time_limit=3000,  # 50 minutes soft limit
)


def get_sync_db():
    """Get synchronous database session for Celery tasks"""
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()


@celery_app.task(bind=True, name='generate_image')
def generate_image_task(
    self,
    generation_id: str,
    tenant_id: str,
    user_id: str,
    prompt: str,
    negative_prompt: str,
    model: str,
    width: int,
    height: int,
    steps: int,
    cfg: float,
    sampler: str,
    scheduler: str,
    seed: int,
    safety_checker: bool
):
    """
    Background task for image generation
    """
    from app.models.generation import Generation
    
    db = get_sync_db()
    start_time = time.time()
    
    try:
        # Update status to processing
        generation = db.query(Generation).filter(Generation.id == generation_id).first()
        if not generation:
            logger.error(f"Generation not found: {generation_id}")
            return
        
        generation.status = 'processing'
        db.commit()
        
        logger.info(f"Starting image generation: {generation_id}")
        
        # Generate image with ComfyUI
        result = comfyui_service.generate_image(
            prompt=prompt,
            negative_prompt=negative_prompt,
            model=model,
            width=width,
            height=height,
            steps=steps,
            cfg=cfg,
            sampler=sampler,
            scheduler=scheduler,
            seed=seed,
            safety_checker=safety_checker
        )
        
        # Upload to R2
        output_urls = []
        for image_path in result['images']:
            url = storage_service.upload_file(
                file_path=image_path,
                tenant_id=tenant_id,
                content_type='image/png'
            )
            output_urls.append(url)
        
        # Update generation record
        generation.status = 'completed'
        generation.output_url = output_urls[0] if output_urls else None
        generation.output_urls = output_urls
        generation.processing_time_seconds = int(time.time() - start_time)
        generation.metadata = result.get('metadata', {})
        db.commit()
        
        logger.info(f"Image generation completed: {generation_id}")
        
        return {
            'generation_id': generation_id,
            'status': 'completed',
            'output_urls': output_urls
        }
    
    except Exception as e:
        logger.error(f"Image generation failed: {e}", exc_info=True)
        
        # Update status to failed
        if generation:
            generation.status = 'failed'
            generation.error_message = str(e)
            generation.processing_time_seconds = int(time.time() - start_time)
            db.commit()
        
        raise
    
    finally:
        db.close()


@celery_app.task(bind=True, name='generate_video')
def generate_video_task(self, generation_id: str, tenant_id: str, **kwargs):
    """
    Background task for video generation
    """
    logger.info(f"Video generation task: {generation_id}")
    # TODO: Implement video generation with Open-Sora
    return {"status": "pending"}


@celery_app.task(bind=True, name='generate_voice')
def generate_voice_task(self, generation_id: str, tenant_id: str, **kwargs):
    """
    Background task for voice generation
    """
    logger.info(f"Voice generation task: {generation_id}")
    # TODO: Implement voice generation with Coqui TTS
    return {"status": "pending"}


@celery_app.task(bind=True, name='upscale_image')
def upscale_image_task(self, image_url: str, tenant_id: str):
    """
    Background task for image upscaling with Real-ESRGAN
    """
    logger.info(f"Upscaling image: {image_url}")
    # TODO: Implement upscaling with Real-ESRGAN
    return {"status": "pending"}

