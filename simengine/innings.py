from typing import Optional
from simengine.batting_score import BattingScore
from simengine.bowling_figures import BowlingFigures
from simengine.global_helpers import overs_formatted
from simengine.player_and_team import TeamObject, PlayerObject
from simengine.locations import get_location_name, get_home_ground_code, ground_adjustments

class InningsState:
	innings_no = 1
	max_overs = 20
	overs_in_innings = 20
	batting_team = None
	fielding_team = None
	on_strike_batsman = None
	off_strike_batsman = None
	current_bowler = None
	is_free_hit = False
	is_batsman_aggression_adjusted_for_free_hit = False
	adjusted_batsman = None
	deliveries = 0
	total_runs = 0
	past_runs_scored = 0
	past_runs_conceded = 0
	extras = 0
	total_wickets = 0
	target = -1
	boosting_aggression = False
	boost_factor = 0
	easy_bowling_on = False
	fall_of_wickets = []
	has_declared = False
	def __init__(self, innings_no, max_overs, batting_team, fielding_team, opener1, opener2, target, easy_bowling_on):
		self.innings_no = innings_no
		self.max_overs = max_overs
		self.overs_in_innings = max_overs
		self.batting_team = batting_team
		self.fielding_team = fielding_team
		if (innings_no == 3 or innings_no == 4):
			self.clear_old_data()
		self.target = target
		self.current_bowler = None
		self.is_free_hit = False
		self.deliveries = 0
		self.total_runs = 0
		self.past_runs_scored = 0
		self.past_runs_conceded = 0
		self.extras = 0
		self.total_wickets = 0
		self.boosting_aggression = False
		self.boost_factor = 0
		self.is_batsman_aggression_adjusted_for_free_hit = False
		self.adjusted_batsman = None
		self.easy_bowling_on = easy_bowling_on
		self.fall_of_wickets = []
		self.has_declared = False

	def clear_old_data(self):
		self.batting_team.reset()
		self.fielding_team.reset()

	def set_openers(self, opener1, opener2):
		self.on_strike_batsman = opener1
		self.off_strike_batsman = opener2
		self.batting_team.add_to_batting_order(opener1)
		self.batting_team.add_to_batting_order(opener2)

	# Only for Test cricket
	def set_overs_in_innings(self, overs):
		self.overs_in_innings = overs

	def set_past_runs(self, runs_scored, runs_conceded):
		self.past_runs_scored = runs_scored
		self.past_runs_conceded = runs_conceded

	def max_deliveries(self):
		return (self.max_overs * 6)/5

	def swap_batsmen(self):
		temp = self.on_strike_batsman
		self.on_strike_batsman = self.off_strike_batsman
		self.off_strike_batsman = temp

	def set_opening_bowler(self, bowler):
		self.current_bowler = bowler

	def next_over(self, new_bowler):
		self.current_bowler = new_bowler
		self.swap_batsmen()

	def dot(self):
		self.deliveries += 1
		self.current_bowler.bowling_figures.dot()
		self.on_strike_batsman.batting_score.dot()

	def no_ball(self):
		self.deliveries -= 1
		self.extras += 1
		self.total_runs += 1
		self.current_bowler.bowling_figures.no_ball()
		self.is_free_hit = True

	def wide_ball(self):
		self.extras += 1
		self.total_runs += 1
		self.current_bowler.bowling_figures.wide_ball()

	def single(self):
		self.total_runs += 1
		self.deliveries += 1
		self.on_strike_batsman.batting_score.single()
		self.current_bowler.bowling_figures.single()
		self.swap_batsmen()

	def two_runs(self):
		self.total_runs += 2
		self.deliveries += 1
		self.on_strike_batsman.batting_score.two_runs()
		self.current_bowler.bowling_figures.two_runs()


	def three_runs(self):
		self.total_runs += 3
		self.deliveries += 1
		self.on_strike_batsman.batting_score.three_runs()
		self.current_bowler.bowling_figures.three_runs()
		self.swap_batsmen()

	def four_runs(self):
		self.total_runs += 4
		self.deliveries += 1
		self.on_strike_batsman.batting_score.four_runs()
		self.current_bowler.bowling_figures.four_runs()

	def six_runs(self):
		self.total_runs += 6
		self.deliveries += 1
		self.on_strike_batsman.batting_score.six_runs()
		self.current_bowler.bowling_figures.six_runs()

	def wicket(self, method, fielder):
		self.deliveries += 1
		self.total_wickets += 1
		if self.boosting_aggression:
			for i in range(self.boost_factor):
				self.on_strike_batsman.batting_aggr /= 1.025
		self.on_strike_batsman.batting_score.out(method, self.current_bowler, fielder)
		self.current_bowler.bowling_figures.wicket()
		self.fall_of_wickets.append([self.total_runs, self.total_wickets, self.on_strike_batsman.last_name, self.deliveries])

	def get_run_rate(self):
		if self.deliveries > 0:
			return self.total_runs*6/self.deliveries
		return 0

	def get_required_rate(self):
		if self.deliveries < (self.overs_in_innings * 6) and self.target > 0:
			return ((self.target - self.total_runs) * 6)/((self.overs_in_innings * 6) - self.deliveries)
		return 0

	def boost_aggression(self):
		self.on_strike_batsman.batting_aggr *= 1.025
		self.off_strike_batsman.batting_aggr *= 1.025
		self.boosting_aggression = True
		self.boost_factor += 1


	def temper_aggression(self):
		self.on_strike_batsman.batting_aggr /= 1.025
		self.off_strike_batsman.batting_aggr /= 1.025
		self.boosting_aggression = False
		self.boost_factor -= 1

	def get_eligible_batsmen(self):
		eligible_batsmen = []
		for player in self.batting_team.players:
			if player.batting_score.not_out and player.name not in [self.on_strike_batsman.name if self.on_strike_batsman else None, self.off_strike_batsman.name if self.off_strike_batsman else None]:
				eligible_batsmen.append(player)
		return eligible_batsmen

	def new_batsman_enter(self, batsman):
		self.on_strike_batsman = batsman
		self.batting_team.add_to_batting_order(batsman)
		if self.boosting_aggression:
			for i in range(self.boost_factor):
				self.on_strike_batsman.batting_aggr *= 1.025

	def can_bowl_first(self, player):
		return not player.is_wicketkeeper

	def can_bowl_next(self, player):
		if self.current_bowler.name == player.name:
			return False
		if player.bowling_figures.deliveries >= self.max_deliveries():
			return False
		return not player.is_wicketkeeper

	def get_eligible_bowlers(self):
		eligible_bowlers = []
		for player in self.fielding_team.players:
			if self.can_bowl_next(player):
				eligible_bowlers.append(player)
		return eligible_bowlers

	def get_eligible_bowlers_first_over(self):
		eligible_bowlers = []
		for player in self.fielding_team.players:
			if self.can_bowl_first(player):
				eligible_bowlers.append(player)
		return eligible_bowlers

	def declare(self):
		self.has_declared = True



