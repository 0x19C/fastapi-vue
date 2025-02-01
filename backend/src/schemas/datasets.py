from tortoise.contrib.pydantic import pydantic_model_creator
from typing import List, Optional

from pydantic import BaseModel

from src.database.models import DataSets, Images, DatasetConvertLog
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


class DatasetConvertLogOutSchema(pydantic_model_creator(
    DatasetConvertLog, name="DatasetConvertLogOut", exclude=["dataset", "created_at", "updated_at"]
)):
    origin: "DataSetOutSchema"
    target: "DataSetOutSchema"

    class Config:
        from_attributes = True


class DataSetOutSchema(pydantic_model_creator(
    DataSets, name="DataSetOut", exclude=["created_at", "updated_at"]
)):
    user: UserOutSchema
    dataset_images: List[ImageOutSchema]
    # parent: Optional["DataSetOutSchema"] = None
    # children: List["DataSetOutSchema"] = []
    # log_children: List["DatasetConvertLogOutSchema"] = []
    # log_parent: Optional["DatasetConvertLogOutSchema"] = None

    class Config:
        from_attributes = True
        # arbitrary_types_allowed = True  # Allow custom types
        # populate_by_name = True
        # frozen = True  # Make model immutable
        # annotations=True

DatasetConvertLogOutSchema.model_rebuild()
DataSetOutSchema.model_rebuild()
