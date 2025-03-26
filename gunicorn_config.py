"""Gunicorn config for the Flask application."""
import multiprocessing

# Bind to 0.0.0.0:$PORT
bind = "0.0.0.0:$PORT"

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