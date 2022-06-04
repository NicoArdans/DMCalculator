#!/usr/bin/python3.9

import math


class DriverMeasure:


	VALUESTREAMS = {
		"Short":{},
		"Medium":{},
		"Long":{}
		}

	for VS in VALUESTREAMS:
		VALUESTREAMS[VS] = {
			"hourlyRate":0,
			"dailyRate":0,
			"crewSize":0,
			"flats":0,
			"predictions":{}
			}
		VALUESTREAMS[VS]["predictions"] = {
			"intervals":[],
			"intervalTargets":[],
			"targetsAccumulative":[]
			}
	INTERVALS =  {
		"7-8":1,
		"8-9":1,
		"9-10":1,
		"10:20-11":0.66,
		"11-12":1,
		"12-1":1,
		"1-2":1,
		"2:20-3":0.66,
		"3-4":1,
		"4-5":1,
		"5-6":1
		}

	@classmethod

	def get_user_input(cls):
		for VS in DriverMeasure.VALUESTREAMS:
			DriverMeasure.VALUESTREAMS[VS]["hourlyRate"] = int(input("Enter hourly pick rate for "+ VS +":"))
			DriverMeasure.VALUESTREAMS[VS]["dailyRate"] = DriverMeasure.VALUESTREAMS[VS]["hourlyRate"]*7
			DriverMeasure.VALUESTREAMS[VS]["flats"] = int(input("Enter number of flats to pick for " + VS + " cycle: "))
			DriverMeasure.VALUESTREAMS[VS]["crewSize"] = math.ceil(DriverMeasure.VALUESTREAMS[VS]["flats"]/DriverMeasure.VALUESTREAMS[VS]["dailyRate"])


	def print_crew_data(cls):
		for VS in DriverMeasure.VALUESTREAMS:
			print(VS + " cycle: ", DriverMeasure.VALUESTREAMS[VS]["hourlyRate"], " Flats/Hour")
			print(VS + " cycle: ", DriverMeasure.VALUESTREAMS[VS]["dailyRate"], " Flats/Day")
			print(VS + " cycle: ", DriverMeasure.VALUESTREAMS[VS]["flats"], " Flats to pick")
			print(VS + " cycle: ", DriverMeasure.VALUESTREAMS[VS]["crewSize"], " Crew members")

	def generate_driver_measure(cls):
		for VS in DriverMeasure.VALUESTREAMS:
			DriverMeasure.VALUESTREAMS[VS]["predictions"] = {
				1:["7-8"],
				2:["8-9"],
				3:["9-10"],
				4:["10:20-11"],
				5:["11-12"],
				6:["12-1"],
				7:["1-2"],
				8:["2:20-3"],
				9:["3-4"],
				10:["4-5"],
				11:["5-6"]
				}
			for key in range(1,11):
				DriverMeasure.VALUESTREAMS[VS]["predictions"][key].append(math.floor(DriverMeasure.INTERVALS[DriverMeasure.VALUESTREAMS[VS]["predictions"][key][0]]*DriverMeasure.VALUESTREAMS[VS]["hourlyRate"]* DriverMeasure.VALUESTREAMS[VS]["crewSize"]))
				if key == 1:
					DriverMeasure.VALUESTREAMS[VS]["predictions"][key].append(DriverMeasure.VALUESTREAMS[VS]["predictions"][key][1])
				else:
					DriverMeasure.VALUESTREAMS[VS]["predictions"][key].append(math.floor(DriverMeasure.VALUESTREAMS[VS]["predictions"][key-1][2] + DriverMeasure.VALUESTREAMS[VS]["predictions"][key][1]))
					if DriverMeasure.VALUESTREAMS[VS]["predictions"][key][2] >= DriverMeasure.VALUESTREAMS[VS]["flats"]:
						break


	def generate_csv_file(cls):
		pass
	def open_csv_file(cls):
		pass



# dm = DriverMeasure()
#
# dm.get_user_input()
# dm.print_crew_data()
# dm.generate_driver_measure()
#
# print("Time: ",dm.VALUESTREAMS["Short"]["predictions"][1][0],", Hourly: ", dm.VALUESTREAMS["Short"]["predictions"][1][1],", Accumulative:", dm.VALUESTREAMS["Short"]["predictions"][1][2])
# print("Time: ",dm.VALUESTREAMS["Short"]["predictions"][2][0],", Hourly: ", dm.VALUESTREAMS["Short"]["predictions"][2][1],", Accumulative:", dm.VALUESTREAMS["Short"]["predictions"][2][2])
# print("Time: ",dm.VALUESTREAMS["Short"]["predictions"][3][0],", Hourly: ", dm.VALUESTREAMS["Short"]["predictions"][3][1],", Accumulative:", dm.VALUESTREAMS["Short"]["predictions"][3][2])
# print("Time: ",dm.VALUESTREAMS["Short"]["predictions"][4][0],", Hourly: ", dm.VALUESTREAMS["Short"]["predictions"][4][1],", Accumulative:", dm.VALUESTREAMS["Short"]["predictions"][4][2])
#
# for VS in dm.VALUESTREAMS:
# 	print(VS,":")
# 	for i in range(1,11):
# 		if len(dm.VALUESTREAMS[VS]["predictions"][i]) == 3:
# 			print("Time: ",dm.VALUESTREAMS[VS]["predictions"][i][0],", Hourly: ", dm.VALUESTREAMS[VS]["predictions"][i][1],", Accumulative:", dm.VALUESTREAMS[VS]["predictions"][i][2])
#
