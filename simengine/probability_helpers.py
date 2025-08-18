import random
from . import base_event_matrices as bem

def batting_skill_vs_bowler(batting_vs_pace, batting_vs_spin, bowling_type):
	if bowling_type == "spin":
		return batting_vs_spin
	elif bowling_type == "pace":
		return batting_vs_pace
	else:
		return batting_vs_pace

def flatten_probs(probability_list):
	total = sum(probability_list)
	new_probability_list = []
	for num in probability_list:
		new_probability_list.append(num/total)
	return new_probability_list

def adjust_bowl_probs(bowl_probabilities, easy_bowling_on, bowling_skill):
	original_bowling_skill = bowling_skill
	if (easy_bowling_on):
		bowling_skill *= 1.25
	bowl_probabilities[2] = bowl_probabilities[2] * (bowling_skill / 70.0)
	if (bowling_skill >= 70):
		bowl_probabilities[3] = bowl_probabilities[3] * (1.0 + ((bowling_skill - 70.0) * 2.0 / 100.0))
	else:
		bowl_probabilities[3] = bowl_probabilities[3] * ((bowling_skill / 2.0) / 70.0)
	if (easy_bowling_on):
		bowling_skill = original_bowling_skill
	return flatten_probs(bowl_probabilities)

def adjust_stroke_probs(stroke_probabilities, batting_vs_pace, batting_vs_spin, batting_aggression, bowling_skill, bowling_type):
	batting_skill = batting_skill_vs_bowler(batting_vs_pace, batting_vs_spin, bowling_type)

	#SKILL PART
	stroke_probabilities[0] = stroke_probabilities[0] * (1.5 * bowling_skill / batting_skill)
	stroke_probabilities[1] = stroke_probabilities[1] * (1.5 * bowling_skill / batting_skill)

	#AGGRESSION PART

	if (bowling_skill >= 80 and bowling_skill < 90):
		stroke_probabilities[0] = stroke_probabilities[0] * (1.2 + ((bowling_skill - 80.0) / 30.0))
		stroke_probabilities[1] = stroke_probabilities[1] * (1.2 + ((bowling_skill - 80.0) / 30.0))
	elif (bowling_skill >= 90):
		stroke_probabilities[0] = stroke_probabilities[0] * (1.54 + ((bowling_skill - 90.0) / 20.0))
		stroke_probabilities[1] = stroke_probabilities[1] * (1.54 + ((bowling_skill - 90.0) / 20.0))


	if (batting_skill >= 73 and batting_skill < 80):
		stroke_probabilities[0] = stroke_probabilities[0] * (1.0 - ((batting_skill - 70.0) / 33.0))
		stroke_probabilities[1] = stroke_probabilities[1] * (1.0 - ((batting_skill - 70.0) / 33.0))
	elif (batting_skill >= 80 and batting_skill < 90):
		stroke_probabilities[0] = stroke_probabilities[0] * (0.72 - ((batting_skill - 80.0) / 80.0))
		stroke_probabilities[1] = stroke_probabilities[1] * (0.72 - ((batting_skill - 80.0) / 80.0))
	elif (batting_skill >= 90):
		stroke_probabilities[0] = stroke_probabilities[0] * (0.6 - ((batting_skill - 90.0) / 50.0))
		stroke_probabilities[1] = stroke_probabilities[1] * (0.6 - ((batting_skill - 90.0) / 50.0))

	if (batting_aggression < 50):
		stroke_probabilities[3] = stroke_probabilities[3] * (1.0 - ((50 - batting_aggression) / 100.0))
	elif (batting_aggression < 70):
		# stroke_probabilities[0] = stroke_probabilities[3] + (((batting_aggression - 50.0) / 100.0))
		stroke_probabilities[3] = stroke_probabilities[3] + (((batting_aggression - 50.0) / 100.0))
	elif (batting_aggression < 80):
		# stroke_probabilities[0] = stroke_probabilities[3] + (((batting_aggression - 50.0) / 100.0))
		stroke_probabilities[3] = stroke_probabilities[3] + (((batting_aggression - 50.0) / 70.0))
	elif (batting_aggression < 90):
		stroke_probabilities[3] = stroke_probabilities[3] + 0.5 + ((batting_aggression - 80.0) / 20.0)
		# stroke_probabilities[3] = stroke_probabilities[3] + (((batting_aggression - 40.0) / 100.0))
	else:
		stroke_probabilities[3] = stroke_probabilities[3] + 0.5 + ((batting_aggression - 90.0) / 1.5)

	return flatten_probs(stroke_probabilities)

