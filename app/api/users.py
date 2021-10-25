from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import get_current_active_user, get_current_active_superuser
from app.crud.users import get_by_email, create
from app.models.users import Users
from app.schemas.users import UserIn, UserOut

router = APIRouter()


@router.post('/', response_model=UserOut)
async def create_user(payload: UserIn, current_user: Users = Depends(get_current_active_superuser)) -> Users:
    """
    Create new user.
    """
    user = await get_by_email(payload.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )

    user_in = await create(payload)
    return user_in


@router.get("/me", response_model=UserOut)
async def read_users_me(current_user: Users = Depends(get_current_active_user)):
    """
    Get user info.
    """
    return current_user
