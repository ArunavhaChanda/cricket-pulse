import random
from simengine.batting_score import BattingScore
from simengine.bowling_figures import BowlingFigures

def pick_fielder(fielding_team):
	return fielding_team.players[int(random.random() * 11)]

class PlayerObject:
	name = ""
	last_name = ""
	batting_skill = {"pace": 0.0, "spin": 0.0, "avg": 0.0}
	batting_aggr = 0.0
	bowling_skill = 0.0
	bowler_type = ""
	fielding_skill = 0.0
	is_wicketkeeper = False
	is_captain = False
	batting_score = None
	bowling_figures = None
	def __init__(self, name, batting_skill_pace, batting_skill_spin, batting_aggr, bowling_skill, fielding_skill, is_wicketkeeper, is_captain, bowler_type):
		self.name = name
		self.last_name = name.split()[-1]
		self.batting_skill = {"pace": batting_skill_pace, "spin": batting_skill_spin, "avg": (batting_skill_pace + batting_skill_spin)/2}
		self.batting_aggr = batting_aggr
		self.bowling_skill = bowling_skill
		self.fielding_skill = fielding_skill
		self.is_wicketkeeper = is_wicketkeeper
		self.is_captain = is_captain
		self.bowler_type = bowler_type
		self.batting_score = BattingScore(name)
		self.bowling_figures = BowlingFigures(name)

	def reset(self):
		self.batting_score = BattingScore(self.name)
		self.bowling_figures = BowlingFigures(self.name)		

	def is_spinner(self):
		return self.bowler_type == "spin"

	def is_pacer(self):
		return self.bowler_type == "pace"

class TeamObject:
	team_id = ""
	name = ""
	short_name = ""
	is_ai_team = False
	players = []
	final_batting_order = []
	wicketkeeper = None
	captain = None
	is_winner = False

	def __init__(self, team_id, team_name, short_name, is_ai_team, players_list):
		self.team_id = team_id
		self.name = team_name
		self.short_name = short_name
		self.is_ai_team = is_ai_team
		self.players = players_list
		self.is_winner = False
		self.final_batting_order = []
		for player in players_list:
			if player.is_wicketkeeper:
				self.wicketkeeper = player
			if player.is_captain:
				self.captain = player

	def reset(self):
		self.is_winner = False
		self.final_batting_order = []
		for player in self.players:
			player.reset()

	def add_to_batting_order(self, player):
		self.final_batting_order.append(player)