from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from src.app.db.models import Base

from src.app.core.config import settings  # Import Settings from config.py

# this is the Alembic Config object, which provides access to the values within the .ini file
config = context.config


# Set the sqlalchemy.url using the DATABASE_URL from your settings
config.set_main_option('sqlalchemy.url', settings.DATABASE_URL)

# Your existing target_metadata (if any)
# from myapp import models
# target_metadata = models.Base.metadata

target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    section = config.get_section(config.config_ini_section)
    assert section is not None, "Alembic configuration section is missing."

    connectable = engine_from_config(
        section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()