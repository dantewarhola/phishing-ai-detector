
# Use an official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose ports for FastAPI and Streamlit
EXPOSE 8000
EXPOSE 8501

# Start both backend and frontend using a shell script
CMD ["bash", "-c", "uvicorn src.api:app --host 0.0.0.0 --port 8000 & streamlit run ui/app.py --server.port 8501"]
