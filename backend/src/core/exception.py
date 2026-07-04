class BaseAppException(Exception):
    """Базовый класс кастомных ошибок."""

    pass


class UserNotFound(BaseAppException):
    """Юзер не найден."""

    pass


class InvalidPassword(BaseAppException):
    """Неверный пароль."""

    pass


class UserAlreadyExists(BaseAppException):
    """Пользователь уже существует."""

    pass


class URLNotFound(BaseAppException):
    """Сыылка устарела или не существует."""

    pass


class ListEmpty(BaseAppException):
    """Список пуст."""

    pass


class RedirCreateError(BaseAppException):
    """Не успешное создание ссылки."""  # noqa: RUF002

    pass