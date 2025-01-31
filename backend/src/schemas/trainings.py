from tortoise.contrib.pydantic import pydantic_model_creator
from typing import List
from pydantic import BaseModel

from src.database.models import Trainings
from src.schemas.models import ModelOutSchema
from src.schemas.datasets import DataSetOutSchema


class TrainingRequest(BaseModel):
    model_id: int
    dataset_ids: List[int]


TrainingInSchema = pydantic_model_creator(
    Trainings, name="TrainingIn", exclude_readonly=True, model_config={"extra": "allow"}
)


class TrainingOutSchema(pydantic_model_creator(
    Trainings, name="TrainingOut", exclude=["created_at", "updated_at"]
)):
    model: ModelOutSchema
    dataset: DataSetOutSchema

    class Config:
        from_attributes = True
