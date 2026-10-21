from datetime import datetime, timezone
from typing import List, Optional
import pymongo
from app.database import mongodb
from app.database.collections import Collections
from app.core.constants import Reports
from app.admin.models.report import PostReport


class ReportRepository:

    @staticmethod
    async def find_pending(post_id: str, reporter_id: str) -> Optional[dict]:
        return await mongodb.database[Collections.REPORTS].find_one(
            {"post_id": post_id, "reporter_id": reporter_id, "status": Reports.PENDING}
        )

    @staticmethod
    async def create(report: PostReport) -> PostReport:
        result = await mongodb.database[Collections.REPORTS].insert_one(report.model_dump(exclude={"id"}))
        report.id = str(result.inserted_id)
        return report

    @staticmethod
    async def list_by_status(status: str) -> List[dict]:
        cursor = mongodb.database[Collections.REPORTS].find({"status": status}).sort("created_at", pymongo.DESCENDING)
        docs = []
        async for doc in cursor:
            doc["id"] = str(doc.pop("_id"))
            docs.append(doc)
        return docs

    @staticmethod
    async def count_pending_for_post(post_id: str) -> int:
        return await mongodb.database[Collections.REPORTS].count_documents({"post_id": post_id, "status": Reports.PENDING})

    @staticmethod
    async def resolve_for_post(post_id: str, status: str) -> int:
        result = await mongodb.database[Collections.REPORTS].update_many(
            {"post_id": post_id, "status": Reports.PENDING},
            {"$set": {"status": status, "resolved_at": datetime.now(timezone.utc)}}
        )
        return result.modified_count

    @staticmethod
    async def count_open() -> tuple[int, int]:
        """(pending reports, distinct posts with pending reports)"""
        collection = mongodb.database[Collections.REPORTS]
        total = await collection.count_documents({"status": Reports.PENDING})
        posts = len(await collection.distinct("post_id", {"status": Reports.PENDING}))
        return total, posts
