# Use Python 3.11-slim base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /workspaces

# Install system dependencies, including git
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Clone the Git repository each time the container is started
CMD ["sh", "-c", "git clone https://github.com/AliAlabed1/Wal_Mart_ETL.git && \
    cd Wal_Mart_ETL && \
    pip install -r requierments.txt && \
    uvicorn src.api.main:APP --host 0.0.0.0 --port 8000 --reload"]
