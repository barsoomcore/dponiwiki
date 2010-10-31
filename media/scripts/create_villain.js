function create_villain(role, selected_level, role_name){
	
	var raw_level = role[0][selected_level-1].fields;
	this.level = raw_level;
	
	// create a list of all abilities up to and including the 
	// selected level
	
	var abilities_list = new String();
	var total_abilities = new Array();
	for (var j = 0; j < selected_level; j++){
		for (var m = 0; m < role[0].length; m++) {
			if (role[0][m].fields.level == j+1) {
				total_abilities[j] = role[0][j].fields.abilities;
			}
		}
	}	
	abilities_list = total_abilities.join(', ').replace(/ ,/g, '');
	abilities_list = abilities_list.replace(/^, /, '');
	abilities_list = abilities_list.replace(/,\s*$/, '');
	this.level.abilities = abilities_list;
	
	// create the skills list -- setting the value for each using level
	// and key ability, and applying a smaller value for a couple of skills
	// for Artillery and War Leader
	
	var skill_list = new Array();
	for (var k = 0; k < role[1].length; k++) {				
		var key_ability = role[1][k].fields.key_ability;
		var this_skill = new Array();
		this_skill[0] = role[1][k].pk;
		this_skill[1] = 3 + selected_level + role[0][selected_level-1].fields[key_ability];
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
	this.level.skills = skill_list.join('; ');
	
	
	// set the Reputation
	
	var Reputation = (selected_level/5).toPrecision(1);
	if (Reputation < 1) { Reputation = 0 };
	if (role_name == 'WarLeader'){
		Reputation = Reputation + 3;
	}
	this.level.reputation = Reputation;
	
	// now do all the simple calculations
					
	this.level.fortitude = raw_level.fortitude + raw_level.constitution;
	this.level.reflex = raw_level.reflex + raw_level.dexterity;
	this.level.will = raw_level.will + raw_level.wisdom;
	this.level.toughness = raw_level.toughness + raw_level.constitution;

	this.level.primary_attack = raw_level.base_combat_bonus + raw_level.dexterity;
	this.level.mb = raw_level.base_combat_bonus + raw_level.strength;
	this.level.full_damage = raw_level.damage + raw_level.strength;
	this.level.base_defense = raw_level.base_combat_bonus + 10;
	this.level.dodge = raw_level.base_defense + raw_level.dexterity;
	this.level.parry = raw_level.base_defense + raw_level.strength;
	
	this.level.secondary_attack = raw_level.secondary_combat_bonus + raw_level.dexterity;
	this.level.secondary_defense = raw_level.secondary_combat_bonus + 10;
	this.level.secondary_dodge = raw_level.secondary_defense + raw_level.dexterity;
	this.level.secondary_parry = raw_level.secondary_defense + raw_level.strength;
				
};