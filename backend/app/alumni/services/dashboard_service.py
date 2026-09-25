from app.alumni.repositories.dashboard_repository import DashboardRepository
from app.alumni.repositories.profile_repository import AlumniProfileRepository
from app.alumni.schemas.dashboard_schema import AlumniDashboardStats
from app.alumni.schemas.post_schema import PostResponse


class DashboardService:

    @staticmethod
    async def get_dashboard_stats(user_id: str) -> AlumniDashboardStats:
        stats = await DashboardRepository.get_alumni_stats(user_id)
        profile = await AlumniProfileRepository.get_by_user_id(user_id)

        # Calculate profile completion
        completion_fields = [
            "name", "bio", "avatar_url", "graduation_year",
            "degree", "department", "current_company",
            "current_position", "location", "linkedin_url"
        ]
        completed_fields_count = 0
        if profile:
            for field in completion_fields:
                val = getattr(profile, field, None)
                if val is not None and val != "":
                    completed_fields_count += 1
            if profile.skills and len(profile.skills) > 0:
                completed_fields_count += 1

        total_tracked = len(completion_fields) + 1
        percentage = int((completed_fields_count / total_tracked) * 100) if total_tracked > 0 else 0
        profile_completed = percentage >= 80

        recent_post_responses = [
            PostResponse(**p.model_dump()) for p in stats.get("recent_posts", [])
        ]

        return AlumniDashboardStats(
            total_my_posts=stats.get("total_my_posts", 0),
            total_achievements=stats.get("total_achievements", 0),
            total_jobs_posted=stats.get("total_jobs_posted", 0),
            unread_notifications=stats.get("unread_notifications", 0),
            community_feed_posts_count=stats.get("community_feed_posts_count", 0),
            profile_completed=profile_completed,
            profile_completion_percentage=percentage,
            recent_posts=recent_post_responses
        )
