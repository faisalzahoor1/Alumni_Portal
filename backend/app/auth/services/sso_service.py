from app.core.constants import Roles


class DummySSOService:

    @staticmethod
    async def login(registration_no: str, password: str):

        return {
            "user_id": "student_001",
            "registration_no": registration_no,
            "name": "Muhammad Faisal Zahoor",
            "email": "student@cui.edu.pk",
            "department": "Computer Science",
            "semester": 8,
            "role": Roles.STUDENT
        }