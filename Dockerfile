# Use a slim Python base image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

# Set working directory
WORKDIR /app

# Install system dependencies (including ADB client for android commands)
RUN apt-get update && apt-get install -y --no-install-recommends \
    android-tools-adb \
    && rm -rf /var/lib/apt/lists/*

# Copy configuration files for installing dependencies
COPY pyproject.toml uv.lock ./

# Install project dependencies using uv (cache dependencies)
RUN uv sync --frozen --no-install-project

# Copy the actual source code
COPY src/ ./src/

# Install the project itself
RUN uv sync --frozen

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH"

# Command to run the MCP server using stdio transport
ENTRYPOINT ["uv", "run", "python", "src/sbtumcp/main.py"]
