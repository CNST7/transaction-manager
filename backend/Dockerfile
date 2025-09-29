FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get clean && \
    apt-get install -y --no-install-recommends curl

# Install uv
# https://docs.astral.sh/uv/guides/integration/docker/#intermediate-layers
COPY --from=ghcr.io/astral-sh/uv:0.8.22 /uv /uvx /bin/

# Place project virtual environment binary directory at the front of the path
# https://docs.astral.sh/uv/guides/integration/docker/#using-the-environment
ENV PATH="/backend/.venv/bin:$PATH"

# Silence warnings
# https://docs.astral.sh/uv/guides/integration/docker/#caching
ENV UV_LINK_MODE=copy

# Create non-root user
RUN useradd -m -u 1000 backend

# Change working directory
WORKDIR /backend

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

# Copy project files
COPY --chown=backend:backend . .

# Sync the project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

# Move scripts to transactionManager directory
# and remove directory
RUN mv scripts/* ./transactionManager && \
    rmdir scripts

# Change working directory to transactionManager
WORKDIR /backend/transactionManager

# Create technical directories
# and update theirs ownership to non-root user
RUN mkdir -p logs static media
RUN chown -R backend:backend logs static media

# Change windows file endings to unix-like
# and remove script file
RUN ./replace_windows_line_endings.py && \
    rm replace_windows_line_endings.py

# Switch to non-root user
USER backend

# Run entrypoint script
CMD ["./entrypoint.sh"]
