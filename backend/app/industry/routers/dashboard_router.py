from fastapi import APIRouter, Depends
from app.auth.models.user import User
from app.auth.dependensies import get_current_industry_user
from app.industry.services.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["Industry Dashboard"])

@router.get("/stats")
async def get_dashboard_stats(current_user: User = Depends(get_current_industry_user)):
    return await DashboardService.get_dashboard_stats(current_user.id)
