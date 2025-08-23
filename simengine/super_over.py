from simengine.global_helpers import overs_formatted
from simengine.batting_score import BattingScore
from simengine.bowling_figures import BowlingFigures

class SuperOverInnings:
	innings_no = 1
	batting_team = None
	fielding_team = None
	on_strike_batsman = None
	off_strike_batsman = None
	third_batsman = None
	current_bowler = None
	is_free_hit = False
	is_batsman_aggression_adjusted_for_free_hit = False
	adjusted_batsman = None
	deliveries = 0
	total_runs = 0
	total_wickets = 0
	target = -1
	boosting_aggression = False
	easy_bowling_on = False
	boost_factor = 0
	max_overs = 1
	def __init__(self, innings_no, batting_team, fielding_team, target, easy_bowling_on):
		self.innings_no = innings_no
		self.batting_team = batting_team
		self.fielding_team = fielding_team
		self.on_strike_batsman = None
		self.off_strike_batsman = None
		self.current_bowler = None
		self.is_free_hit = False
		self.is_batsman_aggression_adjusted_for_free_hit = False
		self.adjusted_batsman = None
		self.deliveries = 0
		self.total_runs = 0
		self.total_wickets = 0
		self.target = target
		self.boosting_aggression = False
		self.easy_bowling_on = easy_bowling_on
		self.boost_factor = 0
		self.max_overs = 1

	def set_batsmen(self, opener1, opener2, third_batsman):
		self.on_strike_batsman = opener1
		self.off_strike_batsman = opener2
		self.third_batsman = third_batsman

	def set_bowler(self, bowler):
		self.current_bowler = bowler

	def get_eligible_batsmen(self):
		eligible_batsmen = []
		for player in self.batting_team.players:
			eligible_batsmen.append(player)
		return eligible_batsmen

	def next_batsman_prompt(self, eligible_batsmen):
		for batting_index in range(len(eligible_batsmen)):
			print (str(batting_index + 1) + " " + eligible_batsmen[batting_index].get_batting_prompt())

	def new_batsman_enter(self, batsman):
		self.on_strike_batsman = batsman
		if self.boosting_aggression:
			for i in range(self.boost_factor):
				self.on_strike_batsman.batting_aggr *= 1.2

	def can_bowl(self, player):
		return not player.is_wicketkeeper

	def get_eligible_bowlers(self):
		eligible_bowlers = []
		for player in self.fielding_team.players:
			if self.can_bowl(player):
				eligible_bowlers.append(player)
		return eligible_bowlers

	def bowler_prompt(self, eligible_bowlers):
		for bowling_index in range(len(eligible_bowlers)):
			print (str(bowling_index + 1) + " " + eligible_bowlers[bowling_index].get_bowling_prompt())


	def swap_batsmen(self):
		temp = self.on_strike_batsman
		self.on_strike_batsman = self.off_strike_batsman
		self.off_strike_batsman = temp

	def next_batsman(self):
		self.new_batsman_enter(self.third_batsman)

	def dot(self):
		self.deliveries += 1

	def no_ball(self):
		self.deliveries -= 1
		self.total_runs += 1
		self.is_free_hit = True

	def wide_ball(self):
		self.total_runs += 1

	def single(self):
		self.total_runs += 1
		self.deliveries += 1
		self.swap_batsmen()

	def two_runs(self):
		self.total_runs += 2
		self.deliveries += 1

	def three_runs(self):
		self.total_runs += 3
		self.deliveries += 1
		self.swap_batsmen()

	def four_runs(self):
		self.total_runs += 4
		self.deliveries += 1

	def six_runs(self):
		self.total_runs += 6
		self.deliveries += 1

	def wicket(self, method, fielder):
		self.deliveries += 1
		self.total_wickets += 1
		if self.boosting_aggression:
			for i in range(self.boost_factor):
				self.on_strike_batsman.batting_aggr /= 1.2


	def boost_aggression(self):
		self.on_strike_batsman.batting_aggr *= 1.2
		self.off_strike_batsman.batting_aggr *= 1.2
		self.boosting_aggression = True
		self.boost_factor += 1

	def temper_aggression(self):
		self.on_strike_batsman.batting_aggr /= 1.2
		self.off_strike_batsman.batting_aggr /= 1.2
		self.boosting_aggression = False
		self.boost_factor -= 1


	def formatted_overs(self):
		return overs_formatted(self.deliveries)

	def formatted_score(self):
		return self.batting_team.short_name+": "+str(self.total_runs)+"/"+str(self.total_wickets)

	def formatted_chase_status(self):
		if (self.deliveries < 6):
			if self.innings_no == 2 and self.total_runs < self.target:
				return self.batting_team.short_name + " need " +\
				 str(self.target - self.total_runs) + " to win from " +\
				 str(6 - self.deliveries)
		return ""

	def get_batting_scorecard(self):
		print("\n" + self.batting_team.name + "\nTOTAL: " + str(self.total_runs) + "/" +str(self.total_wickets) + " (" + str(self.formatted_overs()) + ")")
		if self.innings_no == 1:
			print("\n" + self.fielding_team.name + " need " + str(self.total_runs + 1) + " to win from 6 deliveries")
		print("\n\n")


class SuperOver:
	first_team = None
	second_team = None
	first_team_over = None
	second_team_over = None
	easy_bowling_on = False
	def __init__(self, first_team, second_team, easy_bowling_on):
		self.first_team = first_team
		self.second_team = second_team
		self.first_team_over = None
		self.second_team_over = None
		self.easy_bowling_on = easy_bowling_on

	def set_first_over(self):
		self.first_team_over = SuperOverInnings(1, self.first_team, self.second_team, -1, self.easy_bowling_on)
		return self.first_team_over

	def set_second_over(self):
		self.second_team_over = SuperOverInnings(2, self.second_team, self.first_team, self.first_team_over.total_runs + 1, self.easy_bowling_on)
		return self.second_team_over
