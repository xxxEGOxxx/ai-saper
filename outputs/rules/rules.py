def findDecision(obj): #obj[0]: Size(bigger_more_difficult), obj[1]: Year(older_more_difficult), obj[2]: Protection_from_defuse, obj[3]: Meters_under_the_ground, obj[4]: Random_detonation_chance, obj[5]: Detonation_power_in_m
	# {"feature": "Random_detonation_chance", "instances": 200, "metric_value": 0.9965, "depth": 1}
	if obj[4]<=80.67436609605278:
		# {"feature": "Protection_from_defuse", "instances": 161, "metric_value": 0.9204, "depth": 2}
		if obj[2]<=0:
			# {"feature": "Meters_under_the_ground", "instances": 135, "metric_value": 0.7365, "depth": 3}
			if obj[3]<=7:
				# {"feature": "Year(older_more_difficult)", "instances": 116, "metric_value": 0.3936, "depth": 4}
				if obj[1]<=1997.8794790831414:
					# {"feature": "Detonation_power_in_m", "instances": 97, "metric_value": 0.4457, "depth": 5}
					if obj[5]<=2:
						# {"feature": "Size(bigger_more_difficult)", "instances": 65, "metric_value": 0.3335, "depth": 6}
						if obj[0]>3:
							return 'defuse'
						elif obj[0]<=3:
							return 'defuse'
						else: return 'defuse'
					elif obj[5]>2:
						# {"feature": "Size(bigger_more_difficult)", "instances": 32, "metric_value": 0.6253, "depth": 6}
						if obj[0]<=7:
							return 'defuse'
						elif obj[0]>7:
							return 'defuse'
						else: return 'defuse'
					else: return 'defuse'
				elif obj[1]>1997.8794790831414:
					return 'defuse'
				else: return 'defuse'
			elif obj[3]>7:
				return 'detonate'
			else: return 'detonate'
		elif obj[2]>0:
			return 'detonate'
		else: return 'detonate'
	elif obj[4]>80.67436609605278:
		return 'detonate'
	else: return 'detonate'
