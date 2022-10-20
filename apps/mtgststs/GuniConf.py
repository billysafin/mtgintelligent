import multiprocessing

# Server Socket
bind = 'unix:/var/shared/nginx/gunicorn_my_app.sock'
backlog = 2048

# Worker Processes
#workers = multiprocessing.cpu_count() * 2 + 1
workers = 1
worker_class = 'sync'
worker_connections = 1
max_requests = 0
timeout = 120
keepalive = 2
debug = False
spew = False

# Logging
logfile = '/var/www/log/app.log'
loglevel = 'info'
logconfig = None

# Process Name
proc_name = 'gunicorn_my_app'
