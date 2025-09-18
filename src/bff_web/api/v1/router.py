from fastapi import APIRouter

from .marketing import router as marketing_router
from .tracking import router as tracking_router

router = APIRouter()

router.include_router(marketing_router, prefix="/marketing", tags=["marketing"])
router.include_router(tracking_router, prefix="/tracking", tags=["tracking"])