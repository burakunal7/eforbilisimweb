import sys
import os

# Add the project directory to the Python path
INTERP = os.path.expanduser("/home/YOUR_USERNAME/venv/bin/python")
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

# Import the Flask app
from app import app as application

# For debugging
if __name__ == '__main__':
    application.run() 