from litestar import Router
from litestar.di import Provide

from app.api.dependencies import db_session_dependency, user_service_dependency
from app.api.v1.user import (create_user, delete_user, get_user, list_users,
                             update_user)
from app.core.config import settings

# Define the router and attach the controller methods as route handlers
user_router_v1 = Router(
    path=f"{settings.API_V1_PREFIX}/users",
    tags=["v1"],
    dependencies={
        "user_service": Provide(user_service_dependency),
        "db_session": Provide(db_session_dependency),
    },
    route_handlers=[
        list_users,
        get_user,
        create_user,
        update_user,
        delete_user,
    ],
)
