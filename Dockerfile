FROM python:3.13-slim
LABEL authors="Victor Martin"

RUN groupadd -r appgroup && useradd -r -g appgroup -d /app -s /sbin/nologin -c "App user" appuser

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appgroup src/ ./src/

USER appuser

EXPOSE 8000

CMD ["fastapi", "run", "src/main.py", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]