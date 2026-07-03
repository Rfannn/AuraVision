import os

bind = os.getenv("AV_HOST", "0.0.0.0") + ":" + os.getenv("AV_PORT", "5000")
workers = int(os.getenv("AV_WORKERS", "1"))
worker_class = "eventlet"
timeout = 120
accesslog = "-"
errorlog = "-"
loglevel = os.getenv("AV_LOG_LEVEL", "error")
