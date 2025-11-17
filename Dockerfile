
FROM python:3.11-slim AS base

# Prevent Python from writing .pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DEFAULT_TIMEOUT=1000

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ curl libffi-dev \
    && rm -rf /var/lib/apt/lists/*


# Install dependencies

COPY requirements.txt .

# 1️⃣ Upgrade pip
RUN pip install --upgrade pip

# 2️⃣ Install lightweight CPU version of torch (optional but faster)
RUN pip install torch==2.3.0+cpu --extra-index-url https://download.pytorch.org/whl/cpu

# 3️⃣ Install project dependencies
RUN pip install -r requirements.txt


COPY rag_project ./rag_project


EXPOSE 8000
CMD ["uvicorn", "rag_project.api.server:app", "--host", "0.0.0.0", "--port", "8000"]
