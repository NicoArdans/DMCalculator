#!/usr/bin/python3.9

import math


class DriverMeasure:

	VALUESTREAMS = {
		"Short": {},
		"Medium": {},
		"Long": {}
		}
	for VS in VALUESTREAMS:
		VALUESTREAMS[VS] = {
			"hourlyRate": 0,
			"dailyRate": 0,
			"crewSize": 0,
			"flats": 0,
			"predictions": {}
			}
		VALUESTREAMS[VS]["predictions"] = {
			"intervals": [],
			"intervalTargets": [],
			"targetsAccumulative": []
			}
	INTERVALS = {
		"6-7": 1,
		"7-8": 1,
		"8-9": 1,
		"9-10": 1,
		"10:20-11": 0.66,
		"11-12": 1,
		"12-1": 1,
		"1-2": 1,
		"2:20-3": 0.66,
		"3-4": 1,
		"4-5": 1,
		"5-6": 1
		}
	timeList = []
	for timeInterval in INTERVALS:
		timeList.append(timeInterval)
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

	def generate_driver_measure(cls, start, finish):
		for VS in DriverMeasure.VALUESTREAMS:
			DriverMeasure.VALUESTREAMS[VS]["predictions"] = {
				1:["6-7"],
				2:["7-8"],
				3:["8-9"],
				4:["9-10"],
				5:["10:20-11"],
				6:["11-12"],
				7:["12-1"],
				8:["1-2"],
				9:["2:20-3"],
				10:["3-4"],
				11:["4-5"],
				12:["5-6"]
				}
			for key in range(DriverMeasure.timeList.index(start)+1, DriverMeasure.timeList.index(finish)+1):
				DriverMeasure.VALUESTREAMS[VS]["predictions"][key].append(math.floor(DriverMeasure.INTERVALS[DriverMeasure.VALUESTREAMS[VS]["predictions"][key][0]]*DriverMeasure.VALUESTREAMS[VS]["hourlyRate"]* DriverMeasure.VALUESTREAMS[VS]["crewSize"]))
				if key == DriverMeasure.timeList.index(start)+1:
					DriverMeasure.VALUESTREAMS[VS]["predictions"][key].append(DriverMeasure.VALUESTREAMS[VS]["predictions"][key][1])
				else:
					DriverMeasure.VALUESTREAMS[VS]["predictions"][key].append(math.floor(DriverMeasure.VALUESTREAMS[VS]["predictions"][key-1][2] + DriverMeasure.VALUESTREAMS[VS]["predictions"][key][1]))
					if DriverMeasure.VALUESTREAMS[VS]["predictions"][key][2] >= DriverMeasure.VALUESTREAMS[VS]["flats"]:
						break

	def generate_data(cls, cycle, rate, units, start, finish):
		startIndex = DriverMeasure.timeList.index(start)
		finishIndex = DriverMeasure.timeList.index(finish)
		totalTime = 0
		for t in range(startIndex,finishIndex):
			totalTime += DriverMeasure.INTERVALS[DriverMeasure.timeList[t]]

		DriverMeasure.VALUESTREAMS[cycle]["hourlyRate"] = rate
		DriverMeasure.VALUESTREAMS[cycle]["flats"] = units

		DriverMeasure.VALUESTREAMS[cycle]["dailyRate"] = int(DriverMeasure.VALUESTREAMS[cycle]["hourlyRate"] * totalTime)
		DriverMeasure.VALUESTREAMS[cycle]["crewSize"] = math.ceil(DriverMeasure.VALUESTREAMS[cycle]["flats"] / DriverMeasure.VALUESTREAMS[cycle]["dailyRate"])
