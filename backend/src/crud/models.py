from fastapi import HTTPException, status

from tortoise.exceptions import DoesNotExist, IntegrityError

from src.database.models import Models
from src.schemas.models import ModelInSchema, ModelOutSchema
from src.schemas.token import Status


async def create_model(model: ModelInSchema) -> ModelOutSchema:
    try:
        model_obj = await Models.create(**model.dict(exclude_unset=True))
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sorry, that model name already exists.") from e

    return await ModelOutSchema.from_queryset_single(Models.get(id=model_obj.id))


async def delete_model(model_id) -> Status:
    try:
        await ModelOutSchema.from_queryset_single(Models.get(id=model_id))
    except DoesNotExist as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Model {model_id} is not found!") from e

    deleted_count = await Models.filter(id=model_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Model {model_id} is not found")
    return Status(message=f"Deleted model {model_id}")
