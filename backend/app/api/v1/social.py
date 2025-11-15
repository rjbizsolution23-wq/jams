"""
JAMS - Social Media Integration API Endpoints
Handles Twitter and Reddit posting via n8n webhooks
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
import httpx
import os
import logging

from app.core.security import get_current_user
from app.core.database import get_db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/social", tags=["social"])

N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "http://localhost:5678/webhook")


class PostToTwitterRequest(BaseModel):
    product_id: str
    tweet_text: Optional[str] = None
    include_image: bool = True


class PostToRedditRequest(BaseModel):
    product_id: str
    subreddit: Optional[str] = None
    title: Optional[str] = None
    include_image: bool = True


@router.post("/twitter/post")
async def post_to_twitter(
    request: PostToTwitterRequest,
    current_user: dict = Depends(get_current_user),
    db=Depends(get_db)
):
    """
    Trigger Twitter post via n8n webhook
    Requires admin or owner role
    """
    # Check user role
    if current_user.get("role") not in ["admin", "owner"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    # Fetch product from database
    async with db.acquire() as conn:
        product = await conn.fetchrow(
            """
            SELECT id, name, description, price, slug, preview_image_url, category
            FROM products
            WHERE id = $1 AND tenant_id = $2
            """,
            request.product_id,
            current_user["tenant_id"]
        )
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Prepare webhook payload
    webhook_payload = {
        "product": dict(product),
        "tweet_text": request.tweet_text,
        "include_image": request.include_image
    }
    
    # Trigger n8n webhook
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{N8N_WEBHOOK_URL}/product-published",
                json=webhook_payload,
                timeout=30.0
            )
            response.raise_for_status()
            
            result = response.json()
            
            # Update product with Twitter post ID
            if result.get("success") and result.get("tweet_id"):
                async with db.acquire() as conn:
                    await conn.execute(
                        """
                        UPDATE products
                        SET metadata = jsonb_set(
                            COALESCE(metadata, '{}'::jsonb),
                            '{twitter_post_id}',
                            to_jsonb($1::text)
                        )
                        WHERE id = $2
                        """,
                        result["tweet_id"],
                        request.product_id
                    )
            
            return {
                "success": True,
                "tweet_id": result.get("tweet_id"),
                "tweet_url": result.get("url")
            }
    except httpx.HTTPError as e:
        logger.error(f"Failed to trigger Twitter webhook: {e}")
        raise HTTPException(status_code=500, detail="Failed to post to Twitter")


@router.post("/reddit/post")
async def post_to_reddit(
    request: PostToRedditRequest,
    current_user: dict = Depends(get_current_user),
    db=Depends(get_db)
):
    """
    Trigger Reddit post via n8n webhook
    Requires admin or owner role
    """
    # Check user role
    if current_user.get("role") not in ["admin", "owner"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    # Fetch product from database
    async with db.acquire() as conn:
        product = await conn.fetchrow(
            """
            SELECT id, name, description, price, slug, preview_image_url, category
            FROM products
            WHERE id = $1 AND tenant_id = $2
            """,
            request.product_id,
            current_user["tenant_id"]
        )
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Prepare webhook payload
    webhook_payload = {
        "product": dict(product),
        "subreddit": request.subreddit,
        "title": request.title,
        "include_image": request.include_image
    }
    
    # Trigger n8n webhook
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{N8N_WEBHOOK_URL}/product-published-reddit",
                json=webhook_payload,
                timeout=30.0
            )
            response.raise_for_status()
            
            result = response.json()
            
            # Update product with Reddit post ID
            if result.get("success") and result.get("reddit_post_id"):
                async with db.acquire() as conn:
                    await conn.execute(
                        """
                        UPDATE products
                        SET metadata = jsonb_set(
                            COALESCE(metadata, '{}'::jsonb),
                            '{reddit_post_id}',
                            to_jsonb($1::text)
                        )
                        WHERE id = $2
                        """,
                        result["reddit_post_id"],
                        request.product_id
                    )
            
            return {
                "success": True,
                "reddit_post_id": result.get("reddit_post_id"),
                "reddit_url": result.get("url")
            }
    except httpx.HTTPError as e:
        logger.error(f"Failed to trigger Reddit webhook: {e}")
        raise HTTPException(status_code=500, detail="Failed to post to Reddit")


@router.post("/auto-post")
async def auto_post_product(
    product_id: str,
    platforms: list[str] = ["twitter", "reddit"],
    current_user: dict = Depends(get_current_user),
    db=Depends(get_db)
):
    """
    Automatically post product to multiple platforms
    """
    results = {}
    
    if "twitter" in platforms:
        try:
            twitter_result = await post_to_twitter(
                PostToTwitterRequest(product_id=product_id),
                current_user=current_user,
                db=db
            )
            results["twitter"] = twitter_result
        except Exception as e:
            results["twitter"] = {"success": False, "error": str(e)}
    
    if "reddit" in platforms:
        try:
            reddit_result = await post_to_reddit(
                PostToRedditRequest(product_id=product_id),
                current_user=current_user,
                db=db
            )
            results["reddit"] = reddit_result
        except Exception as e:
            results["reddit"] = {"success": False, "error": str(e)}
    
    return {
        "success": all(r.get("success", False) for r in results.values()),
        "results": results
    }

