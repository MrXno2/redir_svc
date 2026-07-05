from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from src.core.exception import URLNotFound
from src.core.security import auth
from src.modules.redir.schemas import RedirRequestSchema, RedirResponseSchema
from src.modules.dependencies import RedirServiceDep






router_api = APIRouter(prefix="/api/redir")


@router_api.delete("/del/{redir_url}")
async def redir_del_url(
    redir_url: str,
    redir_service: RedirServiceDep,
    payload = Depends(auth.access_token_required),  # noqa: B008
) -> None:
    user_uuid = payload.sub
    await redir_service.redir_del_url(user_uuid=user_uuid, redir_url=redir_url)


@router_api.post("/add", response_model=RedirResponseSchema)
async def redir_set_url(
    req_data: RedirRequestSchema,
    redir_service: RedirServiceDep,
    payload = Depends(auth.access_token_required),  # noqa: B008
) -> RedirResponseSchema:
    user_uuid = payload.sub
    new_url = await redir_service.redir_set_url(req_data=req_data, user_uuid=user_uuid)
    return new_url


@router_api.get("/list")
async def redir_get_list(
    redir_service: RedirServiceDep,
    payload = Depends(auth.access_token_required),  # noqa: B008
) -> list[RedirResponseSchema]:
    user_uuid = payload.sub
    return await redir_service.redir_get_list(user_uuid=user_uuid)


router_redir = APIRouter(prefix="/go")


@router_redir.get("/{redir_url}")
async def redir_in_url(redir_url: str, redir_service: RedirServiceDep) -> RedirectResponse:
    new_url = await redir_service.redir_get_url(redir_url=redir_url)
    if new_url is None:
        raise URLNotFound()
    return RedirectResponse(url=new_url, status_code=302)


