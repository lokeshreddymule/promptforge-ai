# Use Python 3.11 base image
FROM python:3.11-slim

# Install Node.js
RUN apt-get update && apt-get install -y \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy Python requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy React frontend and build it
COPY forge-spark-alchemy-main/forge-spark-alchemy-main/package.json ./frontend/
COPY forge-spark-alchemy-main/forge-spark-alchemy-main/package-lock.json ./frontend/
WORKDIR /app/frontend
RUN npm install

COPY forge-spark-alchemy-main/forge-spark-alchemy-main/ ./
RUN npm run build

# Go back to app root
WORKDIR /app

# Copy all Python backend files
COPY agents/ ./agents/
COPY core/ ./core/
COPY memory/ ./memory/
COPY prompts/ ./prompts/
COPY utils/ ./utils/
COPY app.py .
COPY api_bridge.py .

# Copy built React files to be served by FastAPI
RUN cp -r /app/frontend/dist ./static

# Update api_bridge to serve static files
COPY render_server.py .

# Expose port
EXPOSE 10000

# Start the server
CMD ["python", "render_server.py"]
