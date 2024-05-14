from sqlalchemy.orm import Session
from passlib.context import CryptContext
from ..models.user import UserEntity, User, UserBase, ProfileForm
from ..exceptions import UserNotFoundException, EmailAlreadyRegisteredException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_user(self, user_id: int) -> User:
        user_entity = self.db.query(UserEntity).filter(UserEntity.id == user_id).first()
        if user_entity is None:
            raise UserNotFoundException(user_id)
        return user_entity.to_pydantic()

    def get_user_by_email(self, email: str) -> User:
        user_entity = self.db.query(UserEntity).filter(UserEntity.email == email).first()
        if user_entity is None:
            return None
        return user_entity.to_pydantic()

    def create_user(self, user_data: UserBase) -> User:
        existing_user = self.db.query(UserEntity).filter(UserEntity.email == user_data.email).first()
        if existing_user:
            raise EmailAlreadyRegisteredException(user_data.email)
        hashed_password = pwd_context.hash(user_data.password)
        user_entity = UserEntity.from_pydantic(user_data, hashed_password)
        self.db.add(user_entity)
        self.db.commit()
        self.db.refresh(user_entity)
        return user_entity.to_pydantic()

    def update_user(self, user_id: int, user_update: ProfileForm) -> User:
        user_entity = self.db.query(UserEntity).filter(UserEntity.id == user_id).first()
        if user_entity is None:
            raise UserNotFoundException(user_id)
        update_data = user_update.model_dump(exclude_unset=True)
        if 'password' in update_data:
            update_data['hashed_password'] = pwd_context.hash(update_data.pop('password'))
        for key, value in update_data.items():
            setattr(user_entity, key, value)
        self.db.commit()
        self.db.refresh(user_entity)
        return user_entity.to_pydantic()

    def delete_user(self, user_id: int):
        user_entity = self.db.query(UserEntity).filter(UserEntity.id == user_id).first()
        if user_entity is None:
            raise UserNotFoundException(user_id)
        self.db.delete(user_entity)
        self.db.commit()
        return user_entity.to_pydantic()
