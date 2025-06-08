FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (only what's needed)
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create streamlit config
RUN mkdir -p ~/.streamlit/ && \
    echo "[server]\nheadless = true\nenableCORS = true\nenableXsrfProtection = true\nport = 8080\naddress = \"0.0.0.0\"\n\n[theme]\nbase = \"dark\"\nprimaryColor = \"#ff4c4c\"\nbackgroundColor = \"#0f0f0f\"\nsecondaryBackgroundColor = \"#1a1a1a\"\ntextColor = \"#ffffff\"\n" > ~/.streamlit/config.toml

# Expose port
EXPOSE 8080

# Set environment variables
ENV PORT=8080
ENV PYTHONPATH=/app

# Create optimized startup script
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
cleanup() {\n\
    pkill -f "uvicorn main:app" 2>/dev/null || true\n\
    pkill -f "streamlit run" 2>/dev/null || true\n\
    exit 0\n\
}\n\
\n\
trap cleanup SIGTERM SIGINT\n\
\n\
# Start FastAPI backend\n\
uvicorn main:app --host 0.0.0.0 --port 8000 --log-level warning &\n\
FASTAPI_PID=$!\n\
\n\
# Wait for FastAPI to be ready\n\
for i in {1..30}; do\n\
    if curl -sf http://localhost:8000/ >/dev/null 2>&1; then\n\
        break\n\
    fi\n\
    [ $i -eq 30 ] && { echo "FastAPI failed to start"; exit 1; }\n\
    sleep 2\n\
done\n\
\n\
# Start Streamlit frontend\n\
exec streamlit run app.py --server.port 8080 --server.address 0.0.0.0 --server.headless true --server.enableCORS false\n\
' > /app/start.sh && chmod +x /app/start.sh

# Run the application
CMD ["/app/start.sh"] 