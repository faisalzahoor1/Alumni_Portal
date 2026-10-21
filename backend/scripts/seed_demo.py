"""
Seed demo accounts and posts for local testing: 5 students, 5 alumni and 5 industry
partners, with feed posts from the alumni and industry accounts.

Usage, from the backend folder:
    .venv/bin/python -m scripts.seed_demo
Safe to re-run: accounts are upserted and the demo accounts' posts are recreated.
"""

import asyncio
from datetime import datetime, timedelta, timezone

from app.core.constants import Approval, Roles
from app.core.security import hash_password
from app.database import mongodb
from app.database.collections import Collections
from app.database.mongodb import connect_to_mongodb

PASSWORD = "Demo@1234"
STUDENT_EMAIL_DOMAIN = "students.cui.edu.pk"  # matches DummySSOService

STUDENTS = [
    {"registration_no": "FA21-BCS-001", "name": "Ayesha Khan"},
    {"registration_no": "FA21-BCS-002", "name": "Hamza Ali"},
    {"registration_no": "FA22-BSE-003", "name": "Fatima Noor"},
    {"registration_no": "SP22-BCS-004", "name": "Usman Tariq"},
    {"registration_no": "FA23-BAI-005", "name": "Zainab Riaz"},
]

ALUMNI = [
    {
        "email": "alumni1@demo.com", "name": "Sara Ahmed", "graduation_year": 2018, "degree": "BS Computer Science",
        "department": "Computer Science", "current_company": "Google", "current_position": "Software Engineer",
        "location": "Dublin, Ireland", "skills": ["Go", "Kubernetes", "Distributed Systems"],
        "bio": "Building reliable infrastructure at scale. Happy to mentor students interested in backend roles.",
        "posts": [
            {"post_type": "achievement", "title": "Promoted to Senior Software Engineer at Google",
             "content": "Six years after graduating from COMSATS, I've been promoted to Senior SWE. Grateful to my teachers and the friends who pushed me through those late-night labs.",
             "tags": ["career", "google", "milestone"], "media_urls": ["https://picsum.photos/seed/alumni1a/800/500"]},
            {"post_type": "general", "title": "Free mock interviews for final-year students",
             "content": "I'm offering 10 free 45-minute mock coding interviews this month. Message me with your CV and preferred time slot.",
             "tags": ["mentorship", "interviews"]},
        ],
    },
    {
        "email": "alumni2@demo.com", "name": "Bilal Hussain", "graduation_year": 2016, "degree": "BS Software Engineering",
        "department": "Software Engineering", "current_company": "Careem", "current_position": "Engineering Manager",
        "location": "Dubai, UAE", "skills": ["Leadership", "Java", "Microservices"],
        "bio": "Engineering manager working on ride-hailing and payments.",
        "posts": [
            {"post_type": "job_opportunity", "title": "Careem is hiring backend engineers",
             "content": "My team is looking for backend engineers with 1-3 years of experience. Java or Kotlin preferred. Referrals available for COMSATS grads.",
             "job_title": "Backend Engineer", "company_name": "Careem", "job_apply_url": "https://example.com/careem/backend",
             "tags": ["hiring", "backend", "dubai"]},
            {"post_type": "announcement", "title": "Alumni meetup in Dubai, 15 November",
             "content": "All COMSATS alumni in the UAE are invited to an evening meetup. Dinner is on us. Reply here if you're coming.",
             "tags": ["meetup", "networking"]},
        ],
    },
    {
        "email": "alumni3@demo.com", "name": "Mariam Siddiqui", "graduation_year": 2020, "degree": "BS Artificial Intelligence",
        "department": "Computer Science", "current_company": "Stanford University", "current_position": "PhD Researcher",
        "location": "California, USA", "skills": ["PyTorch", "NLP", "Research"],
        "bio": "PhD candidate researching low-resource language models, including Urdu.",
        "posts": [
            {"post_type": "achievement", "title": "Our paper was accepted at NeurIPS 2026",
             "content": "Our work on Urdu language models got accepted at NeurIPS! Huge thanks to my co-authors. Happy to talk to anyone curious about applying for a PhD.",
             "tags": ["research", "ai", "neurips"], "media_urls": ["https://picsum.photos/seed/alumni3a/800/500"]},
            {"post_type": "general", "title": "How I prepared my PhD applications",
             "content": "A short guide: start emailing professors early, write a focused statement of purpose, and get research experience during your undergrad, even if it's small.",
             "tags": ["phd", "higher-studies"]},
        ],
    },
    {
        "email": "alumni4@demo.com", "name": "Ahmed Raza", "graduation_year": 2015, "degree": "BS Electrical Engineering",
        "department": "Electrical Engineering", "current_company": "Raza Robotics", "current_position": "Founder & CEO",
        "location": "Lahore, Pakistan", "skills": ["Robotics", "Embedded Systems", "Startups"],
        "bio": "Founder of a robotics startup building warehouse automation.",
        "posts": [
            {"post_type": "job_opportunity", "title": "Summer internships at Raza Robotics",
             "content": "We're taking 5 interns this summer for embedded systems and computer vision. Paid, in Lahore, and a great fit for third-year students.",
             "job_title": "Robotics Intern", "company_name": "Raza Robotics", "job_apply_url": "https://example.com/raza/internships",
             "tags": ["internship", "robotics", "lahore"]},
            {"post_type": "achievement", "title": "Raza Robotics closes its seed round",
             "content": "We raised our seed round to scale warehouse robots across Pakistan. It all started with a final-year project at COMSATS.",
             "tags": ["startup", "funding"], "media_urls": ["https://picsum.photos/seed/alumni4a/800/500"]},
        ],
    },
    {
        "email": "alumni5@demo.com", "name": "Hina Javed", "graduation_year": 2019, "degree": "BS Computer Science",
        "department": "Computer Science", "current_company": "Microsoft", "current_position": "Product Designer",
        "location": "Seattle, USA", "skills": ["UX Design", "Figma", "User Research"],
        "bio": "Designer who used to be a developer. Ask me about switching to UX.",
        "posts": [
            {"post_type": "general", "title": "Moving from development to UX design",
             "content": "Three years ago I was writing code; now I design products at Microsoft. If you're curious about UX, start by redesigning apps you use every day and write up your reasoning.",
             "tags": ["design", "career-switch"]},
            {"post_type": "announcement", "title": "Free portfolio review session this Saturday",
             "content": "I'll be reviewing design portfolios live over video call this Saturday at 8 PM PKT. Drop your link in the comments.",
             "tags": ["design", "portfolio"]},
        ],
    },
]

