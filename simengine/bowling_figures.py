from typing import Optional
from simengine.global_helpers import overs_formatted

class BowlingFigures:
	player_name = ""
	deliveries = 0
	dot_balls = 0
	runs_conceded =	0
	wickets_taken = 0

	def __init__(self, player_name):
		self.player_name = player_name
		self.deliveries = 0
		self.dot_balls = 0
		self.runs_conceded = 0
		self.wickets_taken = 0
		self.economy_rate = 0.0

	def dot(self):
		self.deliveries += 1
		self.dot_balls += 1

	def no_ball(self):
		# Make sure another event is also registered
		self.deliveries -= 1
		self.runs_conceded += 1

	def wide_ball(self):
		self.runs_conceded += 1

	def single(self):
		self.runs_conceded += 1
		self.deliveries += 1

	def two_runs(self):
		self.runs_conceded += 2
		self.deliveries += 1

	def three_runs(self):
		self.runs_conceded += 3
		self.deliveries += 1

	def four_runs(self):
		self.runs_conceded += 4
		self.deliveries += 1

	def six_runs(self):
		self.runs_conceded += 6
		self.deliveries += 1

	def wicket(self):
		self.deliveries += 1
		self.wickets_taken += 1
		self.dot_balls += 1

	def get_formatted_overs(self):
		return overs_formatted(self.deliveries)

	def get_economy_rate(self):
		if self.deliveries == 0:
			return 0
		return (self.runs_conceded/self.deliveries) * 6.0
