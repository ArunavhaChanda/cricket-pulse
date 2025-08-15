# cricket_engine.py - Integration point for your existing Python logic
import random
import json
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass

@dataclass
class DeliveryResult:
    delivery_type: str  # 'no_ball', 'wide', 'fair', 'good'
    stroke_type: str    # 'miss', 'dot', 'hit', 'slog'
    runs_scored: int
    extras: int
    is_wicket: bool
    dismissal_type: Optional[str] = None
    fielder_involved: Optional[int] = None

class CricketGameEngine:
    '''
    Integration wrapper for your existing Python cricket simulation logic.
    Replace the methods below with calls to your actual game engine.
    '''
    
    def __init__(self, match):
        self.match = match
        self.location_multipliers = self._get_location_multipliers(match.location)
        
    def _get_location_multipliers(self, location: str) -> Dict[str, float]:
        '''Get location-based attribute multipliers'''
        multipliers = {
            'mumbai': {
                'batting_vs_pace': 1.1,
                'batting_vs_spin': 0.9,
                'bowling_skill': 1.0,
                'fielding_skill': 1.0
            },
            'chennai': {
                'batting_vs_pace': 0.9,
                'batting_vs_spin': 1.1,
                'bowling_skill': 1.0,
                'fielding_skill': 1.0
            },
            'delhi': {
                'batting_vs_pace': 1.0,
                'batting_vs_spin': 1.0,
                'bowling_skill': 1.1,
                'fielding_skill': 1.0
            },
            'default': {
                'batting_vs_pace': 1.0,
                'batting_vs_spin': 1.0,
                'bowling_skill': 1.0,
                'fielding_skill': 1.0
            }
        }
        return multipliers.get(location, multipliers['default'])
    
    def apply_location_adjustments(self, player_attributes: Dict[str, float]) -> Dict[str, float]:
        '''Apply location-based adjustments to player attributes'''
        adjusted = player_attributes.copy()
        for attr, multiplier in self.location_multipliers.items():
            if attr in adjusted:
                adjusted[attr] *= multiplier
        return adjusted
    
    def simulate_delivery(self, bowler_id: int, striker_id: int, non_striker_id: int, 
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
        from models import Player
        bowler = Player.query.get(bowler_id)
        striker = Player.query.get(striker_id)
        non_striker = Player.query.get(non_striker_id)
        
        # Apply location adjustments
        bowler_attrs = self.apply_location_adjustments({
            'bowling_skill': bowler.bowling_skill,
            'bowling_type': bowler.bowling_type
        })
        
        striker_attrs = self.apply_location_adjustments({
            'batting_vs_pace': striker.batting_vs_pace,
            'batting_vs_spin': striker.batting_vs_spin,
            'batting_aggression': striker.batting_aggression
        })
        
        # PLACEHOLDER: Your probability matrices and simulation logic would go here
        # This is where you'd call your existing Python cricket simulation
        
        # For now, return a random outcome for demonstration
        return self._generate_mock_delivery()
    
    def _generate_mock_delivery(self) -> DeliveryResult:
        '''Generate a mock delivery for demonstration purposes'''
        # Probability-based outcome generation
        rand = random.random()
        
        if rand < 0.02:  # 2% chance of no ball
            return DeliveryResult(
                delivery_type='no_ball',
                stroke_type='hit',
                runs_scored=random.choice([0, 1, 2, 4, 6]),
                extras=1,
                is_wicket=False
            )
        elif rand < 0.04:  # 2% chance of wide
            return DeliveryResult(
                delivery_type='wide',
                stroke_type='miss',
                runs_scored=0,
                extras=1,
                is_wicket=False
            )
        elif rand < 0.08:  # 4% chance of wicket
            return DeliveryResult(
                delivery_type='fair',
                stroke_type='miss',
                runs_scored=0,
                extras=0,
                is_wicket=True,
                dismissal_type=random.choice(['bowled', 'lbw', 'caught', 'stumped'])
            )
        elif rand < 0.35:  # 27% chance of dot ball
            return DeliveryResult(
                delivery_type='fair',
                stroke_type='dot',
                runs_scored=0,
                extras=0,
                is_wicket=False
            )
        elif rand < 0.50:  # 15% chance of 4
            return DeliveryResult(
                delivery_type='fair',
                stroke_type='hit',
                runs_scored=4,
                extras=0,
                is_wicket=False
            )
        elif rand < 0.55:  # 5% chance of 6
            return DeliveryResult(
                delivery_type='fair',
                stroke_type='slog',
                runs_scored=6,
                extras=0,
                is_wicket=False
            )
        else:  # Remaining chance for 1, 2, or 3 runs
            return DeliveryResult(
                delivery_type='fair',
                stroke_type='hit',
                runs_scored=random.choice([1, 1, 1, 2, 2, 3]),  # Weighted toward singles
                extras=0,
                is_wicket=False
            )
    
    def get_available_bowlers(self, innings_id: int, current_bowler_id: int = None) -> List[Dict]:
        '''Get list of bowlers available for the next over'''
        from models import Innings, Player, BowlingStats
        
        innings = Innings.query.get(innings_id)
        if not innings:
            return []
        
        # Get bowling team players
        bowling_team_players = innings.bowling_team.players
        
        # Get max overs per bowler based on match type
        max_overs = 4 if self.match.match_type == 'T20' else 10
        
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
            if overs_bowled < max_overs:
                available_bowlers.append({
                    'id': player.id,
                    'name': player.name,
                    'bowling_type': player.bowling_type,
                    'bowling_skill': player.bowling_skill,
                    'overs_bowled': overs_bowled,
                    'overs_remaining': max_overs - overs_bowled
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
        max_overs = 20 if self.match.match_type == 'T20' else 50
        if innings.overs_completed >= max_overs:
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