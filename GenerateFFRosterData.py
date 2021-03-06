import TBAconnection

teams_per_roster = 12

einstein = ["cmptx", "cmpmo"]
houston = ["carv", "gal", "hop", "new", "roe", "tur"]
stlouis = ["arc", "cars", "cur", "dal", "dar", "tes"]

def generate(location, date):
	filein = location + "/" + date + "/rosters-" + date + ".csv"
	f = open(filein, "r")
	rosters_str = f.read().splitlines()
	rosters = {}

	for roster_str in rosters_str:
		content = roster_str.split(',')
		name = content[0]
		teams = content[1:]

		rosters[name] = teams

	for roster in rosters:
		out = location + "/" + date + "/" + roster + "-" + date + ".csv"
		file_out = open(out, "w")

		for team in rosters[roster]:
			events_on_week = {}
			events = TBAconnection.get_team_events(team, 2017)
			for event in events:
				week = event.get_week()
				key = event.get_key()
				if key[4:] in einstein:
					continue
				if key[4:] in houston:
					week = 8
				if key[4:] in stlouis:
					week = 9
				events_on_week[week] = key
			print events_on_week
			full_team = TBAconnection.get_team(team)
			district_data = TBAconnection.get_distrct_history(team)
			if "2017" in district_data:
				district = district_data["2017"][4:]
			else:
				district = "None"
			name = full_team.get_nickname()

			file_out.write(str(team) + "," + ''.join([i if ord(i) < 128 else "" for i in name]) + "," + district)
			for i in range(1, 10):
				file_out.write(",")
				if i in events_on_week:
					file_out.write(events_on_week[i][4:])
			file_out.write("\n")
		file_out.close()