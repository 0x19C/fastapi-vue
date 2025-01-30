from fastapi import HTTPException, status

from tortoise.exceptions import IntegrityError

from src.database.models import Trainings
from src.schemas.trainings import TrainingInSchema, TrainingOutSchema


async def create_training(training: TrainingInSchema) -> TrainingOutSchema:
    try:
        training_obj = await Trainings.create(**training.dict(exclude_unset=True))
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sorry, You can't register training record.") from e

    return await TrainingOutSchema.from_queryset_single(Trainings.get(id=training_obj.id))
