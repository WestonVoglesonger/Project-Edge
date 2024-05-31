import logging
from typing import List
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from backend.entities.user_entity import UserEntity
from ..models.user import ProfileForm, User, UserBase, UserResponse
from .exceptions import EmailAlreadyRegisteredException, UserNotFoundException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

logger = logging.getLogger(__name__)

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_user(self, user_id: int) -> UserResponse:
        user_entity = self.db.query(UserEntity).filter(UserEntity.id == user_id).first()
        if user_entity is None:
            raise UserNotFoundException(f"User with id {user_id} not found")
        return user_entity.to_user_response()

    def get_user_by_email_no_password(self, email: str) -> UserResponse:
        user_entity = self.db.query(UserEntity).filter(UserEntity.email == email).first()
        if user_entity is None:
            raise UserNotFoundException(f"User with email {email} not found")
        return user_entity.to_user_response()

    def get_user_by_email(self, email: str) -> User:
        user_entity = self.db.query(UserEntity).filter(UserEntity.email == email).first()
        if user_entity is None:
            raise UserNotFoundException(f"User with email {email} not found")
        return user_entity.to_user()
    
    def search_users_by_name(self, name: str) -> List[UserResponse]:
        name_parts = name.split()
        if len(name_parts) == 1:
            # Single part name search
            user_entities = self.db.query(UserEntity).filter(
                UserEntity.first_name.ilike(f"%{name}%") | 
                UserEntity.last_name.ilike(f"%{name}%")
            ).all()
        elif len(name_parts) == 2:
            # Full name search (first and last name)
            first_name, last_name = name_parts
            user_entities = self.db.query(UserEntity).filter(
                UserEntity.first_name.ilike(f"%{first_name}%") & 
                UserEntity.last_name.ilike(f"%{last_name}%")
            ).all()
        else:
            # If name_parts has more than 2 elements, treat it as a single part name search
            user_entities = self.db.query(UserEntity).filter(
                UserEntity.first_name.ilike(f"%{name}%") | 
                UserEntity.last_name.ilike(f"%{name}%")
            ).all()

        return [user_entity.to_user_response() for user_entity in user_entities]

    def create_user(self, user_data: UserBase) -> UserResponse:
        existing_user = self.db.query(UserEntity).filter(UserEntity.email == user_data.email).first()
        if existing_user:
            raise EmailAlreadyRegisteredException(user_data.email)
        hashed_password = pwd_context.hash(user_data.password)
        user_entity = UserEntity.from_new_model(user_data, hashed_password)
        self.db.add(user_entity)
        self.db.commit()
        self.db.refresh(user_entity)
        return user_entity.to_user_response()

    def update_user(self, user_id: int, user_update: ProfileForm) -> UserResponse:
        user_entity = self.db.query(UserEntity).filter(UserEntity.id == user_id).first()
        if user_entity is None:
            raise UserNotFoundException(f"User with id {user_id} not found")
        update_data = user_update.model_dump(exclude_unset=True)
        if 'password' in update_data:
            update_data['hashed_password'] = pwd_context.hash(update_data.pop('password'))
        for key, value in update_data.items():
            setattr(user_entity, key, value)
        self.db.commit()
        self.db.refresh(user_entity)
        return user_entity.to_user_response()

    def delete_user(self, user_id: int) -> UserResponse:
        user_entity = self.db.query(UserEntity).filter(UserEntity.id == user_id).first()
        if user_entity is None:
            raise UserNotFoundException(f"User with id {user_id} not found")
        self.db.delete(user_entity)
        self.db.commit()
        return user_entity.to_user_response()