INDUSTRY = [
    {
        "email": "industry1@demo.com", "company_name": "Systems Limited", "industry_type": "IT Services",
        "location": "Lahore, Pakistan", "employee_count": "5000+", "website": "https://example.com/systems",
        "description": "One of Pakistan's largest software services companies.",
        "posts": [
            {"post_type": "job_opportunity", "title": "Graduate Trainee Program 2027",
             "content": "Applications are open for our graduate trainee program. Six months of paid training followed by placement in a delivery team.",
             "job_title": "Graduate Trainee Engineer", "job_apply_url": "https://example.com/systems/gtp", "tags": ["graduates", "training"]},
            {"post_type": "announcement", "title": "Campus recruitment drive at COMSATS",
             "content": "Our recruitment team visits the COMSATS Islamabad campus on 2 December. Bring your CV and a laptop for the coding test.",
             "tags": ["campus-drive", "recruitment"]},
        ],
    },
    {
        "email": "industry2@demo.com", "company_name": "Arbisoft", "industry_type": "Software",
        "location": "Lahore, Pakistan", "employee_count": "1000-5000", "website": "https://example.com/arbisoft",
        "description": "Product engineering for education, travel and fintech companies.",
        "posts": [
            {"post_type": "job_opportunity", "title": "Hiring Python / Django developers",
             "content": "We're hiring Python developers with 0-2 years of experience. Hybrid work, health insurance and a strong learning culture.",
             "job_title": "Associate Software Engineer (Python)", "job_apply_url": "https://example.com/arbisoft/python", "tags": ["python", "django", "hiring"]},
            {"post_type": "job_opportunity", "title": "Frontend internship (React)",
             "content": "Three-month paid internship for students who know React basics. Strong performers get full-time offers.",
             "job_title": "Frontend Intern", "job_apply_url": "https://example.com/arbisoft/frontend-intern", "tags": ["react", "internship"]},
        ],
    },
    {
        "email": "industry3@demo.com", "company_name": "Jazz", "industry_type": "Telecommunications",
        "location": "Islamabad, Pakistan", "employee_count": "5000+", "website": "https://example.com/jazz",
        "description": "Pakistan's leading digital operator.",
        "posts": [
            {"post_type": "announcement", "title": "Jazz xlr8 startup accelerator: applications open",
             "content": "Student-founded startups can apply to our 12-week accelerator. Mentorship, office space and funding opportunities.",
             "tags": ["startups", "accelerator"], "media_urls": ["https://picsum.photos/seed/industry3a/800/500"]},
            {"post_type": "job_opportunity", "title": "Data analyst positions",
             "content": "Looking for fresh graduates with strong SQL and Python skills to join our data team in Islamabad.",
             "job_title": "Data Analyst", "job_apply_url": "https://example.com/jazz/data-analyst", "tags": ["data", "sql", "islamabad"]},
        ],
    },
    {
        "email": "industry4@demo.com", "company_name": "10Pearls", "industry_type": "Software",
        "location": "Karachi, Pakistan", "employee_count": "1000-5000", "website": "https://example.com/10pearls",
        "description": "Digital transformation partner for global companies.",
        "posts": [
            {"post_type": "job_opportunity", "title": "QA Automation Engineers needed",
             "content": "We need QA engineers who know Selenium or Cypress. Fresh graduates with good projects are welcome to apply.",
             "job_title": "QA Automation Engineer", "job_apply_url": "https://example.com/10pearls/qa", "tags": ["qa", "automation"]},
            {"post_type": "general", "title": "What we look for in a fresh graduate's CV",
             "content": "Real projects beat long lists of courses. Link your GitHub, show what you built and explain your role in team projects.",
             "tags": ["cv-tips", "careers"]},
        ],
    },
    {
        "email": "industry5@demo.com", "company_name": "NetSol Technologies", "industry_type": "Fintech",
        "location": "Lahore, Pakistan", "employee_count": "1000-5000", "website": "https://example.com/netsol",
        "description": "Software for the global leasing and finance industry.",
        "posts": [
            {"post_type": "job_opportunity", "title": ".NET developers for our leasing platform",
             "content": "Join the team behind our flagship leasing platform. C# and SQL Server experience required.",
             "job_title": "Software Engineer (.NET)", "job_apply_url": "https://example.com/netsol/dotnet", "tags": [".net", "csharp", "fintech"]},
            {"post_type": "achievement", "title": "NetSol wins Fintech Company of the Year",
             "content": "We're proud to win Fintech Company of the Year. Many of our award-winning engineers are COMSATS graduates!",
             "tags": ["award", "fintech"], "media_urls": ["https://picsum.photos/seed/industry5a/800/500"]},
        ],
    },
]


