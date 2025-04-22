# Use a minimal Python runtime
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# 1. Copy & install only the API dependencies
COPY requirements-api.txt .
RUN pip install --no-cache-dir -r requirements-api.txt

# 2. Copy your application code and the trained models
COPY src/    src/
COPY models/ models/

# 3. Expose the port FastAPI will run on
EXPOSE 8000

# 4. Start the server
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
