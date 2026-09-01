from fastapi import APIRouter, Depends, File, Form, UploadFile
from app.core.dependencies import get_current_student
from app.student.schemas.additional_info import StudentAdditionalInfoRequest
from app.student.schemas.student import StudentResponse
from app.student.services.student_service import StudentService


router = APIRouter(
    prefix="/student",
    tags=["Student Profile"]
)


@router.get("/me",response_model=StudentResponse)
async def get_my_profile(current_user: dict = Depends(get_current_student)):

    return await StudentService.get_student_by_registration_no( current_user["registration_no"] )


@router.patch("/additional-info",response_model=StudentResponse)
async def update_additional_info(
    linkedin_url: str | None = Form(None),
    instagram_url: str | None = Form(None),
    cv: UploadFile | None = File(None),
    current_user: dict = Depends(get_current_student)
):
    
    request = StudentAdditionalInfoRequest(
        linkedin_url=linkedin_url,
        instagram_url=instagram_url
    )

    return await StudentService.update_additional_info(registration_no=current_user["registration_no"],request=request, cv=cv)