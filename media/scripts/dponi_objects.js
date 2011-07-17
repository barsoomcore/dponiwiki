function DPoNIVillain(role, selected_level, role_name){

	// this object provides all the stats for a villian of the indicated role
	// and level. 'role' is a json array with two items -- the former being an
	// array of all the levels for the villain role and the fields for each,
	// and the latter being an array of all the skills for the role, along with
	// the key ability for each. You can see an example of the json in the
	// DPoNI Villain pages.
	
	this.level = role[0][selected_level-1].fields;
	
	// create a list of all abilities up to and including the 
	// selected level
	
	var total_abilities = new Array();
	for (var j = 0; j < selected_level; j++){
		for (var m = 0; m < role[0].length; m++) {
			if (role[0][m].fields.level == j+1) {
				total_abilities[j] = role[0][j].fields.abilities;
			}
		}
	}	
	this.level.abilities = total_abilities.join(', ').replace(/ ,/g, '');
	this.level.abilities = this.level.abilities.replace(/^, /, '');
	this.level.abilities = this.level.abilities.replace(/,\s*$/, '');
	
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
	
	
	// now do all the simple calculations and your object is ready to use
					
	this.level.fortitude = this.level.fortitude + this.level.constitution;
	this.level.reflex = this.level.reflex + this.level.dexterity;
	this.level.will = this.level.will + this.level.wisdom;
	this.level.toughness = this.level.toughness + this.level.constitution;

	this.level.primary_attack = this.level.base_combat_bonus + this.level.dexterity;
	this.level.mb = this.level.base_combat_bonus + this.level.strength;
	this.level.full_damage = this.level.damage + this.level.strength;
	this.level.base_defense = this.level.base_combat_bonus + 10;
	this.level.dodge = this.level.base_defense + this.level.dexterity;
	this.level.parry = this.level.base_defense + this.level.strength;
	
	this.level.secondary_attack = this.level.secondary_combat_bonus + this.level.dexterity;
	this.level.secondary_defense = this.level.secondary_combat_bonus + 10;
	this.level.secondary_dodge = this.level.secondary_defense + this.level.dexterity;
	this.level.secondary_parry = this.level.secondary_defense + this.level.strength;
				
};


