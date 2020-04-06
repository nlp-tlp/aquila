simple_chart_config = {
	chart: {
		node: {
			collapsable: false
		}, 
		rootOrientation: "WEST", 
		container: "#category-tree", 
		levelSeparation: 80
	}, 
	nodeStructure: {
		text: {
			name: "Entity"
		}, 
		HTMLclass: "node-color-0", 
		children: [
			{
				text: {
					name: "severity"
				}, 
				HTMLclass: "node-color-1", 
				children: [
					{
						text: {
							name: "mild"
						}, 
						HTMLclass: "node-color-1"
					}, 
					{
						text: {
							name: "traumatic"
						}, 
						HTMLclass: "node-color-1"
					}
				]
			}, 
			{
				text: {
					name: "person"
				}, 
				HTMLclass: "node-color-2", 
				children: [
					{
						text: {
							name: "injured_person"
						}, 
						HTMLclass: "node-color-2"
					}, 
					{
						text: {
							name: "operator"
						}, 
						HTMLclass: "node-color-2"
					}, 
					{
						text: {
							name: "maintainer"
						}, 
						HTMLclass: "node-color-2"
					}, 
					{
						text: {
							name: "boilermaker"
						}, 
						HTMLclass: "node-color-2"
					}, 
					{
						text: {
							name: "fitter"
						}, 
						HTMLclass: "node-color-2"
					}, 
					{
						text: {
							name: "contractor"
						}, 
						HTMLclass: "node-color-2"
					}, 
					{
						text: {
							name: "service_crew"
						}, 
						HTMLclass: "node-color-2"
					}, 
					{
						text: {
							name: "worker"
						}, 
						HTMLclass: "node-color-2"
					}, 
					{
						text: {
							name: "supervisor"
						}, 
						HTMLclass: "node-color-2"
					}, 
					{
						text: {
							name: "employee"
						}, 
						HTMLclass: "node-color-2"
					}, 
					{
						text: {
							name: "individual"
						}, 
						HTMLclass: "node-color-2"
					}, 
					{
						text: {
							name: "offsider"
						}, 
						HTMLclass: "node-color-2"
					}, 
					{
						text: {
							name: "telehandler"
						}, 
						HTMLclass: "node-color-2"
					}, 
					{
						text: {
							name: "personnel"
						}, 
						HTMLclass: "node-color-2"
					}, 
					{
						text: {
							name: "driver"
						}, 
						HTMLclass: "node-color-2"
					}, 
					{
						text: {
							name: "underground_operator"
						}, 
						HTMLclass: "node-color-2"
					}, 
					{
						text: {
							name: "process_worker"
						}, 
						HTMLclass: "node-color-2"
					}, 
					{
						text: {
							name: "blaster"
						}, 
						HTMLclass: "node-color-2"
					}, 
					{
						text: {
							name: "driller"
						}, 
						HTMLclass: "node-color-2"
					}, 
					{
						text: {
							name: "electrical_worker"
						}, 
						HTMLclass: "node-color-2"
					}, 
					{
						text: {
							name: "blast_guard"
						}, 
						HTMLclass: "node-color-2"
					}, 
					{
						text: {
							name: "spotter"
						}, 
						HTMLclass: "node-color-2"
					}
				]
			}, 
			{
				text: {
					name: "vehicle"
				}, 
				HTMLclass: "node-color-3", 
				children: [
					{
						text: {
							name: "light_vehicle"
						}, 
						HTMLclass: "node-color-3", 
						children: [
							{
								text: {
									name: "ute"
								}, 
								HTMLclass: "node-color-3"
							}, 
							{
								text: {
									name: "forklift"
								}, 
								HTMLclass: "node-color-3"
							}, 
							{
								text: {
									name: "man_car"
								}, 
								HTMLclass: "node-color-3"
							}, 
							{
								text: {
									name: "mine_car"
								}, 
								HTMLclass: "node-color-3"
							}, 
							{
								text: {
									name: "car"
								}, 
								HTMLclass: "node-color-3"
							}
						]
					}, 
					{
						text: {
							name: "heavy_vehicle"
						}, 
						HTMLclass: "node-color-3", 
						children: [
							{
								text: {
									name: "haul_truck"
								}, 
								HTMLclass: "node-color-3"
							}, 
							{
								text: {
									name: "dump_truck"
								}, 
								HTMLclass: "node-color-3"
							}, 
							{
								text: {
									name: "dozer"
								}, 
								HTMLclass: "node-color-3"
							}, 
							{
								text: {
									name: "excavator"
								}, 
								HTMLclass: "node-color-3"
							}, 
							{
								text: {
									name: "scraper"
								}, 
								HTMLclass: "node-color-3"
							}, 
							{
								text: {
									name: "bogger"
								}, 
								HTMLclass: "node-color-3"
							}, 
							{
								text: {
									name: "continuous_miner"
								}, 
								HTMLclass: "node-color-3"
							}
						]
					}
				]
			}, 
			{
				text: {
					name: "unspecified_category"
				}, 
				HTMLclass: "node-color-4"
			}, 
			{
				text: {
					name: "equipment"
				}, 
				HTMLclass: "node-color-5", 
				children: [
					{
						text: {
							name: "chute"
						}, 
						HTMLclass: "node-color-5"
					}, 
					{
						text: {
							name: "headframe"
						}, 
						HTMLclass: "node-color-5"
					}, 
					{
						text: {
							name: "mechanical_equipment"
						}, 
						HTMLclass: "node-color-5", 
						children: [
							{
								text: {
									name: "pump"
								}, 
								HTMLclass: "node-color-5"
							}, 
							{
								text: {
									name: "auger"
								}, 
								HTMLclass: "node-color-5"
							}, 
							{
								text: {
									name: "cavity_monitoring_system"
								}, 
								HTMLclass: "node-color-5"
							}, 
							{
								text: {
									name: "conveyor"
								}, 
								HTMLclass: "node-color-5"
							}, 
							{
								text: {
									name: "crusher"
								}, 
								HTMLclass: "node-color-5"
							}, 
							{
								text: {
									name: "skip"
								}, 
								HTMLclass: "node-color-5"
							}
						]
					}, 
					{
						text: {
							name: "jumbo"
						}, 
						HTMLclass: "node-color-5"
					}, 
					{
						text: {
							name: "bund_wall"
						}, 
						HTMLclass: "node-color-5"
					}, 
					{
						text: {
							name: "chock"
						}, 
						HTMLclass: "node-color-5"
					}, 
					{
						text: {
							name: "cage"
						}, 
						HTMLclass: "node-color-5"
					}, 
					{
						text: {
							name: "catenery_cable"
						}, 
						HTMLclass: "node-color-5"
					}, 
					{
						text: {
							name: "personal_protective_equipment"
						}, 
						HTMLclass: "node-color-5"
					}
				]
			}, 
			{
				text: {
					name: "body part"
				}, 
				HTMLclass: "node-color-6", 
				children: [
					{
						text: {
							name: "body"
						}, 
						HTMLclass: "node-color-6", 
						children: [
							{
								text: {
									name: "stomach"
								}, 
								HTMLclass: "node-color-6"
							}, 
							{
								text: {
									name: "torso"
								}, 
								HTMLclass: "node-color-6"
							}, 
							{
								text: {
									name: "chest"
								}, 
								HTMLclass: "node-color-6"
							}
						]
					}, 
					{
						text: {
							name: "head"
						}, 
						HTMLclass: "node-color-6", 
						children: [
							{
								text: {
									name: "eye"
								}, 
								HTMLclass: "node-color-6", 
								children: [
									{
										text: {
											name: "left_eye"
										}, 
										HTMLclass: "node-color-6"
									}, 
									{
										text: {
											name: "right_eye"
										}, 
										HTMLclass: "node-color-6"
									}
								]
							}, 
							{
								text: {
									name: "ear"
								}, 
								HTMLclass: "node-color-6", 
								children: [
									{
										text: {
											name: "left_ear"
										}, 
										HTMLclass: "node-color-6"
									}, 
									{
										text: {
											name: "right_ear"
										}, 
										HTMLclass: "node-color-6"
									}
								]
							}, 
							{
								text: {
									name: "mouth"
								}, 
								HTMLclass: "node-color-6"
							}, 
							{
								text: {
									name: "nose"
								}, 
								HTMLclass: "node-color-6"
							}
						]
					}, 
					{
						text: {
							name: "neck"
						}, 
						HTMLclass: "node-color-6"
					}, 
					{
						text: {
							name: "leg"
						}, 
						HTMLclass: "node-color-6", 
						children: [
							{
								text: {
									name: "ankle"
								}, 
								HTMLclass: "node-color-6", 
								children: [
									{
										text: {
											name: "left_ankle"
										}, 
										HTMLclass: "node-color-6"
									}, 
									{
										text: {
											name: "right_ankle"
										}, 
										HTMLclass: "node-color-6"
									}
								]
							}, 
							{
								text: {
									name: "right_leg"
								}, 
								HTMLclass: "node-color-6"
							}, 
							{
								text: {
									name: "thigh"
								}, 
								HTMLclass: "node-color-6", 
								children: [
									{
										text: {
											name: "right_thigh"
										}, 
										HTMLclass: "node-color-6"
									}, 
									{
										text: {
											name: "left_thigh"
										}, 
										HTMLclass: "node-color-6"
									}
								]
							}, 
							{
								text: {
									name: "foot"
								}, 
								HTMLclass: "node-color-6", 
								children: [
									{
										text: {
											name: "left_foot"
										}, 
										HTMLclass: "node-color-6"
									}, 
									{
										text: {
											name: "toes"
										}, 
										HTMLclass: "node-color-6"
									}, 
									{
										text: {
											name: "right_foot"
										}, 
										HTMLclass: "node-color-6"
									}
								]
							}, 
							{
								text: {
									name: "knee"
								}, 
								HTMLclass: "node-color-6", 
								children: [
									{
										text: {
											name: "left_knee"
										}, 
										HTMLclass: "node-color-6"
									}, 
									{
										text: {
											name: "right_knee"
										}, 
										HTMLclass: "node-color-6"
									}
								]
							}, 
							{
								text: {
									name: "left_leg"
								}, 
								HTMLclass: "node-color-6"
							}, 
							{
								text: {
									name: "calf"
								}, 
								HTMLclass: "node-color-6", 
								children: [
									{
										text: {
											name: "left_calf"
										}, 
										HTMLclass: "node-color-6"
									}, 
									{
										text: {
											name: "right_calf"
										}, 
										HTMLclass: "node-color-6"
									}
								]
							}
						]
					}, 
					{
						text: {
							name: "back"
						}, 
						HTMLclass: "node-color-6", 
						children: [
							{
								text: {
									name: "upper_back"
								}, 
								HTMLclass: "node-color-6"
							}, 
							{
								text: {
									name: "lower_back"
								}, 
								HTMLclass: "node-color-6"
							}
						]
					}, 
					{
						text: {
							name: "groin"
						}, 
						HTMLclass: "node-color-6"
					}, 
					{
						text: {
							name: "arm"
						}, 
						HTMLclass: "node-color-6", 
						children: [
							{
								text: {
									name: "shoulder"
								}, 
								HTMLclass: "node-color-6", 
								children: [
									{
										text: {
											name: "left_shoulder"
										}, 
										HTMLclass: "node-color-6"
									}, 
									{
										text: {
											name: "right_shoulder"
										}, 
										HTMLclass: "node-color-6"
									}
								]
							}, 
							{
								text: {
									name: "left_arm"
								}, 
								HTMLclass: "node-color-6"
							}, 
							{
								text: {
									name: "right_arm"
								}, 
								HTMLclass: "node-color-6"
							}, 
							{
								text: {
									name: "elbow"
								}, 
								HTMLclass: "node-color-6", 
								children: [
									{
										text: {
											name: "left_elbow"
										}, 
										HTMLclass: "node-color-6"
									}, 
									{
										text: {
											name: "right_elbow"
										}, 
										HTMLclass: "node-color-6"
									}
								]
							}, 
							{
								text: {
									name: "hand"
								}, 
								HTMLclass: "node-color-6", 
								children: [
									{
										text: {
											name: "right_hand"
										}, 
										HTMLclass: "node-color-6"
									}, 
									{
										text: {
											name: "left_hand"
										}, 
										HTMLclass: "node-color-6"
									}, 
									{
										text: {
											name: "fingers"
										}, 
										HTMLclass: "node-color-6"
									}
								]
							}
						]
					}
				]
			}, 
			{
				text: {
					name: "location"
				}, 
				HTMLclass: "node-color-7"
			}, 
			{
				text: {
					name: "activity"
				}, 
				HTMLclass: "node-color-8", 
				children: [
					{
						text: {
							name: "walking"
						}, 
						HTMLclass: "node-color-8"
					}, 
					{
						text: {
							name: "running"
						}, 
						HTMLclass: "node-color-8"
					}, 
					{
						text: {
							name: "driving"
						}, 
						HTMLclass: "node-color-8"
					}
				]
			}, 
			{
				text: {
					name: "injury"
				}, 
				HTMLclass: "node-color-9", 
				children: [
					{
						text: {
							name: "laceration"
						}, 
						HTMLclass: "node-color-9"
					}, 
					{
						text: {
							name: "chemical_effect"
						}, 
						HTMLclass: "node-color-9"
					}, 
					{
						text: {
							name: "loss_of_conciousness"
						}, 
						HTMLclass: "node-color-9"
					}, 
					{
						text: {
							name: "fracture"
						}, 
						HTMLclass: "node-color-9", 
						children: [
							{
								text: {
									name: "break"
								}, 
								HTMLclass: "node-color-9"
							}
						]
					}, 
					{
						text: {
							name: "amputation"
						}, 
						HTMLclass: "node-color-9"
					}, 
					{
						text: {
							name: "multiple_injuries"
						}, 
						HTMLclass: "node-color-9"
					}, 
					{
						text: {
							name: "bruises"
						}, 
						HTMLclass: "node-color-9", 
						children: [
							{
								text: {
									name: "contusion"
								}, 
								HTMLclass: "node-color-9"
							}
						]
					}, 
					{
						text: {
							name: "splinter"
						}, 
						HTMLclass: "node-color-9"
					}, 
					{
						text: {
							name: "burn"
						}, 
						HTMLclass: "node-color-9", 
						children: [
							{
								text: {
									name: "thermal_burn"
								}, 
								HTMLclass: "node-color-9"
							}, 
							{
								text: {
									name: "electric_burn"
								}, 
								HTMLclass: "node-color-9"
							}
						]
					}, 
					{
						text: {
							name: "unspecified_injuries"
						}, 
						HTMLclass: "node-color-9"
					}, 
					{
						text: {
							name: "puncture"
						}, 
						HTMLclass: "node-color-9"
					}, 
					{
						text: {
							name: "dislocation"
						}, 
						HTMLclass: "node-color-9", 
						children: [
							{
								text: {
									name: "displacement"
								}, 
								HTMLclass: "node-color-9"
							}
						]
					}, 
					{
						text: {
							name: "crush_injury"
						}, 
						HTMLclass: "node-color-9"
					}, 
					{
						text: {
							name: "bite"
						}, 
						HTMLclass: "node-color-9"
					}, 
					{
						text: {
							name: "muscle"
						}, 
						HTMLclass: "node-color-9", 
						children: [
							{
								text: {
									name: "sprain"
								}, 
								HTMLclass: "node-color-9"
							}, 
							{
								text: {
									name: "strain"
								}, 
								HTMLclass: "node-color-9"
							}
						]
					}
				]
			}, 
			{
				text: {
					name: "accident_cause"
				}, 
				HTMLclass: "node-color-10", 
				children: [
					{
						text: {
							name: "over_exertion"
						}, 
						HTMLclass: "node-color-10"
					}, 
					{
						text: {
							name: "struck_by_object"
						}, 
						HTMLclass: "node-color-10"
					}, 
					{
						text: {
							name: "caught_between"
						}, 
						HTMLclass: "node-color-10"
					}, 
					{
						text: {
							name: "recurrence"
						}, 
						HTMLclass: "node-color-10"
					}, 
					{
						text: {
							name: "stepping"
						}, 
						HTMLclass: "node-color-10"
					}, 
					{
						text: {
							name: "fall"
						}, 
						HTMLclass: "node-color-10", 
						children: [
							{
								text: {
									name: "fall_from_heights"
								}, 
								HTMLclass: "node-color-10"
							}, 
							{
								text: {
									name: "fall_from_vehicle"
								}, 
								HTMLclass: "node-color-10"
							}
						]
					}, 
					{
						text: {
							name: "trip_and_fall"
						}, 
						HTMLclass: "node-color-10"
					}, 
					{
						text: {
							name: "bodily_contact"
						}, 
						HTMLclass: "node-color-10"
					}, 
					{
						text: {
							name: "vehicle_related"
						}, 
						HTMLclass: "node-color-10"
					}
				]
			}
		]
	}
}