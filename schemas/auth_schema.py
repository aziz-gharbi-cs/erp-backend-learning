from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RegisterRequest(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=50,
    )

    password: str = Field(
        min_length=8,
        max_length=128,
    )

    name: str

    email: EmailStr

    phone_number: str | None = None

    address: str | None = None

    job_title: str

    role: str = "EMPLOYEE"


class LoginRequest(BaseModel):
    username: str

    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str
    exp: int
    role: str | None = None


class AuthenticatedEmployee(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    name: str
    email: EmailStr
    role: str
    is_active: bool