async def upsert_user(email: str, role: str, now: datetime) -> str:
    users = mongodb.database[Collections.USERS]
    existing = await users.find_one({"email": email})
    if existing and existing["role"] != role:
        raise SystemExit(f"{email} already belongs to a {existing['role']} account; remove it first.")
    fields = {
        "hashed_password": hash_password(PASSWORD),
        "role": role,
        "is_verified": True,
        "approval_status": Approval.APPROVED,
        "updated_at": now,
    }
    if existing:
        await users.update_one({"_id": existing["_id"]}, {"$set": fields})
        return str(existing["_id"])
    result = await users.insert_one({"email": email, **fields, "created_at": now})
    return str(result.inserted_id)


async def upsert_profile(collection: str, user_id: str, fields: dict, now: datetime):
    await mongodb.database[collection].update_one(
        {"user_id": user_id},
        {"$set": {**fields, "updated_at": now}, "$setOnInsert": {"user_id": user_id, "created_at": now}},
        upsert=True,
    )


async def replace_posts(user_id: str, role: str, author_name: str, posts: list[dict], company_name: str | None, now: datetime, offset: int):
    collection = mongodb.database[Collections.POSTS]
    await collection.delete_many({"author_id": user_id})
    for i, post in enumerate(posts):
        # Spread posts over the last few days so the feed has a natural order
        created = now - timedelta(hours=offset * 7 + i * 31)
        await collection.insert_one({
            "author_id": user_id,
            "author_name": author_name,
            "author_role": role,
            "author_avatar": None,
            "title": post["title"],
            "content": post["content"],
            "media_urls": post.get("media_urls", []),
            "job_apply_url": post.get("job_apply_url"),
            "external_urls": [],
            "company_name": post.get("company_name", company_name if post["post_type"] == "job_opportunity" else None),
            "job_title": post.get("job_title"),
            "post_type": post["post_type"],
            "tags": post.get("tags", []),
            "likes_count": 0,
            "dislikes_count": 0,
            "comments_count": 0,
            "is_public": True,
            "created_at": created,
            "updated_at": created,
        })


