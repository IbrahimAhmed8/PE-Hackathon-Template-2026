FROM python:3.12-slim
RUN apt-get update && apt-get install -y libpq-dev gcc curl && rm -rf /var/lib/apt/lists/*
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:/root/.cargo/bin:${PATH}"
WORKDIR /app
COPY . /app/
RUN uv venv && uv sync
RUN uv add gunicorn
EXPOSE 5000
CMD ["sh", "-c", "uv run python init_db.py && uv run gunicorn --bind 0.0.0.0:5000 --workers 4 run:app"]