function DPoNIStatblock(level, role_name, statblock_div_id, npc_name){
	
	// given a DPoNIVillain object, displays a printable statblock including
	// damage track and space for a name
	
	if (npc_name) { this.name = npc_name; }
	else { this.name = '' }
	this.role_name = role_name;
	this.level = level;
	
	// got this function from the good folks at Shopify
	// http://forums.shopify.com/categories/2/posts/29259
	this.make_ordinal = function(source) {
		var n = parseInt(source);
		var s=["th","st","nd","rd"],
		   v=n%100;
		return n+(s[(v-20)%10]||s[v]||s[0]);
	};
	
	// some numbers ought to have a '+' in front of them
	
	this.format_numbers = function() {
		var numbers = new Array();
		var characters = new Array();
		numbers = ['primary_attack', 'secondary_attack', 'secondary_damage', 'fortitude', 'reflex', 'will', 'damage', 'toughness', 'strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma', 'mb', 'full_damage'];
		characters = ['-', '<'];
		for (var i = 0; i <= numbers.length; i++){
			if (characters.indexOf(String(this.level[numbers[i]]).charAt(0)) == -1){
				this.level[numbers[i]] = '+' + this.level[numbers[i]];
			}
		}
	};
	
	var ability_cell_open = '<td width="8%" class="stat_name" style="text-align:center">';
	var ability_cell_close = '</td><td width="9%" class="statvalue">';
		
	this.display = function(){
		this.format_numbers();
		$(statblock_div_id).html('<table id="statblocktable"><tr><td>Name:</td><td colspan="6">' + this.name + '</td></tr></table>');
		$("#statblocktable tr:last").append('<td colspan="5"><strong>(' + this.make_ordinal(this.level.level) + ' Level ' + this.role_name + ')</td></tr>');
		$("#statblocktable").append('<tr class="titlebar"><td colspan="12">Abilities</td></tr><tr>' + ability_cell_open + 'STR' + ability_cell_close + this.level.strength + '</td>');
		$("#statblocktable tr:last").append(ability_cell_open + 'DEX' + ability_cell_close + this.level.dexterity + '</td>');
		$("#statblocktable tr:last").append(ability_cell_open + 'CON' + ability_cell_close + this.level.constitution + '</td>');
		$("#statblocktable tr:last").append(ability_cell_open + 'INT' + ability_cell_close + this.level.intelligence +'</td>');
		$("#statblocktable tr:last").append(ability_cell_open + 'WIS' + ability_cell_close + this.level.wisdom + '</td>');
		$("#statblocktable tr:last").append(ability_cell_open + 'CHA' + ability_cell_close + this.level.charisma + '</td></tr>');
		$("#statblocktable").append('<tr class="titlebar"><td colspan="12">Skills</td></tr><tr><td colspan="12" style="padding-bottom: 30px">' + this.level.skills + '</td></tr>');
		$("#statblocktable").append('<tr class="titlebar"><td colspan="12">Feats and Powers</td></tr><tr><td colspan="12" style="padding-bottom: 30px"><span class="Abilities">None</span></td></tr><tr class="DC_row"></tr>');
		if (this.level.abilities != '') {$(".Abilities").html(this.level.abilities);}
			else $(".Abilites").html('None');
		if (this.level.dc != null) { 
			$(".DC_row").html(
				'<td colspan="2">Save DC:</td><td colspan="10">'
				+ this.level.dc + '</span></td>')
		};
		$("#statblocktable").append('<tr class="titlebar"><td colspan="12">Combat</td></tr><tr><td class="stat_name">Init:</td><td colspan="2" class="statvalue"><span class="Init"></span></td>');
		$(".Init").html(this.level.dexterity);
		$("#statblocktable tr:last").append('<td colspan="3" class="stat_name">Primary Attack:</td><td colspan="2" class="statvalue">' + this.level.primary_attack + '</td>');
		$("#statblocktable tr:last").append('<td class="stat_name" colspan="2">Damage:</td><td colspan="2" class="statvalue">' + this.level.full_damage + '</td></tr>');
		$("#statblocktable").append('<tr><td class="stat_name">Maneuver:</td><td colspan="2" class="statvalue">' + this.level.mb + '</td>');
		$("#statblocktable tr:last").append('<td colspan="9" id="Secondary_Attack"></td></tr>');
		if (this.level.secondary_attack != "+undefined") {
			if (this.level.secondary_damage == "+undefined") { this.level.secondary_damage = this.level.full_damage; }
			$("#Secondary_Attack").replaceWith('<td colspan="3" class="stat_name">Secondary Attack:</td><td colspan="2" class="statvalue">' + this.level.secondary_attack + '</td>	<td class="stat_name" colspan="2">Damage:</td><td colspan="2" class="statvalue">' + this.level.secondary_damage + '</td>');
		}
		$("#statblocktable").append('<tr><td colspan="2" class="stat_name" style="font-style:italic; text-align:center">Defense</td><td class="stat_name" colspan="2">Flat-Footed:</td><td colspan="2" class="statvalue">' + this.level.base_defense + '<span class="Second_Defense"></span></td>');
		$("#statblocktable tr:last").append('<td class="stat_name">Dodge:</td><td colspan="2" class="statvalue">' + this.level.dodge + '<span class="Second_Dodge"></span></td>');
		$("#statblocktable tr:last").append('<td class="stat_name">Parry:</td><td colspan="2" class="statvalue">' + this.level.parry + '<span class="Second_Parry"></span></td></tr>');
		$("#statblocktable").append('<tr class="stat_name" style="text-align:center; background-color: grey; color:white"><td>Damage:</td><td colspan="2">0</td><td colspan="3">10+</td><td colspan="3">15+</td><td colspan="3">20+</td></tr>');
		$("#statblocktable").append('<tr class="stat_name" style="text-align:center"><td>/</td><td colspan="2">Bruised</td><td colspan="3">Dazed</td><td colspan="3">Staggered</td><td colspan="3">Unconscious</td></tr>');
		$("#statblocktable").append('<tr style="text-align:center;"><td>&nbsp;</td><td colspan="2"><table width="100%"><tr><td class="checkbox">&nbsp;</td><td>&nbsp;</td><td class="checkbox">&nbsp;</td><td>&nbsp;</td><td class="checkbox">&nbsp;</td></tr></table></td><td colspan="3"><table width="100%"><tr><td>&nbsp;</td><td>&nbsp;</td><td class="checkbox">&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr></table></td><td colspan="3"><table width="100%"><tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td class="checkbox">&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr></table></td><td colspan="3"><table width="100%"><tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td class="checkbox">&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr></table></td></tr>');
		$("#statblocktable").append('<tr class="stat_name" style="text-align:center"><td>X</td><td colspan="2">Hurt</td><td colspan="3">Wounded</td><td colspan="3">Disabled</td><td colspan="3">Dying</td></tr>');
		$("#statblocktable").append('<tr class="titlebar"><td colspan="12">Saves</td></tr><tr><td colspan="2" class="stat_name">Toughness:</td><td class="statvalue">' + this.level.toughness + '</td>');
		$("#statblocktable tr:last").append('<td colspan="2" class="stat_name">Fortitude:</td><td class="statvalue">' + this.level.fortitude + '</td>');
		$("#statblocktable tr:last").append('<td colspan="2" class="stat_name">Reflex:</td><td class="statvalue">' + this.level.reflex + '</td>');
		$("#statblocktable tr:last").append('<td colspan="2" class="stat_name">Will:</td><td class="statvalue">' + this.level.will + '</td>');
		if (this.level.secondary_combat_bonus) {
			$(".Second_Defense").html(' (' + this.level.secondary_defense + ')');
			$(".Second_Dodge").html(' (' + this.level.secondary_dodge + ')');
			$(".Second_Parry").html(' (' + this.level.secondary_parry + ')');
		}
		$(statblock_div_id).show();
	};
};