class Game:
	home_team = None
	away_team = None
	game_multipliers = (1.0, 1.0, 1.0)
	first_innings = None
	second_innings = None
	third_innings = None
	fourth_innings = None
	winner = None
	location = ""
	def __init__(self, home_team, away_team):
		self.home_team = home_team
		self.away_team = away_team
		self.game_multipliers = (1.0, 1.0, 1.0)
		self.first_innings = None
		self.second_innings = None
		self.third_innings = None
		self.fourth_innings = None
		self.winner = None
		self.location = ""

	def set_location(self, location):
		self.location = location


	def chosen_team_has_better_batting(self, chosen_team):
		team1 = self.home_team
		team2 = self.away_team
		if chosen_team.name == self.away_team.name:
			team1 = self.away_team
			team2 = self.home_team
		team1_skill = 0
		team2_skill = 0
		team1_aggr = 0
		team2_aggr = 0
		team1_batsmen = list(team1.players)[:6]
		for team1_player in team1_batsmen:
			team1_skill += (team1_player.batting_skill["spin"] + team1_player.batting_skill["pace"])
			team1_aggr += team1_player.batting_aggr
		team2_batsmen = list(team2.players)[:6]
		for team2_player in team2_batsmen:
			team2_skill += (team2_player.batting_skill["spin"] + team2_player.batting_skill["pace"])
			team2_aggr += team2_player.batting_aggr
		if team2_skill - team1_skill > 6:
			return True
		elif team1_skill - team2_skill > 6:
			return False
		elif team2_aggr - team1_aggr > 8:
			return True
		return False

	def home_has_better_batting(self):
		return self.chosen_team_has_better_batting(self.home_team)

	def away_has_better_batting(self):
		return self.chosen_team_has_better_batting(self.away_team)

	def chosen_team_has_better_bowling(self, chosen_team):
		def sort_by_bowling_skill(bowler):
			return bowler.bowling_skill
		team1 = self.home_team
		team2 = self.away_team
		if chosen_team.name == self.away_team.name:
			team1 = self.away_team
			team2 = self.home_team

		team1_skill = 0
		team2_skill = 0

		team1_bowlers = sorted(team1.players, key = sort_by_bowling_skill, reverse = True)[:5]
		team2_bowlers = sorted(team2.players, key = sort_by_bowling_skill, reverse = True)[:5]

		for team1_player in team1_bowlers:
			team1_skill += team1_player.bowling_skill
		for team2_player in team2_bowlers:
			team2_skill += team2_player.bowling_skill
		if team2_skill - team1_skill > 7:
			return True
		return False

	def home_has_better_bowling(self):
		return self.chosen_team_has_better_bowling(self.away_team)

	def away_has_better_bowling(self):
		return self.chosen_team_has_better_bowling(self.home_team)

	def toss(self):
		location_name = get_location_name(self.location)
		location_string = ""
		if location_name != "":
			location_string = location_name + " for "
		print("\n\nWelcome to " + location_string + self.home_team.name + " vs " + self.away_team.name + "\n")

		_ = input("")
		_ = input("Ground multipliers for today: ")
		_ = input("Aggression: x" + str(self.game_multipliers[0]))
		_ = input("Spin: x" + str(self.game_multipliers[1]))
		_ = input("Pace: x" + str(self.game_multipliers[2]))
		_ = input("")

		print(self.home_team.captain.name + " (" + self.home_team.short_name + ") and " +\
			self.away_team.captain.name + " (" + self.away_team.short_name + ") out for the toss\n")
		toss_prompt = self.away_team.name + ", make you call (H or T): "
		if self.away_team.is_ai_team:
			print(toss_prompt, end = '')
			if (random.random() < 0.5):
				away_call = "H"
			else:
				away_call = "T"
			print(away_call)
			_ = input("")
		else:
			away_call = input(toss_prompt)
		result = ""
		if (random.random() < 0.5):
			result = "H"
		else:
			result = "T"
		if away_call == result:
			decision_prompt = self.away_team.name + " won the toss, what do you choose? (1 = Bowling, 2 = Batting): "
			decision = 1
			if self.away_team.is_ai_team:
				if (self.away_has_better_bowling()):
					decision = 1
				elif (self.away_has_better_batting()):
					decision = 2
				else:
					decision = 1
				print(decision_prompt, end = '')
				print(str(decision))
				_ = input("")
			else:
				decision = input(decision_prompt)
		else:
			decision_prompt = self.home_team.name + " won the toss, what do you choose? (1 = Batting, 2 = Bowling): "
			decision = 2
			if self.home_team.is_ai_team:
				if (self.home_has_better_bowling()):
					decision = 2
				elif (self.home_has_better_batting()):
					decision = 1
				else:
					decision = 2
				print(decision_prompt, end = '')
				print(str(decision))
				_ = input("")
			else:
				decision = input(decision_prompt)
		# print("")
		_ = input("")

		self.print_team_lineups()

		_ = input("")

		if int(decision) == 1:
			return (self.home_team, self.away_team)
		return (self.away_team, self.home_team)

	def boost_stats(self, player):
		player.batting_skill["pace"] = min(100,round(player.batting_skill["pace"] * 1.01))
		player.batting_skill["spin"] = min(100,round(player.batting_skill["spin"] * 1.01))
		player.batting_aggr = min(100,round(player.batting_aggr * 1.01))
		player.bowling_skill = min(100,round(player.bowling_skill * 1.01))
		player.fielding_skill = min(100,round(player.fielding_skill * 1.01))


	def set_ground_adjustments(self):
		if (self.location == ""):
			self.location = get_home_ground_code(self.home_team.short_name)
		((self.home_team, self.away_team), self.game_multipliers) = ground_adjustments(self.home_team, self.away_team, self.location)


	def set_home_advantage(self):
		for player in self.home_team.players:
			self.boost_stats(player)

	def set_away_advantage(self):
		for player in self.away_team.players:
			self.boost_stats(player)

	def set_first_innings(self, first_innings):
		self.first_innings = first_innings

	def set_second_innings(self, second_innings):
		self.second_innings = second_innings

	def set_third_innings(self, third_innings):
		self.third_innings = third_innings

	def set_fourth_innings(self, fourth_innings):
		self.fourth_innings = fourth_innings


