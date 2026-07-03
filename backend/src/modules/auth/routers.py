from authx import TokenResponse
from fastapi import APIRouter, Depends, Response
from src.core.dependencies import get_auth_service
from src.modules.auth.service import AuthService
from src.modules.auth.shemas import AuthRequestShema
from src.core.settings import settings

    

router = APIRouter(prefix="/api/auth")



@router.post("/login")
async def login_user(
    req_data: AuthRequestShema,
    response: Response,
    auth_service: AuthService = Depends(get_auth_service)
) -> TokenResponse:
    token = await auth_service.auth_login(req_data=req_data)
    response.set_cookie(settings.JWT_ACCESS_COOKIE_NAME, token.access_token)
    response.set_cookie(settings.JWT_REFRESH_COOKIE_NAME, token.refresh_token)
    return token

@router.post("/register")
async def register_user(
    req_data: AuthRequestShema,
    response: Response,
    auth_service: AuthService = Depends(get_auth_service)
) -> TokenResponse:
    token = await auth_service.auth_register(req_data=req_data)
    response.set_cookie(settings.JWT_ACCESS_COOKIE_NAME, token.access_token)
    response.set_cookie(settings.JWT_REFRESH_COOKIE_NAME, token.refresh_token)
    return token