from typing import TYPE_CHECKING

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from core.security import hash_password, verify_password
from repositories.user_repository import UserRepository
from schemas.auth_schema import RegisterRequest


from models.user import User


class AuthService:

    def __init__(self, session: Session):
        self.session = session
        self.user_repo = UserRepository(session)

    def register(self, request: RegisterRequest) -> "User":

        existing_user = self.user_repo.get_by_username(
            request.username
        )

        if existing_user is not None:
            raise ValueError("Username already exists.")

        user = User(
            username=request.username,
            password_hash=hash_password(request.password),
            name=request.name,
            email=request.email,
            phone_number=request.phone_number,
            address=request.address,
            role=request.role,
        )

        try:
            self.user_repo.save(user)

            self.session.commit()
            self.session.refresh(user)

            return user

        except IntegrityError:
            self.session.rollback()
            raise ValueError("User already exists.")

        except Exception:
            self.session.rollback()
            raise

    def authenticate(
        self,
        username: str,
        password: str,
    ) -> "User":

        user = self.user_repo.get_by_username(username)

        if user is None:
            raise ValueError("Invalid username or password.")

        if not user.is_active:
            raise ValueError("User account is disabled.")

        if not verify_password(
            password,
            user.password_hash,
        ):
            raise ValueError("Invalid username or password.")

        return user