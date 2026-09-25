from fastapi import APIRouter, Depends
from app.auth.models.user import User
from app.alumni.dependecies import get_current_alumni_user
from app.alumni.schemas.dashboard_schema import AlumniDashboardStats
from app.alumni.services.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["Alumni Dashboard"])


@router.get("/stats", response_model=AlumniDashboardStats)
async def get_dashboard_stats(current_user: User = Depends(get_current_alumni_user)):
    return await DashboardService.get_dashboard_stats(current_user.id)