function RandomMonster(){
	
	// based on the great work by Esoteric at the Old School Hack Forums
	// (forums.oldschoolhack.net) -- this just creates little text descriptions
	// of improbable beasties
	
	this.attribute = ["Abominable", "Cunning", "Oozing", "Hulking", "Twisted", "Daring", "Bloodthirsty", "Menacing", "Honor-Bound", "Persuasive", "Fickle", "Clueless", "Soulless", "Pustulent", "Cowardly", "Foolish", "Zealous", "Slumbering", "Mysterious", "Beautiful"];
	this.ability = ["Flying", "Invisible", "Wish-Granting", "Far-Seeing", "Wall-Climbing", "Shape-Shifting", "Camouflaged", "Many-Armed", "Gelatinous", "Dimension-Jumping", "Scent-Following", "Leaping", "Demon-Calling", "Laughing", "Fortune-Telling", "Many-Legged", "Dead-Raising", "Magic-Eating", "Illusion-Weaving", "Insubstantial"];
	this.type = ["Undead", "Lesser", "Half", "Elder", "Purple", "Greater", "Eldritch", "Feral", "Dire", "Nocturnal", "Cyclopic", "Dark", "Clockwork", "Draconic", "Elemental", "Incorporeal", "Common", "Aquatic", "Immortal", "Heavenly"];
	this.name1 = ["Shark", "Death", "Temple", "Demon", "Battle", "Slug", "Monkey", "Desert", "Slime", "Insect", "Cave", "Giant", "Swamp", "Bird", "Hell", "Spirit", "Nightmare", "Spider", "Grave", "Thunder"];
	this.name2 = ["Golem", "Behemoth", "Stalker", "Beast", "God", "Mage", "Lord", "Fiend", "Bees", "Servant", "Slime", "Tyrant", "Knight", "Monkey", "Devourer", "Shark", "Lich", "kin", "Spawn", "Genius"];
	this.attack_adjective = ["Hypnotizing", "Poisonous", "Crushing", "Divine", "Necrotic", "Elemental", "Vengeful", "Shielding", "Ensnaring", "Warding", "Exploding", "Enervating", "Enslaving", "Ichorus", "Love-Kindling", "Hallucinogenic", "Stunning", "Psychic", "Healing", "Terrifying"];
	this.attack = ["Bite", "Breath", "Song", "Gaze", "Venom", "Tentacles", "Claws", "Secrets", "Slime", "Charge", "Frenzy", "Blades", "Blast", "Ninjas", "Aura", "Webs", "Spores", "Flatulence", "Spines", "Glyphs"];
	this.d20 = function(){
		return Math.floor(Math.random() * (19 - 0 + 1)) + 0;
	};
	this.display = function(monsterDivId){
		$(monsterDivId).html("The " + 
		this.attribute[this.d20()] + " " + 
		this.ability[this.d20()] + " " + 
		this.type[this.d20()] + " " + 
		this.name1[this.d20()] + " " + 
		this.name2[this.d20()] + " with " +
		this.attack_adjective[this.d20()] + " " +
		this.attack[this.d20()]);
	};
};