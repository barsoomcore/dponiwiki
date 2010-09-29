function create_villain(select, role_name, role_slug, statblock_div_id){
	// this gets the JSON of the villain data (including skills) and then generates
	// lists of stuff like abilities and skills that aren't exactly level-based
	// and then creates and displays a DPoNIStatblock object
	
	$.getJSON('../../villains/villain_data_json/' + role_slug + '/', function(villain_json_data){
		
		for (var i = 0; i < villain_json_data[0].length; i++){
			if (villain_json_data[0][i].fields.level == select){
				var selected_level = villain_json_data[0][i].fields;
				
				// create a list of all abilities up to and including the 
				// selected level
				
				var abilities_list = new String();
				var total_abilities = new Array();
				for (var j = 0; j < select; j++){
					for (var m = 0; m < villain_json_data[0].length; m++) {
						if (villain_json_data[0][m].fields.level == j+1) {
							total_abilities[j] = villain_json_data[0][j].fields.abilities;
						}
					}
				}	
				abilities_list = total_abilities.join(', ').replace(/ ,/g, '');
				abilities_list = abilities_list.replace(/^, /, '');
				abilities_list = abilities_list.replace(/,\s*$/, '');
				selected_level.abilities = abilities_list;
				
				// create the skills list -- setting the value for each using level
				// and key ability, and applying a smaller value for a couple of skills
				// for Artillery and War Leader
				
				var skill_list = new Array();
				for (var k = 0; k < villain_json_data[1].length; k++) {				
					var key_ability = villain_json_data[1][k].fields.key_ability;
					var this_skill = new Array();
					this_skill[0] = villain_json_data[1][k].pk;
					this_skill[1] = 3 + select + villain_json_data[0][i].fields[key_ability];
					if (role_name == 'Artillery') {
						var Level_Skills = ['Acrobatics', 'Climb', 'Jump', 'Swim'];
						for (var n = 0; n <= Level_Skills.length; n++) {
							if (this_skill[0] == Level_Skills[n]) {
								this_skill[1] = this_skill[1] - 3;
							}
						}
					}
					if (role_name == 'War Leader') {
						if (this_skill[0] == 'Notice') {
							this_skill[1] = this_skill[1] - 3;
						}
					}
					if (String(this_skill[1]).charAt(0) != '-'){
						this_skill[1] = '+' + this_skill[1];
					}
					skill_list.push(this_skill.join(':&nbsp;'));
				}
				selected_level.skills = skill_list.join('; ');
				
				// set the Reputation
				
				var Reputation = (select/5).toPrecision(1);
				if (Reputation < 1) { Reputation = 0 };
				if (role_name == 'WarLeader'){
					Reputation = Reputation + 3;
				}
				selected_level.reputation = Reputation;
				
				// create the new DPoNIStatblock object and display
				
				new_villain = new DPoNIStatblock(selected_level, role_name, statblock_div_id);
				new_villain.display();
				$("title").html(new_villain.make_ordinal(new_villain.Level) + ' Level ' + role_name);
			}
		}
	});
};