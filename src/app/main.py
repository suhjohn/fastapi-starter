from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.router import router
from .core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Lifespan context manager for FastAPI application.
    Handles startup and shutdown events.
    """
    # Startup
    print("Starting up...")
    # Add any async startup code here, like:
    # - Database connections
    # - Cache initialization
    # - Background tasks

    yield  # App is running

    # Shutdown
    print("Shutting down...")
    # Add any async cleanup code here, like:
    # - Closing database connections
    # - Cleaning up background tasks


def create_application() -> FastAPI:
    """
    Create and configure the FastAPI application.
    """
    app = FastAPI(
        docs_url=None,  # Disable default docs
        redoc_url=None,  # Disable default redoc
        lifespan=lifespan,
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register routers
    app.include_router(
        router,
    )

    return app


app = create_application()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        port=settings.PORT,
        log_level=settings.LOG_LEVEL,
        reload=True,
    )
