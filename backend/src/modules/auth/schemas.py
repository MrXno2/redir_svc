from pydantic import BaseModel, Field, model_validator


class AuthRegisterShema(BaseModel):
    login: str = Field(
        min_length=4,
        pattern=r"^[a-zA-Z0-9]+$",
        description="От 4 символов, только a-z A-Z 0-9.",
    )
    password1: str = Field(
        min_length=6, pattern=r"^\S+$", description="От 6 символов, без пробелов."
    )
    password2: str = Field(
        min_length=6, pattern=r"^\S+$", description="От 6 символов, без пробелов."
    )

    @model_validator(mode="after")
    def check_password(self):
        if self.password1 != self.password2:
            raise ValueError("Пароли не совпадают.")
        return self


class AuthLoginShema(BaseModel):
    login: str = Field(
        min_length=4,
        pattern=r"^[a-zA-Z0-9]+$",
        description="От 4 символов, только a-z A-Z 0-9.",
    )
    password: str = Field(
        min_length=6, pattern=r"^\S+$", description="От 6 символов, без пробелов."
    )