# routes.py - Add these routes to your app.py

from flask import request, jsonify, render_template
from flask_socketio import emit
from cricket_engine import CricketGameEngine
from simengine.delivery_result import DeliveryResult
import uuid
import random

def register_api_routes(app, db, socketio):
    '''Register all API routes with the Flask app'''
    from models import db, Team, Player, Match, Innings, Delivery, BattingStats, BowlingStats

    # @app.route('/')
    # def index():
    #     return render_template('index.html')

    # @app.route('/teams')
    # def teams_page():
    #     return render_template('teams.html')

    # @app.route('/match/<match_id>')
    # def match_page(match_id):
    #     match = Match.query.filter_by(match_id=match_id).first_or_404()
    #     return render_template('match.html', match=match)

    # Team Management APIs
    @app.route('/api/teams', methods=['GET'])
    def get_teams():
        teams = Team.query.all()
        return jsonify([team.to_dict() for team in teams])

    @app.route('/api/teams', methods=['POST'])
    def create_team():
        data = request.json
        
        if not data.get('full_name') or not data.get('short_name'):
            return jsonify({'error': 'Full name and short name required'}), 400
        
        if len(data['short_name']) != 3:
            return jsonify({'error': 'Short name must be exactly 3 characters'}), 400
        
        existing_team = Team.query.filter_by(short_name=data['short_name'].upper()).first()
        if existing_team:
            return jsonify({'error': 'Team with this short name already exists'}), 400
        
        team = Team(
            full_name=data['full_name'],
            short_name=data['short_name'].upper()
        )
        
        db.session.add(team)
        db.session.commit()
        
        return jsonify(team.to_dict()), 201

    @app.route('/api/teams/<int:team_id>', methods=['DELETE'])
    def delete_team(team_id):
        team = Team.query.get_or_404(team_id)
        db.session.delete(team)
        db.session.commit()
        return jsonify({'message': 'Team deleted successfully'})

    @app.route('/api/teams/<int:team_id>/players', methods=['POST'])
    def add_player_to_team(team_id):
        team = Team.query.get_or_404(team_id)
        data = request.json
        
        if not data.get('name'):
            return jsonify({'error': 'Player name is required'}), 400
        
        if len(team.players) >= 11:
            return jsonify({'error': 'Team already has maximum 11 players'}), 400
        
        player = Player(
            name=data['name'],
            team_id=team_id,
            batting_vs_pace=data.get('batting_vs_pace', 50.0),
            batting_vs_spin=data.get('batting_vs_spin', 50.0),
            batting_aggression=data.get('batting_aggression', 50.0),
            bowling_skill=data.get('bowling_skill', 50.0),
            fielding_skill=data.get('fielding_skill', 50.0),
            is_captain=data.get('is_captain', False),
            is_wicketkeeper=data.get('is_wicketkeeper', False),
            bowling_type=data.get('bowling_type', 'pace')
        )
        
        # Ensure only one captain and wicketkeeper per team
        if player.is_captain:
            for p in team.players:
                p.is_captain = False
        
        if player.is_wicketkeeper:
            for p in team.players:
                p.is_wicketkeeper = False
        
        db.session.add(player)
        db.session.commit()
        
        return jsonify(player.to_dict()), 201

    @app.route('/api/players/<int:player_id>', methods=['PUT'])
    def update_player(player_id):
        player = Player.query.get_or_404(player_id)
        data = request.json
        
        # Update player attributes
        for field in ['name', 'batting_vs_pace', 'batting_vs_spin', 'batting_aggression', 
                      'bowling_skill', 'fielding_skill', 'bowling_type']:
            if field in data:
                setattr(player, field, data[field])
        
        # Handle special roles
        if 'is_captain' in data and data['is_captain']:
            for p in player.team.players:
                if p.id != player.id:
                    p.is_captain = False
            player.is_captain = True
        elif 'is_captain' in data:
            player.is_captain = False
        
        if 'is_wicketkeeper' in data and data['is_wicketkeeper']:
            for p in player.team.players:
                if p.id != player.id:
                    p.is_wicketkeeper = False
            player.is_wicketkeeper = True
        elif 'is_wicketkeeper' in data:
            player.is_wicketkeeper = False
        
        db.session.commit()
        return jsonify(player.to_dict())

    @app.route('/api/players/<int:player_id>', methods=['DELETE'])
    def delete_player(player_id):
        player = Player.query.get_or_404(player_id)
        db.session.delete(player)
        db.session.commit()
        return jsonify({'message': 'Player deleted successfully'})

    # Match Management APIs
    @app.route('/api/matches', methods=['POST'])
    def create_match():
        data = request.json
        
        required_fields = ['team1_id', 'team2_id', 'match_type']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        if data['team1_id'] == data['team2_id']:
            return jsonify({'error': 'Teams must be different'}), 400
        
        team1 = Team.query.get(data['team1_id'])
        team2 = Team.query.get(data['team2_id'])
        
        if not team1 or not team2:
            return jsonify({'error': 'One or both teams not found'}), 404
        
        if len(team1.players) != 11 or len(team2.players) != 11:
            return jsonify({'error': 'Both teams must have exactly 11 players'}), 400
        
        match = Match(
            team1_id=data['team1_id'],
            team2_id=data['team2_id'],
            match_type=data['match_type'],
            location=data.get('location', 'default').lower()
        )
        
        db.session.add(match)
        db.session.commit()
        
        return jsonify({
            'match_id': match.match_id,
            'match': match.to_dict()
        }), 201

    @app.route('/api/matches/<match_id>/toss', methods=['POST'])
    def conduct_toss(match_id):
        match = Match.query.filter_by(match_id=match_id).first_or_404()
        
        if match.status != 'setup':
            return jsonify({'error': 'Toss already conducted'}), 400
        
        data = request.json
        calling_team_id = data.get('calling_team_id')
        call = data.get('call')
        
        if calling_team_id not in [match.team1_id, match.team2_id]:
            return jsonify({'error': 'Invalid calling team'}), 400
        
        if call not in ['heads', 'tails']:
            return jsonify({'error': 'Call must be heads or tails'}), 400
        
        # Simulate toss
        import random
        toss_result = random.choice(['heads', 'tails'])
        toss_won = (call == toss_result)
        
        if toss_won:
            match.toss_winner_id = calling_team_id
        else:
            match.toss_winner_id = match.team2_id if calling_team_id == match.team1_id else match.team1_id
        
        match.status = 'toss'
        db.session.commit()
        
        # Emit toss result via WebSocket
        socketio.emit('toss_result', {
            'match_id': match_id,
            'toss_result': toss_result,
            'toss_winner': match.toss_winner.short_name,
            'calling_team': match.team1.short_name if calling_team_id == match.team1_id else match.team2.short_name,
            'call': call
        }, room=match_id)
        
        return jsonify({
            'toss_result': toss_result,
            'toss_winner': match.toss_winner.short_name,
            'decision_pending': True
        })

    @app.route('/api/matches/<match_id>/toss-decision', methods=['POST'])
    def make_toss_decision(match_id):
        match = Match.query.filter_by(match_id=match_id).first_or_404()
        
        if match.status != 'toss':
            return jsonify({'error': 'Toss decision not available'}), 400
        
        data = request.json
        decision = data.get('decision')
        
        if decision not in ['bat', 'bowl']:
            return jsonify({'error': 'Decision must be bat or bowl'}), 400
        
        match.toss_decision = decision
        
        if decision == 'bat':
            match.batting_first_id = match.toss_winner_id
            match.batting_second_id = match.team2_id if match.toss_winner_id == match.team1_id else match.team1_id
        else:
            match.batting_second_id = match.toss_winner_id
            match.batting_first_id = match.team2_id if match.toss_winner_id == match.team1_id else match.team1_id
        
        match.status = 'ready_to_start'
        db.session.commit()
        
        # Emit decision via WebSocket
        socketio.emit('toss_decision', {
            'match_id': match_id,
            'decision': decision,
            'batting_first': match.batting_first.short_name,
            'bowling_first': match.batting_second.short_name
        }, room=match_id)
        
        return jsonify({
            'decision': decision,
            'batting_first': match.batting_first.short_name,
            'bowling_first': match.batting_second.short_name
        })

    @app.route('/api/matches/<match_id>/start', methods=['POST'])
    def start_match(match_id):
        match = Match.query.filter_by(match_id=match_id).first_or_404()
        
        if match.status != 'ready_to_start':
            return jsonify({'error': 'Match not ready to start'}), 400
        
        # Create first innings
        innings = Innings(
            match_id=match.id,
            innings_number=1,
            batting_team_id=match.batting_first_id,
            bowling_team_id=match.batting_second_id
        )
        
        db.session.add(innings)
        match.status = 'first_innings'
        match.current_innings = 1
        
        db.session.commit()
        
        # Initialize batting and bowling stats for all players
        batting_team = match.batting_first
        bowling_team = match.batting_second
        
        for player in batting_team.players:
            stats = BattingStats(innings_id=innings.id, player_id=player.id)
            db.session.add(stats)
        
        for player in bowling_team.players:
            stats = BowlingStats(innings_id=innings.id, player_id=player.id)
            db.session.add(stats)
        
        db.session.commit()
        
        # Emit match start
        socketio.emit('match_started', {
            'match_id': match_id,
            'innings_number': 1,
            'batting_team': batting_team.short_name,
            'bowling_team': bowling_team.short_name
        }, room=match_id)
        
        return jsonify({
            'message': 'Match started',
            'innings_number': 1,
            'status': 'first_innings'
        })

    @app.route('/api/matches/<match_id>/simulate-delivery', methods=['POST'])
    def simulate_delivery(match_id):
        '''Simulate a single delivery - main integration point for your cricket logic'''
        try:
            print(f"DEBUG: Starting delivery simulation for match {match_id}")
            
            match = Match.query.filter_by(match_id=match_id).first_or_404()
            print(f"DEBUG: Found match with status: {match.status}")
            
            if match.status not in ['first_innings', 'second_innings']:
                return jsonify({'error': 'Match not in progress'}), 400
            
            data = request.json
            print(f"DEBUG: Received data: {data}")
            
            bowler_id = data.get('bowler_id')
            striker_id = data.get('striker_id')
            non_striker_id = data.get('non_striker_id')
            fielder_id = data.get('fielder_id')
            wicketkeeper_id = data.get('wicketkeeper_id')
            
            print(f"DEBUG: Player IDs - Bowler: {bowler_id}, Striker: {striker_id}, Non-striker: {non_striker_id}, Fielder: {fielder_id}, Wicketkeeper: {wicketkeeper_id}")
            
            if not all([bowler_id, striker_id, non_striker_id, fielder_id]):
                return jsonify({'error': 'Missing player IDs'}), 400
            
            # Get current innings
            current_innings = Innings.query.filter_by(
                match_id=match.id,
                innings_number=match.current_innings
            ).first()
            
            if not current_innings:
                return jsonify({'error': 'Current innings not found'}), 400
            
            print(f"DEBUG: Found innings {current_innings.id}")
            
            # Initialize cricket engine with your logic
            print("DEBUG: Initializing CricketGameEngine")
            engine = CricketGameEngine(match)
            
            # Calculate current over and ball
            total_balls = len(current_innings.deliveries)
            current_over = (total_balls // 6) + 1
            ball_in_over = (total_balls % 6) + 1
            
            print(f"DEBUG: Simulating delivery - Over: {current_over}, Ball: {ball_in_over}")
            
            # Simulate delivery using your cricket logic
            delivery_result = engine.simulate_delivery(
                bowler_id, striker_id, non_striker_id, fielder_id, wicketkeeper_id, current_over, ball_in_over
            )
            
            print(f"DEBUG: Delivery result: {delivery_result}")
            
            # Save delivery to database
            delivery = Delivery(
                innings_id=current_innings.id,
                over_number=current_over,
                ball_number=ball_in_over,
                bowler_id=bowler_id,
                striker_id=striker_id,
                non_striker_id=non_striker_id,
                delivery_type=delivery_result.delivery_type,
                stroke_type=delivery_result.stroke_type,
                runs_scored=delivery_result.runs_scored,
                extras=delivery_result.extras,
                is_wicket=delivery_result.is_wicket,
                dismissal_type=delivery_result.dismissal_type,
                total_runs_after=current_innings.total_runs + delivery_result.runs_scored + delivery_result.extras,
                wickets_after=current_innings.wickets_lost + (1 if delivery_result.is_wicket else 0)
            )
            
            db.session.add(delivery)
            
            # Update innings state
            current_innings.total_runs += delivery_result.runs_scored + delivery_result.extras
            if delivery_result.is_wicket:
                current_innings.wickets_lost += 1
            
            # Update overs completed (only count legal deliveries)
            if delivery_result.extras == 0:
                current_innings.current_over_balls += 1
                if current_innings.current_over_balls >= 6:
                    current_innings.overs_completed += 1
                    current_innings.current_over_balls = 0
            
            print("DEBUG: Committing to database")
            db.session.commit()
            
            # Emit delivery update via WebSocket
            socketio.emit('delivery_update', {
                'match_id': match_id,
                'delivery_result': delivery_result.__dict__,
                'total_runs': current_innings.total_runs,
                'wickets_lost': current_innings.wickets_lost,
                'overs_completed': current_innings.overs_completed
            }, room=match_id)
            
            print("DEBUG: Delivery simulation completed successfully")
            
            return jsonify({
                'delivery_result': delivery_result.__dict__,
                'match_state': {
                    'total_runs': current_innings.total_runs,
                    'wickets_lost': current_innings.wickets_lost,
                    'overs_completed': current_innings.overs_completed
                }
            })
            
        except Exception as e:
            print(f"ERROR in simulate_delivery: {str(e)}")
            import traceback
            traceback.print_exc()
            return jsonify({'error': f'Internal server error: {str(e)}'}), 500

    
    # Additional API endpoints for dashboard
    @app.route('/api/matches/recent', methods=['GET'])
    def get_recent_matches():
        """Get recent matches for dashboard"""
        matches = Match.query.order_by(Match.created_at.desc()).limit(10).all()
        return jsonify([{
            'match_id': match.match_id,
            'team1_name': match.team1.short_name,
            'team2_name': match.team2.short_name,
            'match_type': match.match_type,
            'location': match.location,
            'status': match.status,
            'result_text': match.result_text,
            'current_score': f"{match.team1.short_name} vs {match.team2.short_name}"
        } for match in matches])

    @app.route('/api/dashboard/stats', methods=['GET'])
    def get_dashboard_stats():
        """Get overall statistics for dashboard"""
        total_matches = Match.query.count()
        active_matches = Match.query.filter(Match.status.in_(['first_innings', 'second_innings'])).count()
        
        return jsonify({
            'total_matches': total_matches,
            'active_matches': active_matches
        })


    # # WebSocket Events for Real-time Updates
    # @socketio.on('join_match')
    # def on_join_match(data):
    #     match_id = data['match_id']
    #     join_room(match_id)
    #     emit('joined_match', {'match_id': match_id})

    # @socketio.on('leave_match')
    # def on_leave_match(data):
    #     match_id = data['match_id']
    #     leave_room(match_id)
    #     emit('left_match', {'match_id': match_id})

    # Cricket Game Logic Integration Points
    # class CricketGameEngine:
    #     """
    #     This class will integrate with your existing Python cricket logic.
    #     Replace the stub methods with calls to your actual game engine.
    #     """
        
    #     def __init__(self, match):
    #         self.match = match
    #         self.location_multipliers = LOCATION_MULTIPLIERS.get(
    #             match.location, 
    #             LOCATION_MULTIPLIERS['default']
    #         )
        
    #     def apply_location_adjustments(self, player_attributes):
    #         """Apply location-based attribute adjustments"""
    #         adjusted = player_attributes.copy()
    #         for attr, multiplier in self.location_multipliers.items():
    #             if attr in adjusted:
    #                 adjusted[attr] *= multiplier
    #         return adjusted
        
    #     def simulate_delivery(self, innings_id, bowler_id, striker_id, non_striker_id):
    #         """
    #         Simulate a single delivery - integrate your Python logic here
    #         Returns: delivery_result dict with all the outcome data
    #         """
    #         # STUB: Replace with your actual delivery simulation
    #         # This should return a dict with:
    #         # - delivery_type, stroke_type, runs_scored, extras
    #         # - is_wicket, dismissal_type, etc.
    #         pass
        
    #     def get_next_bowler_suggestions(self, innings_id):
    #         """Get list of available bowlers for next over"""
    #         # STUB: Implement bowler rotation logic
    #         pass
        
    #     def get_next_batsman_suggestions(self, innings_id):
    #         """Get list of available batsmen when wicket falls"""
    #         # STUB: Implement batting order logic
    #         pass

def _generate_mock_delivery():
    """Generate mock delivery for demo purposes"""
    rand = random.random()
    
    if rand < 0.02:
        return {'type': 'noball', 'runs': random.choice([0,1,2,4,6]), 'extras': 1, 'isWicket': False}
    elif rand < 0.04:
        return {'type': 'wide', 'runs': 0, 'extras': 1, 'isWicket': False}
    elif rand < 0.08:
        return {'type': 'wicket', 'runs': 0, 'extras': 0, 'isWicket': True}
    elif rand < 0.35:
        return {'type': 'dot', 'runs': 0, 'extras': 0, 'isWicket': False}
    elif rand < 0.50:
        return {'type': 'four', 'runs': 4, 'extras': 0, 'isWicket': False}
    elif rand < 0.55:
        return {'type': 'six', 'runs': 6, 'extras': 0, 'isWicket': False}
    else:
        return {'type': 'runs', 'runs': random.choice([1,1,1,2,2,3]), 'extras': 0, 'isWicket': False}