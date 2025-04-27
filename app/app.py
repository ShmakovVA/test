"""Production-ready Litestar application with advanced configuration."""

from pathlib import Path

from advanced_alchemy.extensions.litestar import (AsyncSessionConfig,
                                                  SQLAlchemyAsyncConfig,
                                                  SQLAlchemyInitPlugin)
from litestar import Litestar, get
from litestar.config.cors import CORSConfig
from litestar.di import Provide
from litestar.logging import LoggingConfig
from litestar.middleware.rate_limit import RateLimitConfig
from litestar.openapi import OpenAPIConfig
from litestar.openapi.plugins import SwaggerRenderPlugin
from litestar.static_files import StaticFilesConfig
from litestar_granian import GranianPlugin

from app.api.v1.router import user_router_v1
from app.core.config import settings
from app.core.database import provide_transaction

# Configure CORS
cors_config = CORSConfig(
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=settings.CORS_METHODS,  # type: ignore
    allow_headers=settings.CORS_HEADERS,
)

# Configure logging
logging_config = LoggingConfig(
    loggers={
        "app": {
            "level": "INFO",
            "handlers": ["queue_listener"],
        }
    }
)

openapi_config = OpenAPIConfig(
    title="My API",
    description="A simple API example",
    version="1.0.0",
    use_handler_docstrings=True,
    render_plugins=[SwaggerRenderPlugin()],
    path="/docs",
)

# Configure rate limiting
rate_limit_config = RateLimitConfig(
    rate_limit=(
        "minute",
        settings.RATE_LIMIT_PER_MINUTE,
    ),  # maximum number of requests per period
    exclude=["/health"],
)


# Configure database plugin
session_config = AsyncSessionConfig(expire_on_commit=False)
config = SQLAlchemyAsyncConfig(
    connection_string=settings.DATABASE_URL,
    create_all=True,
    session_config=session_config,
)
db_plugin = SQLAlchemyInitPlugin(config=config)

granian_plugin = GranianPlugin()


@get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}


def create_app() -> Litestar:
    """Create and configure the Litestar application."""
    return Litestar(
        route_handlers=[health_check, user_router_v1],
        middleware=[
            rate_limit_config.middleware,
        ],
        plugins=[
            granian_plugin,
            db_plugin,
        ],
        dependencies={
            "transaction": Provide(provide_transaction, sync_to_thread=False),
        },
        cors_config=cors_config,
        logging_config=logging_config,
        debug=settings.DEBUG,
        openapi_config=openapi_config,
        static_files_config=[
            StaticFilesConfig(
                directories=[Path("static")],
                path="/static",
            )
        ],
    )


app = create_app()
