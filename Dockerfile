# ---------- Stage 1: Build ----------
FROM python:3.12-slim AS build

WORKDIR /app

COPY app/requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

COPY app/ .

# ---------- Stage 2: Final runtime image ----------
FROM python:3.12-slim

WORKDIR /app

# Copy installed packages and app code from the build stage
COPY --from=build /root/.local /root/.local
COPY --from=build /app /app

ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

CMD ["python", "app.py"]
