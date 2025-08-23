from simengine.global_helpers import apply_conditions, apply_multipliers

def get_all_locations():
	locations =\
	{\
		"NYC": "New York",\
		"MEL": "Melbourne",\
		"LON": "London",\
		"BAN": "Bangkok",\
		"PAR": "Paris",\
		"CHI": "Chicago",\
		"DUB": "Dubai",\
		"SIN": "Singapore",\
		"SEO": "Seoul",\
		"KOL": "Kolkata",\
		"DHA": "Dhaka",\
		"JOH": "Johannesburg",\
		"BRI": "Bridgetown",\
		"AUC": "Auckland",\
		"SAN": "Santiago",\
		"CAP": "Cape Town",\
		"IST": "Istanbul",\
		"KAT": "Kathmandu",\
		"LAH": "Lahore",\
		"AHM": "Ahmedabad",\
		"BAN": "Bangalore",\
		"HYD": "Hyderabad",\
		"CHN": "Chennai",\
		"MUM": "Mumbai",\
		"DEL": "Delhi",\
		"MOH": "Mohali",\
		"JAI": "Jaipur",\
		"LUC": "Lucknow"\
	}
	return locations

def get_location_name(location_short_code):
	locations = get_all_locations()
	if location_short_code in locations:
		return locations[location_short_code]
	return ""

def get_location_short_code(location_name):
	locations = get_all_locations()
	for short_code, name in locations.items():
		if name == location_name:
			return short_code
	return ""

def get_home_ground_code(team_short_name):
	grounds =\
	{\
		"ESE": "NYC",\
		"MV": "MEL",\
		"BOU": "MEL",\
		"ERB": "LON",\
		"LB": "LON",\
		"BB": "BAN",\
		"PE": "PAR",\
		"MM": "CHI",\
		"DS": "DUB",\
		"SSD": "SIN",\
		"CC": "SAN",\
		"CTC": "CAP",\
		"IE": "IST",\
		"IND": "KOL",\
		"AUS": "MEL",\
		"ENG": "LON",\
		"WI": "BRI",\
		"NZ": "AUC",\
		"RSA": "JOH",\
		"PAK": "DUB",\
		"ROW": "DHA",\
		"GT": "AHM",\
		"KKR": "KOL",\
		"RCB": "BAN",\
		"SRH": "HYD",\
		"CSK": "CHN",\
		"MI": "MUM",\
		"DC": "DEL",\
		"PBKS": "MOH",\
		"RR": "JAI",\
		"LSG": "LUC"\
	}
	if team_short_name in grounds:
		return grounds[team_short_name]
	return ""

def ground_adjustments(home_team, away_team, location):
	# Aggression, Spin, Pace
	ground_multipliers =\
	{\
		"NYC": (1.01, 1.02, 0.99),\
		"MEL": (0.94, 0.95, 1.04),\
		"LON": (0.95, 0.96, 1.03),\
		"BAN": (1.00, 1.03, 0.97),\
		"PAR": (1.03, 0.95, 1.00),\
		"CHI": (0.99, 0.98, 1.02),\
		"DUB": (0.97, 0.98, 1.00),\
		"SIN": (1.05, 1.04, 0.98),\
		"KOL": (0.99, 1.03, 0.97),\
		"JOH": (1.00, 0.98, 1.02),\
		"AUC": (1.03, 0.95, 1.00),\
		"DHA": (1.01, 1.04, 0.99),\
		"BRI": (1.06, 1.02, 0.98),\
		"SEO": (1.01, 1.01, 1.01),\
		"SAN": (1.03, 1.03, 0.97),\
		"CAP": (1.00, 0.98, 1.02),\
		"IST": (0.99, 1.01, 1.00),\
		"LA": (1.10, 0.92, 0.93),\
		"TOR": (0.87, 0.97, 0.98),\
		"TOK": (0.76, 0.92, 0.93),\
		"KAT": (0.55, 1.03, 1.01),\
		"AHM": (0.99, 0.96, 0.98),\
		"LAH": (0.95, 1.03, 0.99),\
		"BAN": (1.04, 1.01, 1.00),\
		"HYD": (1.05, 0.98, 1.00),\
		"CHN": (1.02, 1.03, 0.97),\
		"MUM": (0.97, 1.01, 1.02),\
		"DEL": (0.98, 1.02, 0.99),\
		"MOH": (1.00, 0.99, 1.00),\
		"JAI": (0.99, 1.00, 1.00),\
		"LUC": (1.00, 1.00, 1.00)\
	}
	need_multiplier = False
	multipliers = (1,1,1)

	if (location != ""):
		if (location in ground_multipliers):
			multipliers = ground_multipliers[location]
			need_multiplier = True
	else:
		ground_code = get_home_ground_code(home_team.short_name)
		if ground_code != "":
			multipliers = ground_multipliers[ground_code]
			need_multiplier = True

	multipliers = apply_conditions(multipliers)

	return (apply_multipliers(home_team, away_team, multipliers, need_multiplier), multipliers)
