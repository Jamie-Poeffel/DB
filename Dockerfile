# Use official Python image
FROM python:3.11

# Set working directory
WORKDIR /app

# Copy application files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# # Expose port (optional, if running a web service)
# EXPOSE 5000

RUN bash