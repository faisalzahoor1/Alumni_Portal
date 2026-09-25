from typing import Dict, Any
from app.database import mongodb
from app.database.collections import Collections
from app.alumni.repositories.post_repository import PostRepository
from app.alumni.repositories.notification_repository import NotificationRepository


class DashboardRepository:

    @staticmethod
    async def get_alumni_stats(user_id: str) -> Dict[str, Any]:
        total_my_posts = await PostRepository.count_by_author(user_id)
        total_achievements = await PostRepository.count_by_author_and_type(user_id, "achievement")
        total_jobs_posted = await PostRepository.count_by_author_and_type(user_id, "job_opportunity")
        unread_notifications = await NotificationRepository.count_unread(user_id)
        community_feed_posts_count = await PostRepository.count_feed(roles=["alumni", "industry"])
        recent_posts = await PostRepository.get_by_author(user_id, limit=5, skip=0)

        return {
            "total_my_posts": total_my_posts,
            "total_achievements": total_achievements,
            "total_jobs_posted": total_jobs_posted,
            "unread_notifications": unread_notifications,
            "community_feed_posts_count": community_feed_posts_count,
            "recent_posts": recent_posts
        }
