from app.core.constants import Roles


class DummySSOService:
    """
    Placeholder for the university SSO. Accepts any credentials and derives a
    per-student identity from the registration number, so every student gets a
    unique email (the students collection has a unique email index).
    """

    EMAIL_DOMAIN = "students.cui.edu.pk"

    @staticmethod
    async def login(registration_no: str, password: str):

        registration_no = registration_no.strip().upper()

        return {
            "user_id": registration_no,
            "registration_no": registration_no,
            "name": f"Student {registration_no}",
            "email": f"{registration_no.lower()}@{DummySSOService.EMAIL_DOMAIN}",
            "role": Roles.STUDENT
        }
