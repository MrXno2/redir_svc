class BaseException(Exception):
    """Базовый класс кастомных ошибок."""
    pass


class UserNotFound(BaseException):
    """Юзер не найден."""
    pass


class InvalidPassword(BaseException):
    """Неверный пароль."""
    pass


class UserAlreadyExists(BaseException):
    """Пользователь уже существует."""
    pass


class URLNotFound(BaseException):
    """Сыылка устарела или не существует."""


class ListEmpty(BaseException):
    """Список пуст."""