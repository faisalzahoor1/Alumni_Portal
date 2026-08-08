from datetime import datetime, timezone

from app.database import mongodb
from app.auth.models.user import User
from app.database.collections import Collections
from app.student.models.student import Student


class StudentRepository:

    @staticmethod
    async def create_student(student: Student) -> str:

        student_dict = student.model_dump(
            mode="json"
        )

        result = await mongodb.database[
            Collections.STUDENTS
        ].insert_one(student_dict)

        return str(result.inserted_id)

    @staticmethod
    async def find_by_registration_no(registration_no: str) -> Student | None:

        document = await mongodb.database[Collections.STUDENTS].find_one(
            {
                "registration_no": registration_no
            }
        )

        if not document:
            return None

        document["id"] = str(
            document.pop("_id")
        )

        return Student(**document)

    @staticmethod
    async def find_by_email(email: str) -> Student | None:

        document = await mongodb.database[
            Collections.STUDENTS
        ].find_one(
            {
                "email": email
            }
        )

        if not document:
            return None

        document["id"] = str(
            document.pop("_id")
        )

        return Student(**document)

    @staticmethod
    async def find_by_id(
        student_id: str
    ) -> Student | None:

        from bson import ObjectId

        document = await mongodb.database[
            Collections.STUDENTS
        ].find_one(
            {
                "_id": ObjectId(student_id)
            }
        )

        if not document:
            return None

        document["id"] = str(
            document.pop("_id")
        )

        return Student(**document)

    @staticmethod
    async def update_additional_info(registration_no: str,linkedin_url: str | None,instagram_url: str | None):

        update_data = {"updated_at": datetime.now(timezone.utc)}

        if linkedin_url is not None:
            update_data["linkedin_url"] = linkedin_url

        if instagram_url is not None:
            update_data["instagram_url"] = instagram_url

        await mongodb.database[Collections.STUDENTS].update_one(
            {
                "registration_no": registration_no
            },
            {
                "$set": update_data
            }
        )