# Use Python 3.10 as the base image
FROM python:3.10-slim

# Set working directory
WORKDIR /code

# --- PERMISSION FIX FOR HUGGING FACE SPACES ---
# Spaces run as a specific user (1000). We need to make sure 
# the model cache directory is writable by this user.
ENV HF_HOME=/code/.cache/huggingface
RUN mkdir -p $HF_HOME && chmod -R 777 $HF_HOME

# Install system dependencies (needed for some PDF tools)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python libraries
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port Flask runs on
EXPOSE 7860

# Command to run the app
CMD ["python", "app.py"]