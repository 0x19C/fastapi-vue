import shutil
import os

from fastapi import HTTPException, status
from typing import List

from tortoise.exceptions import DoesNotExist, IntegrityError

from src.database.models import DataSets, Images
from src.schemas.datasets import DataSetInSchema, DataSetOutSchema, ImageInSchema
from src.schemas.token import Status


async def create_dataset(dataset: DataSetInSchema, images: List[ImageInSchema]) -> DataSetOutSchema:
    try:
        dataset_obj = await DataSets.create(**dataset.dict(exclude_unset=True))
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sorry, that dataset name already exists.") from e

    try:
        for image in images:
            image.dataset_id = dataset_obj.id
            await Images.create(**image.dict(exclude_unset=True))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sorry, images are not linked to dataset.") from e

    return await DataSetOutSchema.from_queryset_single(DataSets.get(id=dataset_obj.id))


async def delete_dataset(dataset_id) -> Status:
    try:
        dataset = await DataSetOutSchema.from_queryset_single(DataSets.get(id=dataset_id))
        if os.path.exists(dataset.directory_path):
            shutil.rmtree(dataset.directory_path)
    except DoesNotExist as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Dataset {dataset_id} is not found!") from e

    deleted_count = await DataSets.filter(id=dataset_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Dataset {dataset_id} is not found")
    return Status(message=f"Deleted dataset {dataset_id}")
