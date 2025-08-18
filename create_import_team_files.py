def build_squads():
	squads = open("./all_squads.csv",'r')
	players = {}
	player_info = squads.readline()
	while (player_info and player_info != ""):
		has_bowler_type = False
		bowler_type = "pace"
		is_wicketkeeper = False
		is_captain = False
		player_info = player_info.split(',')
		if len(player_info) > 2:
			player_name = player_info[0]
			bowler_type = player_info[1].strip("\n").strip(" ").lower()
			batting_skill_pace = int(player_info[2].strip("\n").strip(" "))
			batting_skill_spin = int(player_info[3].strip("\n").strip(" "))
			batting_aggression = int(player_info[4].strip("\n").strip(" "))
			bowling_skill = int(player_info[5].strip("\n").strip(" "))
			fielding_skill = int(player_info[6].strip("\n").strip(" "))
			players[player_name] = str(player_name) + "," + str(batting_skill_pace) + "," + str(batting_skill_spin) + "," + str(batting_aggression) + "," + str(bowling_skill) + "," + str(fielding_skill) + "," + str(bowler_type)
		player_info = squads.readline()
	squads.close()
	return players


def construct_teams(team_lists, players_to_import_file):

	players_dict = build_squads()

	team_name = team_lists.readline().strip("\n").strip(" ")
	short_name = team_lists.readline().strip("\n").strip(" ")
	_ = team_lists.readline()
	players = []
	for i in range(11):
		has_bowler_type = False
		bowler_type = "pace"
		is_wicketkeeper = False
		is_captain = False
		player_info = team_lists.readline().strip("\n").strip(" ")
		player_info = player_info.split(',')
		player_name = player_info[0]
		if len(player_info) > 1:
			if (player_info[1].strip("\n").strip(" ") == "WK"):
				is_wicketkeeper = True
			if (player_info[1].strip("\n").strip(" ") == "C"):
				is_captain = True
		if len(player_info) > 2:
			if (player_info[2].strip("\n").strip(" ") == "WK"):
				is_wicketkeeper = True
			if (player_info[2].strip("\n").strip(" ") == "C"):
				is_captain = True
		player_found = players_dict[player_name]

		players_to_import_file.write(str(team_name) + "," + str(short_name) + "," + str(player_found) + "," + str(is_captain) + "," + str(is_wicketkeeper) + "\n")

def parse_text(infile, outfile):
	team_lists = open(infile,'r')
	players_to_import_file = open(outfile,'w')
	players_to_import_file.write("team_name,team_short,name,batting_vs_pace,batting_vs_spin,batting_aggression,bowling_skill,fielding_skill,bowling_type,is_captain,is_wicketkeeper\n")
	home_team = construct_teams(team_lists, players_to_import_file)
	_ = team_lists.readline()
	away_team = construct_teams(team_lists, players_to_import_file)
	team_lists.close()
	players_to_import_file.close()


def main():
	team_lists_filename = "./team_lists.txt"
	players_to_import_filename = "./players_to_import.csv"

	parse_text(team_lists_filename, players_to_import_filename)


if __name__ == "__main__":
	main()