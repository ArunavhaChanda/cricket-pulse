import random
from . import probability_helpers as ph
# import ai_helpers as ai
import time
from .delivery_result import DeliveryResult


# DELIVERY HELPERS

def bowl_to_bat(event_matrix):
	miss_event = -1
	miss_event_name = ""
	runs = 0
	stroke_type = -1
	stroke_name = ""
	stroke_result = ""
	# print("bowl probs: "+ str(event_matrix["bowl_probabilities"]))
	(delivery_type, delivery_name) = ph.get_delivery_type(random.random(), event_matrix["bowl_probabilities"])
	if delivery_type != 1:
		# print("stroke probs: "+str(event_matrix["stroke_probabilities"]))
		(stroke_type, stroke_name) = ph.get_stroke_type(random.random(), event_matrix["stroke_probabilities"])
		if (stroke_type == 0):
			# print("miss probs: "+str(event_matrix["miss_probabilities"]))
			(miss_event, miss_event_name) = ph.get_miss_result(random.random(), event_matrix["miss_probabilities"])
		elif (stroke_type == 1):
			stroke_result = "dot"
		else:
			(runs, stroke_result) = bat_to_field(stroke_type, event_matrix, delivery_type == 3)

	return (delivery_type, delivery_name, stroke_type, stroke_name, miss_event, miss_event_name, runs, stroke_result)

def bat_to_field(stroke_type, event_matrix, is_good_delivery):
	modifier = 0.9 if is_good_delivery else 1.0
	if (stroke_type == 2):
		# print("hit probs: "+str(event_matrix["hit_probabilities"]))
		return ph.get_hit_result(modifier * random.random(), event_matrix["hit_probabilities"], event_matrix["caught_out_probabilities"])
	elif (stroke_type == 3):
		# print("slog probs: "+str(event_matrix["slog_probabilities"]))
		return ph.get_slog_result(modifier * random.random(), event_matrix["slog_probabilities"], event_matrix["caught_out_probabilities"])

def delivery(batting_vs_pace, batting_vs_spin, batting_aggression, bowling_skill, bowling_type, wicketkeeper_fielding_skill, fielding_skill, is_free_hit, easy_bowling_on, max_overs):
	is_wicket = False
	extras = 0
	is_no_ball = False
	dismissal_type = None
	fielder_involved = None
	
	event_matrix = ph.create_event_matrix(batting_vs_pace, batting_vs_spin, batting_aggression, bowling_skill, bowling_type, wicketkeeper_fielding_skill, fielding_skill, easy_bowling_on, max_overs)
	(delivery_type, delivery_name, stroke_type, stroke_name, miss_event, miss_event_name, runs, stroke_result) = bowl_to_bat(event_matrix)

	if (delivery_type == 1):
		extras = 1
	else:
		if (delivery_type == 0):
			extras = 1
			is_no_ball = True
		if miss_event != -1:
			if miss_event == 0 and not is_no_ball and not is_free_hit:
				is_wicket = True
				dismissal_type = "bowled"
			elif miss_event == 1  and not is_no_ball and not is_free_hit:
				is_wicket = True
				dismissal_type = "lbw"
			elif miss_event == 2  and not is_no_ball and not is_free_hit:
				is_wicket = True
				if bowling_type == "spinner":
					dismissal_type = "stumped"
					fielder_involved = "wicketkeeper"
				else:
					dismissal_type = "caught behind"
					fielder_involved = "wicketkeeper"
		else:
			if (runs == 0):
				if (stroke_result == "caught") and not is_no_ball and not is_free_hit:
					is_wicket = True
					dismissal_type = "caught"
					fielder_involved = "fielder"
				elif (stroke_result == "dropped"):
					if stroke_type == 3:
						# Implement drop logic here
						fielder_involved = "fielder"
						runs = 1
					else:
						# Implement drop logic here
						fielder_involved = "fielder"
				else:
					# Simple dot
					pass

	return DeliveryResult(
		delivery_type=delivery_name,
		stroke_type=stroke_name,
		runs_scored=runs,
		extras=extras,
		is_wicket=is_wicket,
		dismissal_type=dismissal_type,
		fielder_involved=fielder_involved)



# def over(innings, should_accelerate_for_phase, should_accelerate_for_situation):
# 	if should_accelerate_for_phase:
# 		innings.boost_aggression()
# 	if should_accelerate_for_situation:
# 		innings.boost_aggression()
# 		innings.boost_aggression()
# 	starting_ball = innings.deliveries
# 	while innings.deliveries < (starting_ball + 6) and (innings.total_runs < innings.target if innings.target > 0 else True) and innings.total_wickets < 10:
# 		# time.sleep(0.5)
# 		innings = delivery(innings, False)
# 		_ = input("")
# 	if should_accelerate_for_phase:
# 		innings.temper_aggression()
# 	if should_accelerate_for_situation:
# 		innings.temper_aggression()
# 		innings.temper_aggression()
# 	return innings

# def get_first_bowler(innings):
# 	eligible_bowlers = innings.get_eligible_bowlers_first_over()
# 	innings.next_bowler_prompt(eligible_bowlers)
# 	next_bowler_index = get_bowler(innings, eligible_bowlers, False)
# 	_ = input("")
# 	innings.set_opening_bowler(eligible_bowlers[int(next_bowler_index) - 1])

# def get_next_bowler(innings):
# 	eligible_bowlers = innings.get_eligible_bowlers()
# 	innings.next_bowler_prompt(eligible_bowlers)
# 	next_bowler_index = get_bowler(innings, eligible_bowlers, False)
# 	_ = input("")
# 	if next_bowler_index == "D":
# 		innings.declare()
# 	else:
# 		innings.next_over(eligible_bowlers[int(next_bowler_index) - 1])