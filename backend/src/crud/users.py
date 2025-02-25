from fastapi import HTTPException, status
from passlib.context import CryptContext
from tortoise.exceptions import DoesNotExist, IntegrityError

from src.database.models import Users
from src.schemas.token import Status
from src.schemas.users import UserOutSchema


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_user(user) -> UserOutSchema:
    user.password = pwd_context.encrypt(user.password)

    try:
        user_obj = await Users.create(**user.dict(exclude_unset=True))
    except IntegrityError as e:
        raise HTTPException(status_code=401, detail="Sorry, that email already exists.") from e

    return await UserOutSchema.from_tortoise_orm(user_obj)


async def delete_user(user_id, current_user) -> Status:
    try:
        db_user = await UserOutSchema.from_queryset_single(Users.get(id=user_id))
    except DoesNotExist as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} is not found") from e

    if db_user.id == current_user.id:
        deleted_count = await Users.filter(id=user_id).delete()
        if not deleted_count:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} is not found")
        return Status(message=f"Deleted user {user_id}")

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete")
