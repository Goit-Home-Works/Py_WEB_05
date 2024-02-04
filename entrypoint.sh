#!/bin/sh

# Run the server in the background
python server.py &

# Run the web server
python -m http.server 8000
