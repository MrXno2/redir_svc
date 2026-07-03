from src.core.dependencies import get_redir_service
from src.modules.redir.schemas import RedirRequestSchema, RedirResponseSchema
from src.modules.redir.service import RedirService
from src.core.security import auth
from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse


router_api = APIRouter(prefix="/api/redir")

@router_api.post("/add", response_model=RedirResponseSchema)
async def redir_set_url(
    req_data: RedirRequestSchema,
    redir_service: RedirService = Depends(get_redir_service),
    payload = Depends(auth.access_token_required)
) -> RedirResponseSchema:
    user_uuid = payload.sub
    new_url = await redir_service.redir_set_url(
        req_data=req_data,
        user_uuid=user_uuid
    )
    return new_url

@router_api.get("/list")
async def redir_get_list(
    redir_service: RedirService = Depends(get_redir_service),
    payload = Depends(auth.access_token_required)
) -> list[RedirResponseSchema]:
    user_uuid = payload.sub
    return await redir_service.redir_get_list(user_uuid=user_uuid)



router_redir = APIRouter(prefix="")

@router_redir.get("/{redir_url}")
async def redir_in_url(
    redir_url: str,
    redir_service: RedirService = Depends(get_redir_service)
) -> None:
    new_url = await redir_service.redir_get_url(redir_url=redir_url)
    if new_url:
        return RedirectResponse(url=new_url, status_code=302)