async def main():
    await connect_to_mongodb()
    now = datetime.now(timezone.utc)

    for s in STUDENTS:
        await mongodb.database[Collections.STUDENTS].update_one(
            {"registration_no": s["registration_no"]},
            {
                "$set": {"name": s["name"], "email": f"{s['registration_no'].lower()}@{STUDENT_EMAIL_DOMAIN}", "updated_at": now},
                "$setOnInsert": {"registration_no": s["registration_no"], "linkedin_url": None, "instagram_url": None,
                                 "cv": None, "avatar_url": None, "created_at": now},
            },
            upsert=True,
        )

    for n, a in enumerate(ALUMNI):
        user_id = await upsert_user(a["email"], Roles.ALUMNI, now)
        profile = {k: v for k, v in a.items() if k not in ("posts",)}
        profile.setdefault("achievements", [])
        await upsert_profile(Collections.ALUMNI_PROFILES, user_id, profile, now)
        await replace_posts(user_id, Roles.ALUMNI, a["name"], a["posts"], a["current_company"], now, n * 2)

    for n, c in enumerate(INDUSTRY):
        user_id = await upsert_user(c["email"], Roles.INDUSTRY, now)
        profile = {k: v for k, v in c.items() if k not in ("posts", "email")}
        await upsert_profile(Collections.INDUSTRY_PROFILES, user_id, profile, now)
        await replace_posts(user_id, Roles.INDUSTRY, c["company_name"], c["posts"], c["company_name"], now, n * 2 + 1)

    posts = sum(len(x["posts"]) for x in ALUMNI + INDUSTRY)
    print(f"Seeded {len(STUDENTS)} students, {len(ALUMNI)} alumni, {len(INDUSTRY)} industry accounts and {posts} posts.\n")
    print(f"Password for every account: {PASSWORD}")
    print("Students (Student tab, registration number):", ", ".join(s["registration_no"] for s in STUDENTS))
    print("Alumni (Alumni / Industry tab):", ", ".join(a["email"] for a in ALUMNI))
    print("Industry (Alumni / Industry tab):", ", ".join(c["email"] for c in INDUSTRY))


if __name__ == "__main__":
    asyncio.run(main())
