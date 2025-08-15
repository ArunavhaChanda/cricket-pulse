#!/usr/bin/env python3
"""
Cricket Simulator - Flask Application
Run this file to start the cricket simulator web application.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, socketio

if __name__ == '__main__':
    app = create_app()
    print("\n🏏 Cricket Simulator Starting...")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("⚡ Press Ctrl+C to stop the server\n")
    
    try:
        socketio.run(app, 
                    debug=True, 
                    host='0.0.0.0', 
                    port=5000,
                    allow_unsafe_werkzeug=True)
    except KeyboardInterrupt:
        print("\n👋 Cricket Simulator stopped. Thanks for playing!")
