import numpy as np

def overs_formatted(deliveries):
	num_overs = int(deliveries/6)
	num_balls = deliveries%6
	return str(num_overs)+ ("."+str(num_balls) if num_balls > 0 else "")

def apply_mult_to_team(team, multipliers):
	for player in team.players:
		player.batting_aggr = min(100,round(player.batting_aggr * multipliers[0]))
		bowl_mult = multipliers[1] if player.is_spinner() else multipliers[2]
		player.bowling_skill = min(100,round(player.bowling_skill * bowl_mult))
	return team

def apply_multipliers(home_team, away_team, multipliers, need_multiplier):
	if need_multiplier:
		home_team = apply_mult_to_team(home_team, multipliers)
		away_team = apply_mult_to_team(away_team, multipliers)
	return (home_team, away_team)

def clean_value(num):
	return round(num,2)

def modify_multiplier(mult_val):
	return clean_value(np.random.normal(mult_val,.05/3))

def apply_conditions(multipliers):
	new_multipliers = []
	for i in range(len(multipliers)):
		new_multipliers.append(modify_multiplier(multipliers[i]))
	return tuple(new_multipliers)
