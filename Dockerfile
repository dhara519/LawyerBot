# Use an official lightweight Python image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy only requirements first (to leverage Docker caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire FastAPI app to the container
COPY . .

# Expose the application port (matching FastAPI's default port)
EXPOSE 8000

# Run FastAPI using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
