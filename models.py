from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime
import uuid
from typing import Optional
from app import db


# Database Models
class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    short_name = db.Column(db.String(3), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to players
    players = db.relationship('Player', backref='team', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'short_name': self.short_name,
            'players': [player.to_dict() for player in self.players]
        }

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    
    # Cricket attributes
    batting_vs_pace = db.Column(db.Float, nullable=False, default=50.0)
    batting_vs_spin = db.Column(db.Float, nullable=False, default=50.0)
    batting_aggression = db.Column(db.Float, nullable=False, default=50.0)
    bowling_skill = db.Column(db.Float, nullable=False, default=50.0)
    fielding_skill = db.Column(db.Float, nullable=False, default=50.0)
    
    # Special roles
    is_captain = db.Column(db.Boolean, default=False)
    is_wicketkeeper = db.Column(db.Boolean, default=False)
    bowling_type = db.Column(db.String(10), default='pace')  # 'pace' or 'spin'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'batting_vs_pace': self.batting_vs_pace,
            'batting_vs_spin': self.batting_vs_spin,
            'batting_aggression': self.batting_aggression,
            'bowling_skill': self.bowling_skill,
            'fielding_skill': self.fielding_skill,
            'is_captain': self.is_captain,
            'is_wicketkeeper': self.is_wicketkeeper,
            'bowling_type': self.bowling_type
        }

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.String(36), unique=True, default=lambda: str(uuid.uuid4()))
    
    # Teams
    team1_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    team2_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    
    # Match details
    match_type = db.Column(db.String(10), nullable=False)  # 'T20', 'ODI', 'Test'
    location = db.Column(db.String(100))
    
    # Game state
    status = db.Column(db.String(20), default='setup')  # 'setup', 'toss', 'first_innings', 'second_innings', 'super_over', 'completed'
    current_innings = db.Column(db.Integer, default=1)
    
    # Toss
    toss_winner_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    toss_decision = db.Column(db.String(10))  # 'bat' or 'bowl'
    
    # Batting order
    batting_first_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    batting_second_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    
    # Match result
    winner_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    result_text = db.Column(db.String(200))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    team1 = db.relationship('Team', foreign_keys=[team1_id])
    team2 = db.relationship('Team', foreign_keys=[team2_id])
    toss_winner = db.relationship('Team', foreign_keys=[toss_winner_id])
    batting_first = db.relationship('Team', foreign_keys=[batting_first_id])
    batting_second = db.relationship('Team', foreign_keys=[batting_second_id])
    winner = db.relationship('Team', foreign_keys=[winner_id])
    
    # Match data
    innings = db.relationship('Innings', backref='match', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'match_id': self.match_id,
            'team1': self.team1.to_dict() if self.team1 else None,
            'team2': self.team2.to_dict() if self.team2 else None,
            'match_type': self.match_type,
            'location': self.location,
            'status': self.status,
            'current_innings': self.current_innings,
            'toss_winner': self.toss_winner.short_name if self.toss_winner else None,
            'toss_decision': self.toss_decision,
            'winner': self.winner.short_name if self.winner else None,
            'result_text': self.result_text
        }

class Innings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('match.id'), nullable=False)
    innings_number = db.Column(db.Integer, nullable=False)  # 1, 2, or 3 (super over)
    batting_team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    bowling_team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    
    # Innings state
    total_runs = db.Column(db.Integer, default=0)
    wickets_lost = db.Column(db.Integer, default=0)
    overs_completed = db.Column(db.Float, default=0.0)
    current_over_balls = db.Column(db.Integer, default=0)
    
    # Current players
    striker_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    non_striker_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    current_bowler_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    
    # Innings complete
    is_completed = db.Column(db.Boolean, default=False)
    
    # Relationships
    batting_team = db.relationship('Team', foreign_keys=[batting_team_id])
    bowling_team = db.relationship('Team', foreign_keys=[bowling_team_id])
    striker = db.relationship('Player', foreign_keys=[striker_id])
    non_striker = db.relationship('Player', foreign_keys=[non_striker_id])
    current_bowler = db.relationship('Player', foreign_keys=[current_bowler_id])
    
    # Delivery data
    deliveries = db.relationship('Delivery', backref='innings', lazy=True, cascade='all, delete-orphan')
    batting_stats = db.relationship('BattingStats', backref='innings', lazy=True, cascade='all, delete-orphan')
    bowling_stats = db.relationship('BowlingStats', backref='innings', lazy=True, cascade='all, delete-orphan')

class Delivery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    innings_id = db.Column(db.Integer, db.ForeignKey('innings.id'), nullable=False)
    over_number = db.Column(db.Integer, nullable=False)
    ball_number = db.Column(db.Integer, nullable=False)  # 1-6, can be more with extras
    
    # Players involved
    bowler_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    striker_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    non_striker_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    
    # Delivery outcome
    delivery_type = db.Column(db.String(20))  # 'no_ball', 'wide', 'fair', 'good'
    stroke_type = db.Column(db.String(20))   # 'miss', 'dot', 'hit', 'slog'
    runs_scored = db.Column(db.Integer, default=0)
    extras = db.Column(db.Integer, default=0)
    
    # Dismissal
    is_wicket = db.Column(db.Boolean, default=False)
    dismissal_type = db.Column(db.String(20))  # 'bowled', 'lbw', 'caught', 'stumped', etc.
    dismissed_player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    fielder_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    
    # State after delivery
    total_runs_after = db.Column(db.Integer)
    wickets_after = db.Column(db.Integer)
    
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class BattingStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    innings_id = db.Column(db.Integer, db.ForeignKey('innings.id'), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    
    runs_scored = db.Column(db.Integer, default=0)
    balls_faced = db.Column(db.Integer, default=0)
    fours = db.Column(db.Integer, default=0)
    sixes = db.Column(db.Integer, default=0)
    is_out = db.Column(db.Boolean, default=False)
    dismissal_type = db.Column(db.String(20))
    
    # Relationships
    player = db.relationship('Player')

class BowlingStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    innings_id = db.Column(db.Integer, db.ForeignKey('innings.id'), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    
    overs_bowled = db.Column(db.Float, default=0.0)
    runs_conceded = db.Column(db.Integer, default=0)
    wickets_taken = db.Column(db.Integer, default=0)
    maidens = db.Column(db.Integer, default=0)
    
    # Relationships
    player = db.relationship('Player')