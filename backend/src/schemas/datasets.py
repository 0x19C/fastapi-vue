from tortoise.contrib.pydantic import pydantic_model_creator
from typing import List

from pydantic import BaseModel

from src.database.models import DataSets, Images
from src.schemas.users import UserOutSchema


class DatasetCloneRequest(BaseModel):
    brightness: float
    noise: float


DataSetInSchema = pydantic_model_creator(
    DataSets, name="DataSetIn", exclude_readonly=True, model_config={"extra": "allow"}
)


ImageInSchema = pydantic_model_creator(
    Images, name="ImageIn", exclude_readonly=True, model_config={"extra": "allow"}
)

ImageOutSchema = pydantic_model_creator(
    Images, name="ImageOut", exclude=["dataset", "created_at", "updated_at"]
)

class DataSetOutSchema(pydantic_model_creator(
    DataSets, name="DataSetOut", exclude=["created_at", "updated_at"]
)):
    user: UserOutSchema
    dataset_images: List[ImageOutSchema]

    class Config:
        from_attributes = True
