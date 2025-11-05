# cricket_engine.py - Integration point for your existing Python logic
import random
import json
from turtle import home
from simengine.delivery_result import DeliveryResult
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from simengine.batting_score import BattingScore
from simengine.bowling_figures import BowlingFigures
from simengine.player_and_team import TeamObject, PlayerObject
from simengine.innings import InningsState, Game

EASY_BOWLING_ON = False

class CricketGameEngine:
    '''
    Integration wrapper for Python cricket simulation logic.
    '''
    
    def __init__(self, match):
        from models import Match  # Match is the database model
        self.match = match
        self.max_overs = 20 if self.match.match_type == 'T20' else 50

        home_team = self._build_team(match.team1)
        away_team = self._build_team(match.team2)

        self.game = Game(home_team, away_team)        
        
        self.location_multipliers = self.apply_location_adjustments(match.location)

        # Weather and pitch conditions (can change during match)
        self.pitch_condition = 'normal'  # normal, dry, wet, deteriorating
        self.weather_condition = 'clear'  # clear, overcast, rainy
        self.light_condition = 'good'    # good, poor, floodlit
        
        self.current_delivery_result = None
        self.current_innings = 1
        self.current_over = 0
        self.current_ball = 0
        self.total_runs = 0
        self.wickets_lost = 0
        self.balls_faced = 0
        self.partnership_runs = 0
        self.consecutive_dots = 0
        self.consecutive_boundaries = 0
        
        print(f"Initialized CricketGameEngine for match {match.match_id}")
    
    def _build_team(self, team) -> TeamObject:
        '''Build a TeamObject from a Team database model'''
        # team is a Team (database model), converting to TeamObject (simulation object)

        players_list = []
        for player in team.players:
            players_list.append(PlayerObject(player.id, player.name, player.batting_vs_pace, player.batting_vs_spin, player.batting_aggression, player.bowling_skill, player.fielding_skill, player.is_wicketkeeper, player.is_captain, player.bowling_type))

        return TeamObject(team.id, team.full_name, team.short_name, False, players_list)
        
    def apply_location_adjustments(self, location: str) -> Dict[str, float]:
        '''Get location-based attribute multipliers'''
        from simengine.locations import get_location_short_code
        self.game.set_location(get_location_short_code(location))
        self.game.set_ground_adjustments()

    def start_first_innings(self, batting_first_id, batting_second_id):
        batting_team = self.game.home_team if batting_first_id == self.game.home_team.team_id else self.game.away_team
        bowling_team = self.game.away_team if batting_first_id == self.game.home_team.team_id else self.game.home_team
        first_innings = InningsState(1, self.max_overs, batting_team, bowling_team, self.game.home_team.players[0], self.game.home_team.players[1], 0, EASY_BOWLING_ON)
        self.game.set_first_innings(first_innings)

    def start_second_innings(self):
        second_innings = InningsState(2, self.max_overs, self.game.first_innings.fielding_team, self.game.first_innings.batting_team, self.game.home_team.players[0], self.game.home_team.players[1], self.game.first_innings.total_runs + 1, EASY_BOWLING_ON)
        self.game.set_second_innings(second_innings)

    
    def get_match_state(self) -> Dict[str, Any]:
        """Get current match state for debugging/monitoring"""
        return {
            'current_innings': self.current_innings,
            'current_over': self.current_over,
            'current_ball': self.current_ball,
            'total_runs': self.total_runs,
            'wickets_lost': self.wickets_lost,
            'balls_faced': self.balls_faced,
            'partnership_runs': self.partnership_runs,
            'consecutive_dots': self.consecutive_dots,
            'consecutive_boundaries': self.consecutive_boundaries,
            'pitch_condition': self.pitch_condition,
            'weather_condition': self.weather_condition
        }
    
    def update_match_state(self, delivery_result: DeliveryResult):
        """Update persistent state after a delivery"""
        if delivery_result.is_wicket:
            self.wickets_lost += 1
            self.partnership_runs = 0
        else:
            self.partnership_runs += delivery_result.runs_scored
            
        if delivery_result.extras == 0:  # Only count legal deliveries
            self.balls_faced += 1
            
        self.total_runs += delivery_result.runs_scored + delivery_result.extras
        
        # Update ball count
        if delivery_result.extras == 0:
            self.current_ball += 1
            if self.current_ball > 6:
                self.current_ball = 1
                self.current_over += 1
                
        # Track consecutive deliveries for momentum
        if delivery_result.runs_scored == 0:
            self.consecutive_dots += 1
        else:
            self.consecutive_dots = 0
            
        if delivery_result.runs_scored >= 4:
            self.consecutive_boundaries += 1
        else:
            self.consecutive_boundaries = 0

        # Innings state update
        if self.wickets_lost == 10 or self.balls_faced == self.max_overs * 6:
            self.current_innings = 2
            self.current_over = 0
            self.current_ball = 0
            self.total_runs = 0
            self.wickets_lost = 0
            self.balls_faced = 0
            self.partnership_runs = 0
            self.consecutive_dots = 0
            self.consecutive_boundaries = 0

        self.current_delivery_result = delivery_result
        
        
    
    def set_players(self, striker_id: int, non_striker_id: int, bowler_id: int):
        """Set current players (called when players change)"""
        from models import Player
        self.current_striker = Player.query.get(striker_id)
        self.current_non_striker = Player.query.get(non_striker_id)
        self.current_bowler = Player.query.get(bowler_id)
        
        # Reset partnership when new batsmen come in
        self.partnership_runs = 0
    
    def _fetch_player(self, player_id: int) -> PlayerObject:
        return self.game.home_team.players_map[player_id] if player_id in self.game.home_team.players_map else self.game.away_team.players_map[player_id]
        
    def simulate_delivery(self, bowler_id: int, striker_id: int, non_striker_id: int, fielder_id: int,
                         wicketkeeper_id: int,
                         current_over: int, ball_in_over: int) -> DeliveryResult:
        '''
        Simulate a single delivery using your existing Python logic.
        
        INTEGRATION POINT: Replace this method with a call to your actual 
        cricket simulation engine.
        
        Args:
            bowler_id: ID of the bowling player
            striker_id: ID of the striking batsman
            non_striker_id: ID of the non-striking batsman
            current_over: Current over number
            ball_in_over: Ball number in current over (1-6+)
            
        Returns:
            DeliveryResult with all the outcome data
        '''
        
        # STUB IMPLEMENTATION - Replace with your actual logic
        # Get player objects from database
        # from models import Player
        # bowler = Player.query.get(bowler_id)
        # striker = Player.query.get(striker_id)
        # non_striker = Player.query.get(non_striker_id)
        # fielder = Player.query.get(fielder_id)
        # wicketkeeper = Player.query.get(wicketkeeper_id)
        
        # Apply location adjustments
        bowler = self._fetch_player(bowler_id)
        striker = self._fetch_player(bowler_id)
        non_striker = self._fetch_player(non_striker_id)
        fielder = self._fetch_player(fielder_id)
        wicketkeeper = self._fetch_player(wicketkeeper_id)

        bowler_attrs = {
            'bowling_skill': bowler.bowling_skill,
            'bowling_type': bowler.bowler_type
        }
        
        striker_attrs = {
            'batting_vs_pace': striker.batting_skill["pace"],
            'batting_vs_spin': striker.batting_skill["spin"],
            'batting_aggression': striker.batting_aggr
        }

        fielder_attrs = {
            'fielding_skill': fielder.fielding_skill
        }

        wicketkeeper_attrs = {
            'fielding_skill': wicketkeeper.fielding_skill
        }


        # bowler_attrs = self.apply_location_adjustments({
        #     'bowling_skill': bowler.bowling_skill,
        #     'bowling_type': bowler.bowling_type
        # })
        
        # striker_attrs = self.apply_location_adjustments({
        #     'batting_vs_pace': striker.batting_vs_pace,
        #     'batting_vs_spin': striker.batting_vs_spin,
        #     'batting_aggression': striker.batting_aggression
        # })

        # fielder_attrs = self.apply_location_adjustments({
        #     'fielding_skill': fielder.fielding_skill
        # })

        # wicketkeeper_attrs = self.apply_location_adjustments({
        #     'fielding_skill': wicketkeeper.fielding_skill
        # })

        # Update persistent state
        self.current_over = current_over
        self.current_ball = ball_in_over
        self.current_bowler = bowler
        self.current_striker = striker
        self.current_non_striker = non_striker
        

        # Add free hit adjustments

        
        #
        # 	if is_free_hit and not is_no_ball and (delivery_type != 1): # not a wide
		# is_free_hit = False
        is_free_hit = False
        


        # Import events only when needed to avoid circular import issues
        import simengine.events as events
        delivery = events.delivery(striker_attrs['batting_vs_pace'], striker_attrs['batting_vs_spin'], striker_attrs['batting_aggression'], bowler_attrs['bowling_skill'], bowler_attrs['bowling_type'], wicketkeeper_attrs['fielding_skill'], fielder_attrs['fielding_skill'], is_free_hit, EASY_BOWLING_ON, self.max_overs)
        self.update_match_state(delivery)
        return delivery

        
        # For now, return a random outcome for demonstration
        # return self._generate_mock_delivery()
    
    # def _generate_mock_delivery(self) -> DeliveryResult:
    #     '''Generate a mock delivery for demonstration purposes'''
    #     # Probability-based outcome generation
    #     rand = random.random()
        
    #     if rand < 0.02:  # 2% chance of no ball
    #         return DeliveryResult(
    #             delivery_type='no_ball',
    #             stroke_type='hit',
    #             runs_scored=random.choice([0, 1, 2, 4, 6]),
    #             extras=1,
    #             is_wicket=False
    #         )
    #     elif rand < 0.04:  # 2% chance of wide
    #         return DeliveryResult(
    #             delivery_type='wide',
    #             stroke_type='miss',
    #             runs_scored=0,
    #             extras=1,
    #             is_wicket=False
    #         )
    #     elif rand < 0.08:  # 4% chance of wicket
    #         return DeliveryResult(
    #             delivery_type='fair',
    #             stroke_type='miss',
    #             runs_scored=0,
    #             extras=0,
    #             is_wicket=True,
    #             dismissal_type=random.choice(['bowled', 'lbw', 'caught', 'stumped'])
    #         )
    #     elif rand < 0.35:  # 27% chance of dot ball
    #         return DeliveryResult(
    #             delivery_type='fair',
    #             stroke_type='dot',
    #             runs_scored=0,
    #             extras=0,
    #             is_wicket=False
    #         )
    #     elif rand < 0.50:  # 15% chance of 4
    #         return DeliveryResult(
    #             delivery_type='fair',
    #             stroke_type='hit',
    #             runs_scored=4,
    #             extras=0,
    #             is_wicket=False
    #         )
    #     elif rand < 0.55:  # 5% chance of 6
    #         return DeliveryResult(
    #             delivery_type='fair',
    #             stroke_type='slog',
    #             runs_scored=6,
    #             extras=0,
    #             is_wicket=False
    #         )
    #     else:  # Remaining chance for 1, 2, or 3 runs
    #         return DeliveryResult(
    #             delivery_type='fair',
    #             stroke_type='hit',
    #             runs_scored=random.choice([1, 1, 1, 2, 2, 3]),  # Weighted toward singles
    #             extras=0,
    #             is_wicket=False
    #         )
    
    def get_available_bowlers(self, innings_id: int, current_bowler_id: int = None) -> List[Dict]:
        '''Get list of bowlers available for the next over'''
        from models import Innings, Player, BowlingStats
        
        innings = Innings.query.get(innings_id)
        if not innings:
            return []
        
        # Get bowling team players
        bowling_team_players = innings.bowling_team.players
        
        # Get max overs per bowler based on match type
        max_overs_for_bowler = self.max_overs // 5
        
        available_bowlers = []
        for player in bowling_team_players:
            # Skip current bowler (can't bowl consecutive overs)
            if current_bowler_id and player.id == current_bowler_id:
                continue
                
            # Get bowling stats for this innings
            bowling_stats = BowlingStats.query.filter_by(
                innings_id=innings_id,
                player_id=player.id
            ).first()
            
            overs_bowled = bowling_stats.overs_bowled if bowling_stats else 0
            
            # Check if player can bowl more overs
            if overs_bowled < max_overs_for_bowler:
                available_bowlers.append({
                    'id': player.id,
                    'name': player.name,
                    'bowling_type': player.bowling_type,
                    'bowling_skill': player.bowling_skill,
                    'overs_bowled': overs_bowled,
                    'overs_remaining': max_overs_for_bowler - overs_bowled
                })
        
        # Sort by bowling skill (best bowlers first)
        available_bowlers.sort(key=lambda x: x['bowling_skill'], reverse=True)
        return available_bowlers
    
    def get_available_batsmen(self, innings_id: int) -> List[Dict]:
        '''Get list of batsmen available when a wicket falls'''
        from models import Innings, Player, BattingStats
        
        innings = Innings.query.get(innings_id)
        if not innings:
            return []
        
        batting_team_players = innings.batting_team.players
        
        # Get batsmen who haven't batted yet or are not out
        available_batsmen = []
        for player in batting_team_players:
            batting_stats = BattingStats.query.filter_by(
                innings_id=innings_id,
                player_id=player.id
            ).first()
            
            # If no stats record, player hasn't batted
            # If stats exist but player is not out, they're available
            if not batting_stats or not batting_stats.is_out:
                # Skip if player is currently batting
                if player.id in [innings.striker_id, innings.non_striker_id]:
                    continue
                    
                available_batsmen.append({
                    'id': player.id,
                    'name': player.name,
                    'batting_avg_pace': player.batting_vs_pace,
                    'batting_avg_spin': player.batting_vs_spin,
                    'is_captain': player.is_captain,
                    'is_wicketkeeper': player.is_wicketkeeper
                })
        
        return available_batsmen
    
    def calculate_required_run_rate(self, target: int, current_score: int, 
                                  overs_remaining: float) -> float:
        '''Calculate required run rate for chasing team'''
        runs_needed = target - current_score
        if overs_remaining <= 0:
            return 0.0
        return runs_needed / overs_remaining
    
    def is_innings_complete(self, innings_id: int) -> Tuple[bool, str]:
        '''Check if innings should end and return reason'''
        from models import Innings, BattingStats
        
        innings = Innings.query.get(innings_id)
        if not innings:
            return True, "Invalid innings"
        
        # Check if all overs completed
        if innings.overs_completed >= self.max_overs:
            return True, "Overs completed"
        
        # Check if 10 wickets fallen
        if innings.wickets_lost >= 10:
            return True, "All out"
        
        # For second innings, check if target achieved
        if innings.innings_number == 2:
            # Get first innings total (would need to implement this)
            # For now, return False
            pass
        
        return False, ""