def adjust_miss_probs(miss_probabilities, easy_bowling_on, bowling_skill, wicketkeeper_fielding_skill):
	original_bowling_skill = bowling_skill
	if (easy_bowling_on):
		bowling_skill *= 1.25
	if (not easy_bowling_on):
		if (bowling_skill < 50):
			miss_probabilities[0] = miss_probabilities[0] * (1.0 - ((50 - bowling_skill) / 100.0))
			miss_probabilities[1] = miss_probabilities[1] * (1.0 - ((50 - bowling_skill) / 100.0))
		elif (bowling_skill < 65):
			miss_probabilities[0] = miss_probabilities[0] + (((bowling_skill - 50.0) / 200.0))
			miss_probabilities[1] = miss_probabilities[1] * (1.0 - ((50 - bowling_skill) / 100.0))
	if ((easy_bowling_on  or bowling_skill >= 65) and bowling_skill < 80):
		miss_probabilities[0] = miss_probabilities[0] + (((bowling_skill - 50.0) / 130.0))
		miss_probabilities[1] = miss_probabilities[1] * (1.0 - ((50 - bowling_skill) / 100.0))
	elif (bowling_skill < 90):
		miss_probabilities[0] = miss_probabilities[0] + (((bowling_skill - 72.0) / 27.0))
		miss_probabilities[1] = miss_probabilities[1] * (1.0 - ((50 - bowling_skill) / 100.0))
	elif (bowling_skill >= 90):
		miss_probabilities[0] = miss_probabilities[0] + 0.21 + ((bowling_skill - 87.0) / 7.0)
		miss_probabilities[1] = miss_probabilities[1] * (1.0 - ((50 - bowling_skill) / 100.0))

	if (wicketkeeper_fielding_skill > 70):
		miss_probabilities[2] = miss_probabilities[2] * (wicketkeeper_fielding_skill - 65.0) / 5.0

	if (easy_bowling_on):
		bowling_skill = original_bowling_skill
	return flatten_probs(miss_probabilities)

def batting_skill_with_mult(batting_skill, easy_bowling_on):
	batting_mult = 1.0	
	if (batting_skill >= 90):
		batting_mult = 1.23
		# batting_mult = 1.2
	elif (batting_skill >= 85):
		batting_mult = 1.2
		# batting_mult = 1.15
	elif (batting_skill >= 80):
		batting_mult = 1.1
		# batting_mult = 1.07
	elif (batting_skill <= 68 and not easy_bowling_on):
		batting_mult = 0.9
		# batting_mult = 1.07
	return batting_skill * batting_mult

def adjust_hit_probs(hit_probabilities, easy_bowling_on, batting_vs_pace, batting_vs_spin, batting_aggression, bowling_skill, bowling_type, fielding_skill):
	batting_skill = batting_skill_vs_bowler(batting_vs_pace, batting_vs_spin, bowling_type)
	batting_adjust = batting_skill_with_mult(batting_skill, easy_bowling_on)
	if (bowling_skill > 83):
		hit_probabilities[0] = hit_probabilities[0] * (1.0 + ((bowling_skill - 80)/100))
	hit_probabilities[0] = hit_probabilities[0] * (bowling_skill * .7)
	hit_probabilities[1] = hit_probabilities[1] * 70
	hit_probabilities[2] = hit_probabilities[2] * batting_adjust
	hit_probabilities[3] = hit_probabilities[3] * batting_adjust
	hit_probabilities[4] = hit_probabilities[4] * (batting_adjust * 1.2) * (1.0 if bowling_skill > 75 else (1 + ((75-bowling_skill)/100)))
	hit_probabilities[5] = hit_probabilities[5] * batting_adjust * ((100.0 + batting_aggression) / 180.0)  * (1.0 if bowling_skill > 75 else (1 + ((75-bowling_skill)/100)))

	hit_probabilities[0] = hit_probabilities[0] * fielding_skill
	hit_probabilities[1] = hit_probabilities[1] * (fielding_skill * 0.8)
	hit_probabilities[2] = hit_probabilities[2] * 60
	hit_probabilities[3] = hit_probabilities[3] * (30 + (100 - fielding_skill))
	hit_probabilities[4] = hit_probabilities[4] * (50 + (100 - fielding_skill))
	hit_probabilities[5] = hit_probabilities[5] * (50 + (100 - fielding_skill))

	return flatten_probs(hit_probabilities)

