import os
import sys

# Ensure backend root is in sys.path so 'config' and 'store' can be imported
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(CURRENT_DIR)
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

from config.wsgi import application

# Vercel Serverless Function entry point
app = application

