from authx import TokenResponse
from fastapi import APIRouter, Response
from src.core.settings import settings
from src.modules.auth.schemas import AuthRegisterShema, AuthLoginShema
from src.modules.dependencies import AuthServiceDep


router = APIRouter(prefix="/api/auth")


@router.post("/login")
async def login_user(
    req_data: AuthLoginShema,
    response: Response,
    auth_service: AuthServiceDep,
) -> TokenResponse:
    token = await auth_service.auth_login(req_data=req_data)
    response.set_cookie(settings.JWT_ACCESS_COOKIE_NAME, token.access_token)
    response.set_cookie(settings.JWT_REFRESH_COOKIE_NAME, token.refresh_token)
    return token


@router.post("/register")
async def register_user(
    req_data: AuthRegisterShema,
    response: Response,
    auth_service: AuthServiceDep,
) -> TokenResponse | None:
    token = await auth_service.auth_register(req_data=req_data)
    if token:
        response.set_cookie(settings.JWT_ACCESS_COOKIE_NAME, token.access_token)
        response.set_cookie(settings.JWT_REFRESH_COOKIE_NAME, token.refresh_token)
        return token
