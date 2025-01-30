from fastapi import APIRouter, Depends, HTTPException, status, Query

from typing import List
from tortoise.exceptions import DoesNotExist

import src.crud.trainings as crud

from src.schemas.trainings import TrainingInSchema, TrainingOutSchema
from src.schemas.users import UserOutSchema

from src.database.models import Trainings, Models

from src.auth.jwthandler import (
    get_current_user,
)

from src.module.ai import ai_training_process


router = APIRouter(tags=["Trainings"])

@router.post(
    "/trainings", response_model=List[TrainingOutSchema], dependencies=[Depends(get_current_user)]
)
async def generate_training(
    model_id: int = Query(...),
    dataset_ids: List[int] = Query(...),
    current_user: UserOutSchema = Depends(get_current_user)
) -> List[TrainingOutSchema]:
    try:
        if current_user.is_admin:
            model = await Models.get(id=model_id)
        model = await Models.get(id=model_id, user_id=current_user.id)
    except DoesNotExist as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Model {model_id} does not exist!",
        ) from e

    result = []
    for dataset_id in dataset_ids:
        training_result = await ai_training_process(model_id, dataset_id)
        result.append(await crud.create_training(TrainingInSchema.model_validate(training_result)))
    return result


@router.get(
    "/trainings", response_model=List[TrainingOutSchema], dependencies=[Depends(get_current_user)]
)
async def training_list(current_user: UserOutSchema = Depends(get_current_user)) -> List[TrainingOutSchema]:
    if current_user.is_admin:
        return await TrainingOutSchema.from_queryset(Trainings.all())
    return await TrainingOutSchema.from_queryset(Trainings.filter(model__user_id=current_user.id))


@router.get(
    "/trainings/{training_id}", response_model=TrainingOutSchema, dependencies=[Depends(get_current_user)]
)
async def model_detail(training_id: int, current_user: UserOutSchema = Depends(get_current_user)) -> TrainingOutSchema:
    try:
        if current_user.is_admin:
            return await TrainingOutSchema.from_queryset_single(Trainings.get(id=training_id))
        return await TrainingOutSchema.from_queryset_single(Trainings.get(id=training_id, model__user_id=current_user.id))
    except DoesNotExist as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Training {training_id} does not exist!",
        ) from e
