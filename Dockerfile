FROM python:3.11-slim

WORKDIR /app

# Copy only requirements first for cache efficiency
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy app source code
COPY src/api/ .

# Copy model files
COPY models/trained/*.pkl models/trained/

# Expose port 8000
EXPOSE 8000

# Run the app with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
