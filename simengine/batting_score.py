from typing import Optional

class BattingScore:
	player_name = ""
	runs_scored = 0
	balls_faced = 0
	dots = 0
	not_out = True
	sixes_hit = 0
	fours_hit = 0
	method_of_dismissal = ""
	bowled_by_player_name = ""
	caught_by_player_name = ""
	stumped_by_player_name = ""
	def __init__(self, player_name):
		self.player_name = player_name
		self.runs_scored = 0
		self.balls_faced = 0
		self.not_out = True
		self.sixes_hit = 0
		self.fours_hit = 0
		self.dots = 0
		self.method_of_dismissal = ""
		self.bowled_by_player_name = ""
		self.caught_by_player_name = ""
		self.stumped_by_player_name = ""

	def dot(self):
		self.balls_faced += 1
		self.dots += 1

	def single(self):
		self.runs_scored += 1
		self.balls_faced += 1

	def two_runs(self):
		self.runs_scored += 2
		self.balls_faced += 1

	def three_runs(self):
		self.runs_scored += 3
		self.balls_faced += 1

	def four_runs(self):
		self.runs_scored += 4
		self.balls_faced += 1
		self.fours_hit += 1

	def six_runs(self):
		self.runs_scored += 6
		self.balls_faced += 1
		self.sixes_hit += 1

	def out(self, method, bowler, fielder):
		self.balls_faced += 1
		self.dots += 1
		self.not_out = False
		self.method_of_dismissal = method
		if method == "caught":
			self.caught_by_player_name = fielder.name
		if method == "stumped":
			self.stumped_by_player_name = fielder.name
		self.bowled_by_player_name = bowler.name

	def get_strike_rate(self):
		if self.balls_faced == 0:
			return 0
		return (self.runs_scored * 100)/(self.balls_faced)