def adjust_slog_probs(slog_probabilities, easy_bowling_on, batting_vs_pace, batting_vs_spin, batting_aggression, bowling_skill, bowling_type, fielding_skill):
	batting_skill = batting_skill_vs_bowler(batting_vs_pace, batting_vs_spin, bowling_type)
	batting_adjust = batting_skill_with_mult(batting_skill, easy_bowling_on)
	if (bowling_skill > 83):
		slog_probabilities[0] = slog_probabilities[0] * (1.0 + ((bowling_skill - 80)/100))
	slog_probabilities[0] = slog_probabilities[0] * (bowling_skill * .6)
	slog_probabilities[1] = slog_probabilities[1] * 70
	slog_probabilities[2] = slog_probabilities[2] * batting_adjust
	slog_probabilities[3] = slog_probabilities[3] * batting_adjust
	slog_probabilities[4] = slog_probabilities[4] * (batting_adjust * 1.2) * (1.0 if bowling_skill > 75 else (1 + ((75-bowling_skill)/100)))
	slog_probabilities[5] = slog_probabilities[5] * batting_adjust * ((100.0 + batting_aggression) / 170.0) * (1.0 if bowling_skill > 75 else (1 + ((75-bowling_skill)/100)))
	if (batting_aggression >= 87):
		temp = slog_probabilities[4]
		slog_probabilities[4] = slog_probabilities[5]
		slog_probabilities[5] = temp


	slog_probabilities[0] = slog_probabilities[0] * fielding_skill
	slog_probabilities[1] = slog_probabilities[1] * (fielding_skill * 0.8)
	slog_probabilities[2] = slog_probabilities[2] * 60
	slog_probabilities[3] = slog_probabilities[3] * (30 + (100 - fielding_skill))
	slog_probabilities[4] = slog_probabilities[4] * (50 + (100 - fielding_skill))
	slog_probabilities[5] = slog_probabilities[5] * (50 + (100 - fielding_skill))

	return flatten_probs(slog_probabilities)

def adjust_caught_probs(caught_out_probabilities, batting_vs_pace, batting_vs_spin, bowling_skill, bowling_type, fielding_skill):
	batting_skill = batting_skill_vs_bowler(batting_vs_pace, batting_vs_spin, bowling_type)
	bowler_factor = 1.0
	if (bowling_skill < 65):
		bowler_factor = bowling_skill / 70
	elif (bowling_skill > 83):
		bowler_factor = 1 + ((bowling_skill - 80) / 100)

	caught_out_probabilities[0] = caught_out_probabilities[0] * (fielding_skill/batting_skill) * bowler_factor
	caught_out_probabilities[1] = caught_out_probabilities[1] * (fielding_skill/batting_skill) * bowler_factor

	return caught_out_probabilities

def adjust_matrix(probability_matrix, batting_vs_pace, batting_vs_spin, batting_aggression, bowling_skill, bowling_type, wicketkeeper_fielding_skill, fielding_skill):
	probability_matrix["bowl_probabilities"] = adjust_bowl_probs(probability_matrix["bowl_probabilities"], probability_matrix["easy_bowling_on"], bowling_skill)
	probability_matrix["stroke_probabilities"] = adjust_stroke_probs(probability_matrix["stroke_probabilities"], batting_vs_pace, batting_vs_spin, batting_aggression, bowling_skill, bowling_type)
	probability_matrix["miss_probabilities"] = adjust_miss_probs(probability_matrix["miss_probabilities"], probability_matrix["easy_bowling_on"], bowling_skill, wicketkeeper_fielding_skill)
	probability_matrix["hit_probabilities"] = adjust_hit_probs(probability_matrix["hit_probabilities"], probability_matrix["easy_bowling_on"], batting_vs_pace, batting_vs_spin, batting_aggression, bowling_skill, bowling_type, fielding_skill)
	probability_matrix["slog_probabilities"] = adjust_slog_probs(probability_matrix["slog_probabilities"], probability_matrix["easy_bowling_on"], batting_vs_pace, batting_vs_spin, batting_aggression, bowling_skill, bowling_type, fielding_skill)
	probability_matrix["caught_out_probabilities"] = adjust_caught_probs(probability_matrix["caught_out_probabilities"], batting_vs_pace, batting_vs_spin, bowling_skill, bowling_type, fielding_skill)

	return probability_matrix

