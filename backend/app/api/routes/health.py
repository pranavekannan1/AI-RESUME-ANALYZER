from fastapi import APIRouter

from schemas.response import APIResponse

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/", response_model=APIResponse)
def health_check():
    return APIResponse(
        success=True,
        message="Backend is healthy",
        data={"status": "Running"},
    )
