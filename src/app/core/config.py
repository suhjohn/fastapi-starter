from typing import List
from urllib.parse import parse_qs, urlparse

from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ALLOWED_ORIGINS: list[str] = ["*"]
    PORT: int = 8000
    LOG_LEVEL: str = "info"
    DATABASE_URL: str

    @property
    def ASYNC_DATABASE_URL(self) -> str:
        """
        Derives the async database URL from the sync database URL.

        Handles different formats:
        - postgresql:// -> postgresql+asyncpg://
        - postgres:// -> postgresql+asyncpg://

        Preserves all query parameters and handles URL encoding.
        """
        parsed = urlparse(self.DATABASE_URL)

        # Validate scheme
        if parsed.scheme not in ("postgresql", "postgres"):
            raise ValueError(
                "DATABASE_URL must start with 'postgresql://' or 'postgres://'"
            )

        # Build the base of the async URL
        async_url = f"postgresql+asyncpg://{parsed.netloc}{parsed.path}"

        # If there are query parameters, preserve them
        if parsed.query:
            # Parse existing query parameters
            query_params = parse_qs(parsed.query)

            # Convert query parameters to async-compatible versions if needed
            # For example, 'sslmode=require' in psycopg2 becomes 'ssl=true' in asyncpg
            asyncpg_params: List[str] = []

            for key, values in query_params.items():
                # Handle special cases for parameter conversion
                if key == "sslmode" and "require" in values:
                    asyncpg_params.append("ssl=true")
                elif key == "target_session_attrs" and "read-write" in values:
                    asyncpg_params.append("target_session_attrs=read-write")
                # Add other parameter conversions as needed
                else:
                    # For all other parameters, keep them as-is
                    for value in values:
                        asyncpg_params.append(f"{key}={value}")

            # Add the converted query parameters to the URL
            if asyncpg_params:
                async_url = f"{async_url}?{'&'.join(asyncpg_params)}"

        return async_url

    @field_validator("DATABASE_URL")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        """Validates the database URL format."""
        parsed = urlparse(v)
        if parsed.scheme not in ("postgresql", "postgres"):
            raise ValueError(
                "DATABASE_URL must start with 'postgresql://' or 'postgres://'"
            )
        if not parsed.netloc:
            raise ValueError("DATABASE_URL must contain a host")
        return v

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()  # type: ignore
