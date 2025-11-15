"""
Jukeyman Autonomous Media Station (JAMS) - API v1 Routes
"""
from fastapi import APIRouter

# Import all routers
from app.api.v1.auth import router as auth_router
from app.api.v1.generation import router as generation_router

# Placeholder routers (to be implemented)
products_router = APIRouter()
orders_router = APIRouter()
users_router = APIRouter()
admin_router = APIRouter()
webhooks_router = APIRouter()

# Quick placeholder endpoints
@products_router.get("/")
async def list_products():
    return {"message": "Products API - To be implemented"}

@orders_router.get("/")
async def list_orders():
    return {"message": "Orders API - To be implemented"}

@users_router.get("/")
async def list_users():
    return {"message": "Users API - To be implemented"}

@admin_router.get("/")
async def admin_dashboard():
    return {"message": "Admin API - To be implemented"}

@webhooks_router.post("/stripe")
async def stripe_webhook():
    return {"status": "ok"}

__all__ = [
    "auth_router",
    "generation_router",
    "products_router",
    "orders_router",
    "users_router",
    "admin_router",
    "webhooks_router",
]

