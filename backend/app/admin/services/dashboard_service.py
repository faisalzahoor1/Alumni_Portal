from app.database import mongodb
from app.database.collections import Collections
from app.core.constants import Approval, Roles, University
from app.admin.repositories.notification_repository import AdminNotificationRepository
from app.admin.repositories.post_repository import AdminPostRepository
from app.admin.repositories.report_repository import ReportRepository
from app.admin.schemas.admin_schema import AdminDashboardStats
from app.admin.services.registration_service import RegistrationService


class AdminDashboardService:

    @staticmethod
    async def get_stats() -> AdminDashboardStats:
        db = mongodb.database
        approved = {"$in": [Approval.APPROVED, None]}
        open_reports, reported_posts = await ReportRepository.count_open()
        return AdminDashboardStats(
            pending_registrations=await RegistrationService.count_pending(),
            open_reports=open_reports,
            reported_posts=reported_posts,
            students=await db[Collections.STUDENTS].count_documents({}),
            alumni=await db[Collections.USERS].count_documents({"role": Roles.ALUMNI, "approval_status": approved}),
            industry=await db[Collections.USERS].count_documents({"role": Roles.INDUSTRY, "approval_status": approved}),
            university_posts=await AdminPostRepository.count_by_roles([University.AUTHOR_ROLE]),
            community_posts=await AdminPostRepository.count_by_roles([Roles.ALUMNI, Roles.INDUSTRY]),
            unread_notifications=await AdminNotificationRepository.count_unread(),
        )
