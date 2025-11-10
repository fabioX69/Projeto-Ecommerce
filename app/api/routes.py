# app/api/routes.py
from fastapi import APIRouter
from app.api.auth import router as auth_router
from app.api.products import router as products_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(products_router)
