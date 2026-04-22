ARG BUILD_FROM
FROM $BUILD_FROM

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

COPY pyproject.toml .
RUN uv sync --no-dev

# Install Playwright's Chromium and its OS dependencies
RUN uv run playwright install-deps chromium \
    && uv run playwright install chromium

COPY server.py .

CMD ["uv", "run", "python", "server.py"]
