from pydantic import BaseModel, Field, field_validator


class RedirRequestSchema(BaseModel):
    default_url: str = Field(max_length=255)
    custom_url: str = Field(max_length=255, default="default")

    @field_validator("default_url", mode="before")
    @classmethod
    def add_default_url(cls, v: str) -> str:
        if not v:
            return v
        if v.startswith(("http://", "https://")):
            return v
        return f"https://{v}"
    

class RedirResponseSchema(BaseModel):
#    uuid: UUID
#    user_uuid: UUID
    default_url: str
    redir_url: str
    redir_count: int