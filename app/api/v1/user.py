"""User API endpoints."""

from advanced_alchemy.exceptions import DuplicateKeyError, NotFoundError
from litestar import Response, delete, get, post, put, status_codes

from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.user import UserService
from app.utils.security import get_password_hash


@get()
async def list_users(
    user_service: UserService,
) -> list[UserResponse] | Response:
    """
    List all users .
    """
    try:
        users = await user_service.list_users()
    except Exception:
        return Response(
            status_code=status_codes.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Internal Error"},
        )

    return Response(
        status_code=status_codes.HTTP_200_OK,
        content=users,
        headers={"X-Total-Count": str(len(users))},
    )


@post()
async def create_user(
    user_service: UserService,
    data: UserCreate,
) -> UserResponse | Response:
    """
    Create a new user.
    """
    user = UserCreate(
        name=data.name,
        sername=data.sername,
        password=get_password_hash(data.password),
    )

    try:
        new_user = await user_service.create_user(user)
    except DuplicateKeyError:
        return Response(
            status_code=status_codes.HTTP_400_BAD_REQUEST,
            content={"message": "User already exists"},
        )
    except Exception:
        return Response(
            status_code=status_codes.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Internal Error"},
        )

    return Response(status_code=status_codes.HTTP_201_CREATED, content=new_user)


@get("/{user_id:int}")
async def get_user(
    user_service: UserService,
    user_id: int,
) -> UserResponse | Response:
    """
    Get user details.
    """
    try:
        user = await user_service.get_user(user_id)
    except NotFoundError:
        return Response(
            status_code=status_codes.HTTP_404_NOT_FOUND,
            content={"message": "User not found"},
        )
    except Exception as e:
        return Response(
            status_code=status_codes.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": str(type(e))},
        )

    return Response(status_code=status_codes.HTTP_200_OK, content=user)


@put("/{user_id:int}")
async def update_user(
    user_service: UserService,
    user_id: int,
    data: UserUpdate,
) -> UserResponse | Response:
    """
    Update user details.
    """
    update_dict = {k: v for k, v in data.to_dict().items() if v is not None}
    if "password" in update_dict:
        update_dict["password"] = get_password_hash(update_dict.pop("password"))

    user_update = UserUpdate(**update_dict)

    try:
        updated_user = await user_service.update_user(
            user_id=user_id, user_data=user_update
        )
    except NotFoundError:
        return Response(
            status_code=status_codes.HTTP_404_NOT_FOUND,
            content={"message": "User not found"},
        )
    except DuplicateKeyError:
        return Response(
            status_code=status_codes.HTTP_400_BAD_REQUEST,
            content={"message": "User already exists"},
        )
    except Exception:
        return Response(
            status_code=status_codes.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Internal Error"},
        )

    return Response(status_code=status_codes.HTTP_200_OK, content=updated_user)


@delete("/{user_id:int}")
async def delete_user(
    user_service: UserService,
    user_id: int,
) -> None:
    """
    Delete user.
    """
    try:
        await user_service.delete_user(user_id)
    except NotFoundError:
        return Response(  # type: ignore
            status_code=status_codes.HTTP_404_NOT_FOUND,
            content={"message": "User not found"},
        )
    except Exception:
        return Response(  # type: ignore
            status_code=status_codes.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Internal Error"},
        )

    return None
