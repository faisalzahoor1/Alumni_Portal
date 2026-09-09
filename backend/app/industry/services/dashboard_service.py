from app.industry.repositories.dashboard_repository import DashboardRepository

class DashboardService:
    
    @staticmethod
    async def get_dashboard_stats(company_id: str) -> dict:
        return await DashboardRepository.get_industry_stats(company_id)
