from pydantic import BaseModel


class TokenData(BaseModel):
    name: str
    email: str
    id: int


class Token(BaseModel):
    access_token: str
    token_type: str | None = 'bearer'
