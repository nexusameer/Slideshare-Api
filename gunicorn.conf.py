# Gunicorn configuration file
# See https://docs.gunicorn.org/en/stable/settings.html for all settings

# Server socket
bind = "0.0.0.0:8000"

# Worker processes
workers = 3
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50

# Timeout settings
timeout = 120
keepalive = 2

# Logging
loglevel = "info"
accesslog = "-"
errorlog = "-"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = "slideshare_api"

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Performance
preload_app = True
