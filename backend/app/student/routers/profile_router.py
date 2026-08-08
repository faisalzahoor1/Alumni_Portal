from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_student
from app.student.schemas.additional_info import StudentAdditionalInfoRequest
from app.student.schemas.student import StudentResponse
from app.student.services.student_service import StudentService


router = APIRouter(
    prefix="/student",
    tags=["Student"]
)


@router.get("/me",response_model=StudentResponse)
async def get_my_profile(current_user: dict = Depends(get_current_student)):

    return await StudentService.get_student_by_registration_no( current_user["registration_no"] )


@router.patch("/additional-info",response_model=StudentResponse)
async def update_additional_info(request: StudentAdditionalInfoRequest,current_user: dict = Depends(get_current_student)):

    return await StudentService.update_additional_info(registration_no=current_user["registration_no"],request=request)