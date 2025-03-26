"""Gunicorn config for the Flask application."""
import multiprocessing
import os

# Get the PORT environment variable that Render provides
port = os.environ.get("PORT", "10000")

# Bind to 0.0.0.0:PORT
bind = f"0.0.0.0:{port}"

# Use one worker per core
workers = multiprocessing.cpu_count()

# Set timeout to 120 seconds for image processing
timeout = 120

# Use gevent worker for async processing
worker_class = "gevent"

# Access log format
accesslog = "-"

# Error log
errorlog = "-"

# Log level
loglevel = "info" 