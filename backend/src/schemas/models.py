from tortoise.contrib.pydantic import pydantic_model_creator

from src.database.models import Models
from src.schemas.users import UserOutSchema


ModelInSchema = pydantic_model_creator(
    Models, name="ModelIn", exclude_readonly=True, model_config={"extra": "allow"}
)


class ModelOutSchema(pydantic_model_creator(
    Models, name="ModelOut", exclude=["created_at", "updated_at"]
)):
    user: UserOutSchema

    class Config:
        from_attributes = True
