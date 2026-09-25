from typing import List
from pydantic import BaseModel
from app.alumni.schemas.post_schema import PostResponse


class AlumniDashboardStats(BaseModel):
    total_my_posts: int
    total_achievements: int
    total_jobs_posted: int
    unread_notifications: int
    community_feed_posts_count: int
    profile_completed: bool
    profile_completion_percentage: int
    recent_posts: List[PostResponse] = []
