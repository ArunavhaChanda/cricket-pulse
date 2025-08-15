#!/usr/bin/env python3
"""
Cricket Simulator - Modular Flask Application
Works with separate config.py, models.py, and routes.py files
"""

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit, join_room, leave_room
import os

# Initialize extensions (without app context)
db = SQLAlchemy()
socketio = SocketIO()

def create_app(config_name=None):
    """Application factory function"""
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG', 'default')
    
    app = Flask(__name__)
    
    # Import and apply configuration
    try:
        from config import config
        app.config.from_object(config[config_name])
        print(f"✅ Configuration loaded: {config_name}")
    except ImportError as e:
        print(f"⚠️  Could not import config.py: {e}")
        print("Using default configuration...")
        # Fallback configuration
        app.config['SECRET_KEY'] = 'cricket-simulator-secret-key'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cricket_simulator.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions with app
    db.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")
    
    # Import models and create tables
    try:
        import models
        print("✅ Models imported successfully")
        
        with app.app_context():
            db.create_all()
            print("✅ Database tables created")
            
    except ImportError as e:
        print(f"❌ Could not import models.py: {e}")
        print("Please ensure models.py exists in the same directory")
        raise
    
    # Register basic page routes
    register_page_routes(app)
    
    # Register API routes from separate routes.py file
    try:
        from routes import register_api_routes
        register_api_routes(app, db, socketio)
        print("✅ API routes registered from routes.py")
    except ImportError as e:
        print(f"⚠️  Could not import routes.py: {e}")
        print("API routes will not be available")
    except Exception as e:
        print(f"⚠️  Error registering routes: {e}")
    
    # Register WebSocket events
    register_socketio_events()
    
    return app

def register_page_routes(app):
    """Register basic page routes (not API routes)"""
    
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/teams')
    def teams_page():
        return render_template('teams.html')

    @app.route('/match/<match_id>')
    def match_page(match_id):
        try:
            from models import Match
            match = Match.query.filter_by(match_id=match_id).first_or_404()
            return render_template('match.html', match=match)
        except ImportError:
            return "Error: Could not load match data", 500

def register_socketio_events():
    """Register WebSocket event handlers"""
    
    @socketio.on('join_match')
    def on_join_match(data):
        match_id = data['match_id']
        join_room(match_id)
        emit('joined_match', {'match_id': match_id})
        print(f"Client joined match room: {match_id}")

    @socketio.on('leave_match')
    def on_leave_match(data):
        match_id = data['match_id']
        leave_room(match_id)
        emit('left_match', {'match_id': match_id})
        print(f"Client left match room: {match_id}")

    @socketio.on('connect')
    def on_connect():
        print('Client connected to WebSocket')

    @socketio.on('disconnect')
    def on_disconnect():
        print('Client disconnected from WebSocket')

def run_app():
    """Run the application"""
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

if __name__ == '__main__':
    run_app()
    
    
    

    
    
    
# # app.py
# from flask import Flask, render_template, request, jsonify, session
# from flask_sqlalchemy import SQLAlchemy
# from flask_socketio import SocketIO, emit, join_room, leave_room
# import os
# from config import Config
# import json
# from datetime import datetime
# import uuid


# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'your-secret-key-here'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cricket_simulator.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)
# socketio = SocketIO(app, cors_allowed_origins="*")

# # app = Flask(__name__)
# # app.config.from_object(Config)

# # db = SQLAlchemy(app)
# # socketio = SocketIO(app, cors_allowed_origins="*")

# # Location-based attribute multipliers
# LOCATION_MULTIPLIERS = {
#     'mumbai': {
#         'batting_vs_pace': 1.1,
#         'batting_vs_spin': 0.9,
#         'bowling_skill': 1.0,
#         'fielding_skill': 1.0
#     },
#     'chennai': {
#         'batting_vs_pace': 0.9,
#         'batting_vs_spin': 1.1,
#         'bowling_skill': 1.0,
#         'fielding_skill': 1.0
#     },
#     'delhi': {
#         'batting_vs_pace': 1.0,
#         'batting_vs_spin': 1.0,
#         'bowling_skill': 1.1,
#         'fielding_skill': 1.0
#     },
#     'default': {
#         'batting_vs_pace': 1.0,
#         'batting_vs_spin': 1.0,
#         'bowling_skill': 1.0,
#         'fielding_skill': 1.0
#     }
# }

# # Match type configurations
# MATCH_CONFIGS = {
#     'T20': {'overs': 20, 'max_bowler_overs': 4},
#     'ODI': {'overs': 50, 'max_bowler_overs': 10},
#     'Test': {'overs': 450, 'max_bowler_overs': 90}  # Theoretical max
# }


# def create_app(config_name=None):
#     if config_name is None:
#         config_name = os.environ.get('FLASK_CONFIG', 'default')
    
#     app = Flask(__name__)
#     app.config.from_object(Config[config_name])
    
#     # Initialize extensions with app
#     db.init_app(app)
#     socketio.init_app(app, cors_allowed_origins="*")
    
#     # Import models after db initialization
#     from models import Team, Player, Match, Innings, Delivery, BattingStats, BowlingStats
    
#     # Create database tables
#     with app.app_context():
#         db.create_all()
    
#     # Register routes
#     register_routes(app)
#     register_socketio_events(socketio)
    
#     return app

# def register_routes(app):
#     '''Register all Flask routes'''
    
#     @app.route('/')
#     def index():
#         return render_template('index.html')

#     @app.route('/teams')
#     def teams_page():
#         return render_template('teams.html')

#     @app.route('/match/<match_id>')
#     def match_page(match_id):
#         from models import Match
#         match = Match.query.filter_by(match_id=match_id).first_or_404()
#         return render_template('match.html', match=match)

#     # Import and register API routes
#     from routes import register_api_routes
#     register_api_routes(app)

# def register_socketio_events(socketio):
#     '''Register WebSocket event handlers'''
    
#     @socketio.on('join_match')
#     def on_join_match(data):
#         match_id = data['match_id']
#         join_room(match_id)
#         emit('joined_match', {'match_id': match_id})

#     @socketio.on('leave_match')
#     def on_leave_match(data):
#         match_id = data['match_id']
#         leave_room(match_id)
#         emit('left_match', {'match_id': match_id})


# # if __name__ == '__main__':
# #     app = create_app()
# #     with app.app_context():
# #         db.create_all()
# #     socketio.run(app, debug=True, host='0.0.0.0', port=5000)

# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()
#     socketio.run(app, debug=True, host='0.0.0.0', port=5000)