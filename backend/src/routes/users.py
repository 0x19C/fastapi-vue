from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from tortoise.contrib.fastapi import HTTPNotFoundError

import src.crud.users as crud
from src.auth.users import validate_user
from src.schemas.token import Status
from src.schemas.users import UserInSchema, UserOutSchema, UserLogInSchema

from src.auth.jwthandler import (
    create_access_token,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)


router = APIRouter(tags=["Users"])


@router.post(
    "/register", response_model=UserOutSchema,
    summary="Register user by username, email and password. The default created user is not admin."
)
async def create_user(user: UserInSchema) -> UserOutSchema:
    return await crud.create_user(user)


@router.post("/login", summary="Login with email and password.")
async def login(user: UserLogInSchema):
    user = await validate_user(user)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    token = jsonable_encoder(access_token)
    content = {
        "username": user.username,
        "email": user.email,
        "message": "You've successfully logged in. Welcome back!"
    }
    response = JSONResponse(content=content)
    response.set_cookie(
        "Authorization",
        value=f"Bearer {token}",
        # httponly=True,
        max_age=1800,
        expires=1800,
    )

    return response


@router.get(
    "/users/whoami", response_model=UserOutSchema, dependencies=[Depends(get_current_user)],
    summary="Check who is sent this request by analyzing the cookie."
)
async def read_users_me(current_user: UserOutSchema = Depends(get_current_user)):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": current_user.email}, expires_delta=access_token_expires
    )
    token = jsonable_encoder(access_token)
    response = JSONResponse(content={
        "username": current_user.username,
        "email": current_user.email,
    })
    response.set_cookie(
        "Authorization",
        value=f"Bearer {token}",
        # httponly=True,
        max_age=1800,
        expires=1800,
    )

    return response


@router.post("/logout", summary="Your logout.")
async def logout():
    content = {
        "message": "You've successfully logged out. See you later!"
    }
    response = JSONResponse(content=content)
    response.set_cookie(
        "Authorization",
        value="",
        # httponly=True,
        max_age=1800,
        expires=1,
    )

    return response


@router.delete(
    "/users/{user_id}",
    response_model=Status,
    responses={404: {"model": HTTPNotFoundError}},
    dependencies=[Depends(get_current_user)],
    summary="Only admin can remove special user."
)
async def delete_user(
    user_id: int, current_user: UserOutSchema = Depends(get_current_user)
) -> Status:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not admin!",
        )
    return await crud.delete_user(user_id, current_user)
