FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000 \
    DATABASE_PATH=/app/data/repairs.db

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir --disable-pip-version-check -r requirements.txt \
    && groupadd --system appgroup \
    && useradd --system --uid 10001 --gid appgroup --home-dir /app appuser \
    && mkdir -p /app/data \
    && chown -R appuser:appgroup /app

COPY --chown=appuser:appgroup dee_cycles_api/ ./dee_cycles_api/
COPY --chown=appuser:appgroup run.py ./run.py

USER appuser
EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "from urllib.request import urlopen; urlopen('http://127.0.0.1:5000/api/health', timeout=3).read()" || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--access-logfile", "-", "--error-logfile", "-", "run:app"]
