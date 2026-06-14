from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import get_auth_uc, get_current_user_id
from app.schemas.auth import RegisterRequest, TokenResponse
from app.schemas.user import UserPublic
from app.usecases.auth import AuthUseCase

router = APIRouter(prefix="/auth", tags=["auth"])
router = APIRouter()

@router.post("/auth/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def register(request: RegisterRequest, auth_usecase: AuthUseCase = Depends(get_auth_uc)):
    """Эндпоинт регистрации нового пользователя"""
    return await auth_usecase.register(request)


@router.post("/auth/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
    auth_usecase: AuthUseCase = Depends(get_auth_uc)):
    """Эндпоинт входа в систему"""
    access_token = await auth_usecase.login(email=form_data.username,
        password=form_data.password)
    return TokenResponse(access_token=access_token, token_type="bearer")


@router.get("/auth/me", response_model=UserPublic)
async def get_current(user_id: int = Depends(get_current_user_id),
    auth_usecase: AuthUseCase = Depends(get_auth_uc)):  
    """Эндпоинт получения текущего авторизированного пользователя"""
    return await auth_usecase.me(user_id)