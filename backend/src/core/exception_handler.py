from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

import src.core.exception as custom_exception


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(custom_exception.UserNotFound)
    async def user_not_found_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=404,
            content={
                "message": "Пользователь не найден.",
                "error_type": "UserNotFound",
            },
        )

    @app.exception_handler(custom_exception.InvalidPassword)
    async def invalid_password_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=401,
            content={"message": "Неверный пароль.", "error_type": "InvalidPassword"},
        )

    @app.exception_handler(custom_exception.UserAlreadyExists)
    async def user_already_exists_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=409,
            content={
                "message": "Пользователь уже существует.",
                "error_type": "UserAlreadyExists",
            },
        )

    @app.exception_handler(custom_exception.URLNotFound)
    async def url_not_found_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=404,
            content={
                "message": "Ссылка устарела или не существует.",
                "error_type": "URLNotFound",
            },
        )

    @app.exception_handler(custom_exception.ListEmpty)
    async def list_empty_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=404,
            content={"message": "Список пуст.", "error_type": "ListEmpty"},
        )

    @app.exception_handler(custom_exception.RedirCreateError)
    async def redir_create_error_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=409,
            content={
                "message": "Данный url уже занят.",
                "error_type": "RedirCreateError",
            },
        )
