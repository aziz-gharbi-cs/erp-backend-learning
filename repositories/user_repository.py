from sqlalchemy import select
from sqlalchemy.orm import Session

from models.employee import Employee
from models.user import User
from models.user import User

class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def save(self, user: User) -> None:
        self.session.add(user)
        self.session.flush()

    def get_all(self) -> list[User]:
        stmt = select(User)
        return list(self.session.scalars(stmt))

    def get_by_id(self, user_id: int) -> User | None:
        stmt = select(User).where(User.id == user_id)
        return self.session.scalar(stmt)

    def get_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        return self.session.scalar(stmt)

    def update(self, user: User) -> None:
        self.session.merge(user)
        self.session.flush()

    def delete(self, user: User) -> None:
        self.session.delete(user)
        self.session.flush()