from fastapi import APIRouter, Depends, HTTPException, status, Form

from typing import List
from tortoise.exceptions import DoesNotExist

import src.crud.trainings as crud

from src.schemas.trainings import TrainingInSchema, TrainingOutSchema, TrainingRequest
from src.schemas.users import UserOutSchema

from src.database.models import Trainings, Models

from src.auth.jwthandler import (
    get_current_user,
)

from src.module.ai import ai_training_process


router = APIRouter(tags=["Trainings"])

@router.post(
    "/trainings", response_model=List[TrainingOutSchema], dependencies=[Depends(get_current_user)],
    summary="Start training for your own special model with some datasets."
)
async def generate_training(
    req: TrainingRequest,
    current_user: UserOutSchema = Depends(get_current_user)
) -> List[TrainingOutSchema]:
    try:
        if current_user.is_admin:
            model = await Models.get(id=req.model_id)
        model = await Models.get(id=req.model_id, user_id=current_user.id)
    except DoesNotExist as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Model {req.model_id} does not exist!",
        ) from e

    result = []
    for dataset_id in req.dataset_ids:
        training_result = await ai_training_process(req.model_id, dataset_id)
        result.append(await crud.create_training(TrainingInSchema.model_validate(training_result)))
    return result


@router.get(
    "/trainings", response_model=List[TrainingOutSchema], dependencies=[Depends(get_current_user)],
    summary="List training logs for your own models. If you are admin, you can see whole training logs in this system."
)
async def training_list(current_user: UserOutSchema = Depends(get_current_user)) -> List[TrainingOutSchema]:
    if current_user.is_admin:
        return await TrainingOutSchema.from_queryset(Trainings.all())
    return await TrainingOutSchema.from_queryset(Trainings.filter(model__user_id=current_user.id))


@router.get(
    "/trainings/{training_id}", response_model=TrainingOutSchema, dependencies=[Depends(get_current_user)],
    summary="Get special training log for your own model. If you are admin, you can see any training log."
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
