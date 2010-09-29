function DPoNIStatblock(selected_level, role_name, statblock_div_id, npc_name){
	if (npc_name) { this.Name = npc_name; }
	else { this.Name = '' }
	this.Role_Name = role_name;
	this.Level = selected_level.level;
	this.BCB = selected_level.base_combat_bonus;
	this.SCB = selected_level.secondary_combat_bonus;
	this.Fortitude = selected_level.fortitude + selected_level.constitution;
	this.Reflex = selected_level.reflex + selected_level.dexterity;
	this.Will = selected_level.will + selected_level.wisdom;
	this.DC = selected_level.dc;
	this.Damage = selected_level.damage;
	this.Toughness = selected_level.toughness + selected_level.constitution;
	this.Strength = String(selected_level.strength);
	this.Dexterity = String(selected_level.dexterity);
	this.Constitution = String(selected_level.constitution);
	this.Intelligence =String(selected_level.intelligence);
	this.Wisdom = String(selected_level.wisdom);
	this.Charisma = String(selected_level.charisma);
	
	this.MB = this.BCB + selected_level.strength;
	this.Primary_Attack = this.BCB + selected_level.dexterity;
	this.Full_Damage = this.Damage + selected_level.strength;
	this.Base_Defense = this.BCB + 10;
	this.Dodge = this.Base_Defense + selected_level.dexterity;
	this.Parry = this.Base_Defense + selected_level.strength;
	
	this.Secondary_Attack = this.SCB + selected_level.dexterity;
	this.Second_Defense = this.SCB + 10;
	this.Second_Dodge = this.Second_Defense + selected_level.dexterity;
	this.Second_Parry = this.Second_Defense + selected_level.strength;
	
	this.Abilities = selected_level.abilities;
	this.Skills = selected_level.skills;
	this.Reputation = selected_level.reputation;
	
		
	// got this function from the good folks at Shopify
	// http://forums.shopify.com/categories/2/posts/29259
	this.make_ordinal = function(source) {
		var n = source;
		var s=["th","st","nd","rd"],
		   v=n%100;
		return n+(s[(v-20)%10]||s[v]||s[0]);
	};
	
	this.format_numbers = function() {
		var numbers = new Array();
		numbers = ['BCB', 'Primary_Attack', 'Secondary_Attack', 'Fortitude', 'Reflex', 'Will', 'Damage', 'Toughness', 'Strength', 'Dexterity', 'Constitution', 'Intelligence', 'Wisdom', 'Charisma', 'MB', 'Full_Damage', 'Reputation'];
		for (var i = 0; i <= numbers.length; i++){
			if (String(this[numbers[i]]).charAt(0) != '-'){
				this[numbers[i]] = '+' + this[numbers[i]];
			}
		}
	};
	
	var ability_cell_open = '<td width="8%" class="stat_name" style="text-align:center">';
	var ability_cell_close = '</td><td width="9%" class="statvalue">';
	
	this.display = function(){
		this.format_numbers();
		$(statblock_div_id).html('<table id="statblocktable"><tr><td>Name:</td><td colspan="4">' + this.Name + '</td></tr></table>');
		$("#statblocktable tr:last").append('<td colspan="4"><strong>(' + this.make_ordinal(this.Level) + ' Level ' + this.Role_Name + ')</td>');
		$("#statblocktable tr:last").append('<td colspan="2" class="stat_name">Reputation:</td><td class="statvalue">' + this.Reputation + '</td></tr>');
		$("#statblocktable").append('<tr class="titlebar"><td colspan="12">Abilities</td></tr><tr>' + ability_cell_open + 'STR' + ability_cell_close + this.Strength + '</td>');
		$("#statblocktable tr:last").append(ability_cell_open + 'DEX' + ability_cell_close + this.Dexterity + '</td>');
		$("#statblocktable tr:last").append(ability_cell_open + 'CON' + ability_cell_close + this.Constitution + '</td>');
		$("#statblocktable tr:last").append(ability_cell_open + 'INT' + ability_cell_close + this.Intelligence +'</td>');
		$("#statblocktable tr:last").append(ability_cell_open + 'WIS' + ability_cell_close + this.Wisdom + '</td>');
		$("#statblocktable tr:last").append(ability_cell_open + 'CHA' + ability_cell_close + this.Charisma + '</td></tr>');
		$("#statblocktable").append('<tr class="titlebar"><td colspan="12">Skills</td></tr><tr><td colspan="12" style="padding-bottom: 30px">' + this.Skills + '</td></tr>');
		$("#statblocktable").append('<tr class="titlebar"><td colspan="12">Feats and Powers</td></tr><tr><td colspan="12" style="padding-bottom: 30px"><span class="Abilities">None</span></td></tr><tr class="DC_row"></tr>');
		if (this.Abilities != '') {$(".Abilities").html(this.Abilities);}
			else $(".Abilites").html('None');
		if (this.DC != null) { 
			$(".DC_row").html(
				'<td colspan="2">Save DC:</td><td colspan="10">'
				+ this.DC + '</span></td>')
		};
		$("#statblocktable").append('<tr class="titlebar"><td colspan="12">Combat</td></tr><tr><td class="stat_name">Init:</td><td colspan="2" class="statvalue"><span class="Init"></span></td>');
		$(".Init").html(this.Dexterity);
		$("#statblocktable tr:last").append('<td colspan="3" class="stat_name">Primary Attack:</td><td colspan="2" class="statvalue">' + this.Primary_Attack + '</td>');
		$("#statblocktable tr:last").append('<td class="stat_name" colspan="2">Damage:</td><td colspan="2" class="statvalue">' + this.Full_Damage + '</td></tr>');
		$("#statblocktable").append('<tr><td class="stat_name">Maneuver:</td><td colspan="2" class="statvalue">' + this.MB + '</td>');
		$("#statblocktable tr:last").append('<td colspan="9" id="Secondary_Attack"></td></tr>');
		if (this.Role_Name == 'Artillery' || this.Role_Name == 'Skirmisher') {
			$("#Secondary_Attack").replaceWith('<td colspan="3" class="stat_name">Secondary Attack:</td><td colspan="2" class="statvalue">' + this.Secondary_Attack + '</td>	<td class="stat_name" colspan="2">Damage:</td><td colspan="2" class="statvalue">' + this.Damage + '</td>');
		}
		$("#statblocktable").append('<tr><td colspan="2" class="stat_name" style="font-style:italic; text-align:center">Defense</td><td class="stat_name" colspan="2">Flat-Footed:</td><td colspan="2" class="statvalue">' + this.Base_Defense + '<span class="Second_Defense"></span></td>');
		$("#statblocktable tr:last").append('<td class="stat_name">Dodge:</td><td colspan="2" class="statvalue">' + this.Dodge + '<span class="Second_Dodge"></span></td>');
		$("#statblocktable tr:last").append('<td class="stat_name">Parry:</td><td colspan="2" class="statvalue">' + this.Parry + '<span class="Second_Parry"></span></td></tr>');
		$("#statblocktable").append('<tr class="stat_name" style="text-align:center; background-color: grey; color:white"><td>Damage:</td><td colspan="2">0</td><td colspan="3">5+</td><td colspan="3">10+</td><td colspan="3">15+</td></tr>');
		$("#statblocktable").append('<tr class="stat_name" style="text-align:center"><td>/</td><td colspan="2">Bruised</td><td colspan="3">Dazed</td><td colspan="3">Staggered</td><td colspan="3">Unconscious</td></tr>');
		$("#statblocktable").append('<tr style="text-align:center;"><td>&nbsp;</td><td colspan="2"><table width="100%"><tr><td class="checkbox">&nbsp;</td><td>&nbsp;</td><td class="checkbox">&nbsp;</td><td>&nbsp;</td><td class="checkbox">&nbsp;</td></tr></table></td><td colspan="3"><table width="100%"><tr><td>&nbsp;</td><td>&nbsp;</td><td class="checkbox">&nbsp;</td><td>&nbsp;</td><td class="checkbox">&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr></table></td><td colspan="3"><table width="100%"><tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td class="checkbox">&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr></table></td><td colspan="3"><table width="100%"><tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td class="checkbox">&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr></table></td></tr>');
		$("#statblocktable").append('<tr class="stat_name" style="text-align:center"><td>X</td><td colspan="2">Hurt</td><td colspan="3">Wounded</td><td colspan="3">Disabled</td><td colspan="3">Dying</td></tr>');
		$("#statblocktable").append('<tr class="stat_name" style="text-align:center; background-color: grey; color:white"><td>Fatigue:</td><td colspan="11"></td></tr>');
		$("#statblocktable").append('<tr class="stat_name" style="text-align:center"><td></td><td colspan="2">Strained</td><td colspan="3">Winded</td><td colspan="3">Fatigued</td><td colspan="3">Exhausted</td></tr>');
		$("#statblocktable").append('<tr style="text-align:center"><td>/</td><td colspan="2"><table width="100%"><tr><td>&nbsp;</td><td>&nbsp;</td><td class="checkbox">&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr></table></td><td colspan="3"><table width="100%"><tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td class="checkbox">&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr></table></td><td colspan="3"><table width="100%"><tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td class="checkbox">&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr></table></td><td colspan="3"><table width="100%"><tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td class="checkbox">&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr></table></td></tr>');
		$("#statblocktable").append('<tr class="titlebar"><td colspan="12">Saves</td></tr><tr><td colspan="2" class="stat_name">Toughness:</td><td class="statvalue">' + this.Toughness + '</td>');
		$("#statblocktable tr:last").append('<td colspan="2" class="stat_name">Fortitude:</td><td class="statvalue">' + this.Fortitude + '</td>');
		$("#statblocktable tr:last").append('<td colspan="2" class="stat_name">Reflex:</td><td class="statvalue">' + this.Reflex + '</td>');
		$("#statblocktable tr:last").append('<td colspan="2" class="stat_name">Will:</td><td class="statvalue">' + this.Will + '</td>');
		if (this.SCB) {
			$(".Second_Defense").html(' (' + this.Second_Defense + ')');
			$(".Second_Dodge").html(' (' + this.Second_Dodge + ')');
			$(".Second_Parry").html(' (' + this.Second_Parry + ')');
		}
		$(statblock_div_id).show();
	};
};