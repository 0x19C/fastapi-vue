from fastapi import APIRouter, Depends, HTTPException, status, Form

from typing import List
from tortoise.contrib.fastapi import HTTPNotFoundError
from tortoise.exceptions import DoesNotExist

import src.crud.models as crud

from src.schemas.token import Status
from src.schemas.models import ModelInSchema, ModelOutSchema, ModelRequest
from src.schemas.users import UserOutSchema

from src.database.models import Models

from src.auth.jwthandler import (
    get_current_user,
)


router = APIRouter(tags=["Models"])

@router.post(
    "/models", response_model=ModelOutSchema, dependencies=[Depends(get_current_user)],
    summary="Create a model by setting your own special model name."
)
async def create_model(
    req: ModelRequest,
    current_user: UserOutSchema = Depends(get_current_user)
) -> ModelOutSchema:
    return await crud.create_model(ModelInSchema.model_validate({
        "name": req.name,
        "user_id": current_user.id,
        "parent_id": None,
    }))


@router.get(
    "/models", response_model=List[ModelOutSchema], dependencies=[Depends(get_current_user)],
    summary="List your own models. If you are admin, you can see whole models in this system."
)
async def model_list(current_user: UserOutSchema = Depends(get_current_user)) -> List[ModelOutSchema]:
    if current_user.is_admin:
        return await ModelOutSchema.from_queryset(Models.all())
    return await ModelOutSchema.from_queryset(Models.filter(user_id=current_user.id))


@router.get(
    "/models/{model_id}", response_model=ModelOutSchema, dependencies=[Depends(get_current_user)],
    summary="Get your own special model. If you are admin, you can see anyone's model."
)
async def model_detail(model_id: int, current_user: UserOutSchema = Depends(get_current_user)) -> ModelOutSchema:
    try:
        if current_user.is_admin:
            return await ModelOutSchema.from_queryset_single(Models.get(id=model_id))
        return await ModelOutSchema.from_queryset_single(Models.get(id=model_id, user_id=current_user.id))
    except DoesNotExist as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Model {model_id} does not exist!",
        ) from e


@router.delete(
    "/models/{model_id}",
    response_model=Status,
    responses={404: {"model": HTTPNotFoundError}},
    dependencies=[Depends(get_current_user)],
    summary="Only admin can remove special model."
)
async def delete_model(
    model_id: int, current_user: UserOutSchema = Depends(get_current_user)
) -> Status:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not admin!",
        )
    return await crud.delete_model(model_id)
