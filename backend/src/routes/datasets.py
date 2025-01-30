import os
import uuid
import io

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form

from typing import List
from tortoise.contrib.fastapi import HTTPNotFoundError
from tortoise.exceptions import DoesNotExist

import src.crud.datasets as crud

from src.schemas.token import Status
from src.schemas.datasets import DataSetInSchema, DataSetOutSchema, ImageInSchema
from src.schemas.users import UserOutSchema

from src.database.models import DataSets

from src.auth.jwthandler import (
    get_current_user,
)

from src.module.image import get_image_metadata, clone_image, generate_thumbnail_of_dataset

router = APIRouter(tags=["Datasets"])

UPLOAD_DIR = "./storage/datasets"

@router.post(
    "/datasets", response_model=DataSetOutSchema, dependencies=[Depends(get_current_user)],
    summary="Create new dataset by uploading images.",
)
async def create_dataset(
    name: str = Form(None),
    files: List[UploadFile] = File(...),
    current_user: UserOutSchema = Depends(get_current_user)
) -> DataSetOutSchema:
    directory_name = str(uuid.uuid4())
    dataset_path = UPLOAD_DIR + "/" + directory_name
    if not os.path.exists(dataset_path):
        os.mkdir(dataset_path)

    images = []
    for idx, file in enumerate(files):
        file_path = dataset_path + "/" + str(idx) + "-" + file.filename
        with open(file_path, "wb") as buffer:
            readable_file = await file.read()
            buffer.write(readable_file)
            metadata = get_image_metadata(file_path)
        images.append({
            "name": file.filename,
            "file_path": file_path,
            "metadata": metadata
        })

    generate_thumbnail_of_dataset(dataset_path)

    return await crud.create_dataset(DataSetInSchema.model_validate({
        "name": name or directory_name,
        "directory_path": dataset_path,
        "user_id": current_user.id,
        "sample_count": len(images),
        "metadata": [ele.get("metadata", None) for ele in images],
        "parent_id": None,
    }), [
        ImageInSchema.model_validate(ele)
        for ele in images
    ])


@router.post(
    "/datasets/{dataset_id}", response_model=DataSetOutSchema, dependencies=[Depends(get_current_user)],
    summary="Clone dataset by changing brightness or by adding gaussian noise.",
)
async def clone_dataset(
    dataset_id: int,
    brightness: float = Form(...),
    noise: float = Form(...),
    current_user: UserOutSchema = Depends(get_current_user)
) -> DataSetOutSchema:
    try:
        if current_user.is_admin:
            dataset = await DataSetOutSchema.from_queryset_single(DataSets.get(id=dataset_id))
        dataset = await DataSetOutSchema.from_queryset_single(DataSets.get(id=dataset_id, user_id=current_user.id))
    except DoesNotExist as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dataset does not exist!",
        ) from e

    directory_name = str(uuid.uuid4())
    dataset_path = f"{UPLOAD_DIR}/{directory_name}"
    # if not os.path.exists(dataset_path):
    #     os.mkdir(dataset_path)

    images = []
    for idx, image in enumerate(dataset.dataset_images):
        origin_file_path = image.file_path
        clone_image(origin_file_path, brightness, noise)

        file_path = f"{dataset_path}/{brightness}_{noise}_{str(idx)}-{image.name}"
        # with open(origin_file_path, "rb") as file:
        #     with open(file_path, "wb") as buffer:
        #         readable_file = file.read()
        #         buffer.write(readable_file)
        #         metadata = await get_image_metadata(io.BytesIO(readable_file))
        # images.append({
        #     "name": file.filename,
        #     "file_path": file_path,
        #     "metadata": metadata
        # })
    return dataset

    # return await crud.create_dataset(DataSetInSchema.model_validate({
    #     "name": directory_name,
    #     "directory_path": dataset_path,
    #     "user_id": current_user.id,
    #     "sample_count": len(images),
    #     "metadata": [ele.get("metadata", None) for ele in images],
    #     "parent_id": None,
    # }), [
    #     ImageInSchema.model_validate(ele)
    #     for ele in images
    # ])


@router.get(
    "/datasets", response_model=List[DataSetOutSchema], dependencies=[Depends(get_current_user)],
    summary="List your own datasets. If you are admin, you can list whole datasets in this system.",
)
async def dataset_list(current_user: UserOutSchema = Depends(get_current_user)) -> List[DataSetOutSchema]:
    if current_user.is_admin:
        return await DataSetOutSchema.from_queryset(DataSets.all())
    return await DataSetOutSchema.from_queryset(DataSets.filter(user_id=current_user.id))


@router.get(
    "/datasets/{dataset_id}", response_model=DataSetOutSchema, dependencies=[Depends(get_current_user)],
    summary="Get your own special dataset. If you are admin, you can get anyone's dataset."
)
async def dataset_detail(dataset_id: int, current_user: UserOutSchema = Depends(get_current_user)) -> DataSetOutSchema:
    try:
        if current_user.is_admin:
            return await DataSetOutSchema.from_queryset_single(DataSets.get(id=dataset_id))
        return await DataSetOutSchema.from_queryset_single(DataSets.get(id=dataset_id, user_id=current_user.id))
    except DoesNotExist as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dataset does not exist!",
        ) from e


@router.delete(
    "/datasets/{dataset_id}",
    response_model=Status,
    responses={404: {"model": HTTPNotFoundError}},
    dependencies=[Depends(get_current_user)],
    summary="Only admin can remove special dataset."
)
async def delete_dataset(
    dataset_id: int, current_user: UserOutSchema = Depends(get_current_user)
) -> Status:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not admin!",
        )
    return await crud.delete_dataset(dataset_id)
