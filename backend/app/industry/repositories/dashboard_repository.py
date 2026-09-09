from app.database import mongodb
from app.database.collections import Collections

class DashboardRepository:
    
    @staticmethod
    async def get_industry_stats(company_id: str) -> dict:
        jobs_count = await mongodb.database[Collections.JOBS].count_documents({"company_id": company_id})
        
        # We need to join jobs and applications, but for simplicity, we can do two queries
        # Or an aggregation pipeline to count total applicants for this company's jobs.
        pipeline = [
            {"$match": {"company_id": company_id}},
            {"$lookup": {
                "from": Collections.APPLICATIONS,
                "localField": "_id",
                "foreignField": "job_id", # job_id in application is string, _id is ObjectId. Need conversion if they don't match.
                # Assuming job_id is saved as string in Applications
                "let": {"job_id_str": {"$toString": "$_id"}},
                "pipeline": [
                    {"$match": {"$expr": {"$eq": ["$job_id", "$$job_id_str"]}}}
                ],
                "as": "applications"
            }},
            {"$project": {"app_count": {"$size": "$applications"}}},
            {"$group": {"_id": None, "total_applicants": {"$sum": "$app_count"}}}
        ]
        
        cursor = mongodb.database[Collections.JOBS].aggregate(pipeline)
        result = await cursor.to_list(length=1)
        total_applicants = result[0]["total_applicants"] if result else 0
        
        return {
            "total_jobs": jobs_count,
            "total_applicants": total_applicants
        }
