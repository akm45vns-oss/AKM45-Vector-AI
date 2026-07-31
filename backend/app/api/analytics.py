"""Placeholder router — analytics endpoints."""
from fastapi import APIRouter

router = APIRouter()


@router.get("/status")
async def analytics_status():
    return {"message": "Analytics router active — full implementation in Phase 9"}