def create_event_matrix(batting_vs_pace, batting_vs_spin, batting_aggression, bowling_skill, bowling_type, wicketkeeper_fielding_skill, fielding_skill, easy_bowling_on, max_overs):
	probability_matrix = bem.base_event_matrix_t20(easy_bowling_on)
	if (max_overs == 50):
		probability_matrix = bem.base_event_matrix_odi(easy_bowling_on)
	elif (max_overs > 50):
		probability_matrix = bem.base_event_matrix_test(easy_bowling_on)
	return adjust_matrix(probability_matrix, batting_vs_pace, batting_vs_spin, batting_aggression, bowling_skill, bowling_type, wicketkeeper_fielding_skill, fielding_skill)


def get_event_number(seed, probability_list):
	running_total = 0
	for i in range(0, len(probability_list)):
		running_total = running_total + probability_list[i]
		if (seed < running_total):
			return i
	return -1


def get_delivery_type(seed, bowl_probabilities):
	event = get_event_number(seed, bowl_probabilities)
	if event == 0:
		delivery = "no_ball"
	elif event == 1:
		delivery = "wide_ball"
	elif event == 2:
		delivery = "fair_delivery"
	elif event == 3:
		delivery = "good_delivery"
	return (event, delivery)
	
def get_stroke_type(seed, stroke_probabilities):
	event = get_event_number(seed, stroke_probabilities)
	if event == 0:
		stroke = "miss"
	elif event == 1:
		stroke = "dot"
	elif event == 2:
		stroke = "hit"
	elif event == 3:
		stroke = "slog"
	# print(stroke)
	return (event, stroke)

def get_miss_result(seed, miss_probabilities):
	event = get_event_number(seed, miss_probabilities)
	if event == 0:
		result = "bowled"
	elif event == 1:
		result = "lbw"
	elif event == 2:
		result = "stumped"
	elif event == 3:
		result = "dot"
	# print(event)
	return (event, result)

def get_caught_or_not(seed, caught_out_probabilities, hit_or_slog):
	# event = get_event_number(seed, caught_out_probabilities)
	if hit_or_slog == "hit":
		# print ("hit catch; seed: "+ str(seed) + " caught_out_probability " + str(caught_out_probabilities[0]))
		if (seed < caught_out_probabilities[0]):
			return (0, "caught")
		elif (seed < 0.06):
			return (0, "dropped")
	elif hit_or_slog == "slog":
		# print ("slog catch; seed: "+ str(seed) + " caught_out_probability " + str(caught_out_probabilities[1]))
		if (seed < caught_out_probabilities[1]):
			return (0, "caught")
		elif (seed < 0.15):
			return (0, "dropped")
	return (0, "dot")

def get_hit_result(seed, hit_probabilities, caught_out_probabilities):
	event = get_event_number(seed, hit_probabilities)
	if event == 0:
		return get_caught_or_not(random.random(), caught_out_probabilities, "hit")
	elif event == 1:
		return (1, "one")
	elif event == 2:
		return (2, "two")
	elif event == 3:
		return (3, "three")
	elif event == 4:
		return (4, "four")
	elif event == 5:
		return (6, "six")
	return (-1, "error")


def get_slog_result(seed, slog_probabilities, caught_out_probabilities):
	event = get_event_number(seed, slog_probabilities)
	if event == 0:
		return get_caught_or_not(random.random(), caught_out_probabilities, "slog")
	elif event == 1:
		return (1, "one")
	elif event == 2:
		return (2, "two")
	elif event == 3:
		return (3, "three")
	elif event == 4:
		return (4, "four")
	elif event == 5:
		return (6, "six")
	return (-1, "error")