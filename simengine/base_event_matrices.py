def base_event_matrix_t20(easy_bowling_on):
	#TODO: Incorporate risk

	# Ordered as noball, wide, fair, good
	# bowl_probabilities = [0.05, 0.05, 0.60, 0.30]
	bowl_probabilities = [0.01, 0.035, 0.70, 0.255]

	# Ordered as miss, dot, hit, aggressive hit/slog
	# stroke_probabilities = [0.1, 0.2,  0.6 , 0.1]
	stroke_probabilities = [0.1, 0.22,  0.61 , 0.07]

	# Ordered as bowled, LBW, stumped, dot
	# miss_probabilities = [0.07, 0.05, 0.88]
	miss_probabilities = [0.035, 0.02, 0.01, 0.935]

	# Ordered as 0, 1, 2, 3, 4, 6
	# hit_probabilities = [0.20, 0.33, 0.22, 0.05, 0.12, 0.08]
	# hit_probabilities = [0.30, 0.31, 0.20, 0.03, 0.10, 0.06]
	# hit_probabilities = [0.32, 0.33, 0.20, 0.03, 0.08, 0.04] - 12/29/20
	hit_probabilities = [0.32, 0.34, 0.20, 0.03, 0.08, 0.03]

	# Ordered as 0, 1, 2, 3, 4, 6
	# slog_probabilities = [0.17, 0.20, 0.10, 0.03, 0.30, 0.15]
	# slog_probabilities = [0.27, 0.18, 0.08, 0.01, 0.28, 0.13]
	# slog_probabilities = [0.29, 0.24, 0.11, 0.01, 0.195, 0.105]
	# slog_probabilities = [0.33, 0.22, 0.10, 0.01, 0.19, 0.10] - 12/29/20
	slog_probabilities = [0.33, 0.22, 0.13, 0.01, 0.18, 0.08]

	# Ordered as hit 0, slog 0
	# caught_out_probabilities = [0.27, 0.60]
	caught_out_probabilities = [0.05, 0.12]

	probability_matrix =\
	{"bowl_probabilities": bowl_probabilities,\
	 "stroke_probabilities": stroke_probabilities,\
	 "miss_probabilities": miss_probabilities,\
	 "hit_probabilities": hit_probabilities,\
	 "slog_probabilities": slog_probabilities,\
	 "caught_out_probabilities": caught_out_probabilities,\
	 "easy_bowling_on": easy_bowling_on}

	return probability_matrix


def base_event_matrix_odi(easy_bowling_on):
	#TODO: Incorporate risk

	# Ordered as noball, wide, fair, good
	# bowl_probabilities = [0.05, 0.05, 0.60, 0.30]
	bowl_probabilities = [0.01, 0.035, 0.70, 0.255]

	# Ordered as miss, dot, hit, aggressive hit/slog
	# stroke_probabilities = [0.1, 0.2,  0.6 , 0.1]
	stroke_probabilities = [0.06, 0.24,  0.65 , 0.05]

	# Ordered as bowled, LBW, stumped, dot
	# miss_probabilities = [0.07, 0.05, 0.88]
	miss_probabilities = [0.02, 0.015, 0.005, 0.96]

	# Ordered as 0, 1, 2, 3, 4, 6
	# hit_probabilities = [0.20, 0.33, 0.22, 0.05, 0.12, 0.08]
	# hit_probabilities = [0.30, 0.31, 0.20, 0.03, 0.10, 0.06]
	hit_probabilities = [0.40, 0.34, 0.175, 0.01, 0.05, 0.025]

	# Ordered as 0, 1, 2, 3, 4, 6
	# slog_probabilities = [0.17, 0.20, 0.10, 0.03, 0.30, 0.15]
	# slog_probabilities = [0.27, 0.18, 0.08, 0.01, 0.28, 0.13]
	# slog_probabilities = [0.29, 0.24, 0.11, 0.01, 0.195, 0.105]
	slog_probabilities = [0.41, 0.23, 0.15, 0.01, 0.13, 0.07]

	# Ordered as hit 0, slog 0
	# caught_out_probabilities = [0.27, 0.60]
	caught_out_probabilities = [0.03, 0.07]

	probability_matrix =\
	{"bowl_probabilities": bowl_probabilities,\
	 "stroke_probabilities": stroke_probabilities,\
	 "miss_probabilities": miss_probabilities,\
	 "hit_probabilities": hit_probabilities,\
	 "slog_probabilities": slog_probabilities,\
	 "caught_out_probabilities": caught_out_probabilities,\
	 "easy_bowling_on": easy_bowling_on}

	return probability_matrix


def base_event_matrix_test(easy_bowling_on):
	#TODO: Incorporate risk

	# Ordered as noball, wide, fair, good
	# bowl_probabilities = [0.05, 0.05, 0.60, 0.30]
	bowl_probabilities = [0.01, 0.02, 0.82, 0.15]

	# Ordered as miss, dot, hit, aggressive hit/slog
	# stroke_probabilities = [0.1, 0.2,  0.6 , 0.1]
	stroke_probabilities = [0.04, 0.46,  0.49 , 0.01]

	# Ordered as bowled, LBW, stumped, dot
	# miss_probabilities = [0.07, 0.05, 0.88]
	miss_probabilities = [0.001, 0.0007, 0.0003, 0.998]

	# Ordered as 0, 1, 2, 3, 4, 6
	# hit_probabilities = [0.20, 0.33, 0.22, 0.05, 0.12, 0.08]
	# hit_probabilities = [0.30, 0.31, 0.20, 0.03, 0.10, 0.06]
	hit_probabilities = [0.42, 0.36, 0.175, 0.01, 0.03, 0.005]

	# Ordered as 0, 1, 2, 3, 4, 6
	# slog_probabilities = [0.17, 0.20, 0.10, 0.03, 0.30, 0.15]
	# slog_probabilities = [0.27, 0.18, 0.08, 0.01, 0.28, 0.13]
	# slog_probabilities = [0.29, 0.24, 0.11, 0.01, 0.195, 0.105]
	slog_probabilities = [0.45, 0.25, 0.15, 0.01, 0.10, 0.04]

	# Ordered as hit 0, slog 0
	# caught_out_probabilities = [0.27, 0.60]
	caught_out_probabilities = [0.003, 0.007]

	probability_matrix =\
	{"bowl_probabilities": bowl_probabilities,\
	 "stroke_probabilities": stroke_probabilities,\
	 "miss_probabilities": miss_probabilities,\
	 "hit_probabilities": hit_probabilities,\
	 "slog_probabilities": slog_probabilities,\
	 "caught_out_probabilities": caught_out_probabilities,\
	 "easy_bowling_on": easy_bowling_on}
	 
	return probability_matrix
