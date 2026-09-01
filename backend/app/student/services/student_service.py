from fastapi import HTTPException, status, UploadFile
from datetime import datetime, timezone

from app.student.models.student import Student
from app.student.schemas.student import StudentResponse, CVResponse
from app.student.schemas.additional_info import StudentAdditionalInfoRequest
from app.student.repository.student_repository import StudentRepository
from app.auth.services.file_storage_service import FileStorageService


class StudentService:

    @staticmethod
    async def create_student(student: Student) -> StudentResponse:

        # Check whether student already exists
        existing_student = await StudentRepository.find_by_registration_no(
            student.registration_no
        )

        if existing_student:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Student already exists"
            )

        # Create student
        student_id = await StudentRepository.create_student(
            student
        )

        # Fetch the newly created student
        created_student = await StudentRepository.find_by_id(
            student_id
        )

        if not created_student:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create student"
            )

        return StudentResponse(
            id=created_student.id,
            registration_no=created_student.registration_no,
            name=created_student.name,
            email=created_student.email,
            linkedin_url=created_student.linkedin_url,
            instagram_url=created_student.instagram_url
        )

    @staticmethod
    async def get_student_by_registration_no(registration_no: str) -> StudentResponse:

        student = await StudentRepository.find_by_registration_no(registration_no)

        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found"
            )

        return StudentResponse(
            id=student.id,
            registration_no=student.registration_no,
            name=student.name,
            email=student.email,
            linkedin_url=student.linkedin_url,
            instagram_url=student.instagram_url,
            cv=CVResponse(**student.cv.model_dump()) if student.cv else None
        )

    @staticmethod
    async def get_student_by_email(
        email: str
    ) -> StudentResponse:

        student = await StudentRepository.find_by_email(
            email
        )

        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found"
            )

        return StudentResponse(
            id=student.id,
            registration_no=student.registration_no,
            name=student.name,
            email=student.email,
            linkedin_url=student.linkedin_url,
            instagram_url=student.instagram_url
        )

    MAX_CV_SIZE = 5 * 1024 * 1024  # 5 MB

    @staticmethod
    async def update_additional_info(registration_no: str,request: StudentAdditionalInfoRequest, cv: UploadFile | None = None) -> StudentResponse:

        student = await StudentRepository.find_by_registration_no(registration_no)

        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found"
            )
        cv_data = None
        if cv:

            # Check content type
            if cv.content_type != "application/pdf":

                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only PDF files are allowed"
                )


            # Read PDF
            contents = await cv.read()


            # Check size
            if len(contents) > StudentService.MAX_CV_SIZE:

                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="CV size must not exceed 5 MB"
                )


            # Move pointer back to beginning
            await cv.seek(0)


            # Upload to Cloudinary
            upload_result = await FileStorageService.upload_cv(
                cv
            )


            # Create metadata
            cv_data = {
                "file_name": cv.filename,
                "file_url": upload_result["file_url"],
                "file_size": len(contents),
                "content_type": cv.content_type,
                "uploaded_at": datetime.now(timezone.utc)
            }

        
        await StudentRepository.update_additional_info(
            registration_no=registration_no,
            linkedin_url=(
                str(request.linkedin_url)
                if request.linkedin_url
                else None
            ),
            instagram_url=(
                str(request.instagram_url)
                if request.instagram_url
                else None
            ),
            cv_data=cv_data
        )

        updated_student = await StudentRepository.find_by_email(student.email)

        if not updated_student:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update student"
            )

        return StudentResponse(
            id=updated_student.id,
            registration_no=updated_student.registration_no,
            name=updated_student.name,
            email=updated_student.email,
            linkedin_url=updated_student.linkedin_url,
            instagram_url=updated_student.instagram_url,
            cv=updated_student.cv
        )