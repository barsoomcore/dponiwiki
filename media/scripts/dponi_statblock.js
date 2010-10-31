function DPoNIStatblock(level, role_name, statblock_div_id, npc_name){
	if (npc_name) { this.name = npc_name; }
	else { this.name = '' }
	this.role_name = role_name;
	this.level = level;
	
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
		numbers = ['bcb', 'primary_attack', 'secondary_attack', 'fortitude', 'reflex', 'will', 'damage', 'toughness', 'strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma', 'mb', 'full_damage', 'reputation'];
		for (var i = 0; i <= numbers.length; i++){
			if (String(level[numbers[i]]).charAt(0) != '-'){
				level[numbers[i]] = '+' + level[numbers[i]];
			}
		}
	};
	
	var ability_cell_open = '<td width="8%" class="stat_name" style="text-align:center">';
	var ability_cell_close = '</td><td width="9%" class="statvalue">';
	
	this.display = function(){
		this.format_numbers();
		$(statblock_div_id).html('<table id="statblocktable"><tr><td>Name:</td><td colspan="4">' + this.name + '</td></tr></table>');
		$("#statblocktable tr:last").append('<td colspan="4"><strong>(' + this.make_ordinal(level.level) + ' Level ' + this.role_name + ')</td>');
		$("#statblocktable tr:last").append('<td colspan="2" class="stat_name">Reputation:</td><td class="statvalue">' + level.reputation + '</td></tr>');
		$("#statblocktable").append('<tr class="titlebar"><td colspan="12">Abilities</td></tr><tr>' + ability_cell_open + 'STR' + ability_cell_close + level.strength + '</td>');
		$("#statblocktable tr:last").append(ability_cell_open + 'DEX' + ability_cell_close + level.dexterity + '</td>');
		$("#statblocktable tr:last").append(ability_cell_open + 'CON' + ability_cell_close + level.constitution + '</td>');
		$("#statblocktable tr:last").append(ability_cell_open + 'INT' + ability_cell_close + level.intelligence +'</td>');
		$("#statblocktable tr:last").append(ability_cell_open + 'WIS' + ability_cell_close + level.wisdom + '</td>');
		$("#statblocktable tr:last").append(ability_cell_open + 'CHA' + ability_cell_close + level.charisma + '</td></tr>');
		$("#statblocktable").append('<tr class="titlebar"><td colspan="12">Skills</td></tr><tr><td colspan="12" style="padding-bottom: 30px">' + level.skills + '</td></tr>');
		$("#statblocktable").append('<tr class="titlebar"><td colspan="12">Feats and Powers</td></tr><tr><td colspan="12" style="padding-bottom: 30px"><span class="Abilities">None</span></td></tr><tr class="DC_row"></tr>');
		if (level.abilities != '') {$(".Abilities").html(level.abilities);}
			else $(".Abilites").html('None');
		if (level.dc != null) { 
			$(".DC_row").html(
				'<td colspan="2">Save DC:</td><td colspan="10">'
				+ level.dc + '</span></td>')
		};
		$("#statblocktable").append('<tr class="titlebar"><td colspan="12">Combat</td></tr><tr><td class="stat_name">Init:</td><td colspan="2" class="statvalue"><span class="Init"></span></td>');
		$(".Init").html(level.dexterity);
		$("#statblocktable tr:last").append('<td colspan="3" class="stat_name">Primary Attack:</td><td colspan="2" class="statvalue">' + level.primary_attack + '</td>');
		$("#statblocktable tr:last").append('<td class="stat_name" colspan="2">Damage:</td><td colspan="2" class="statvalue">' + level.full_damage + '</td></tr>');
		$("#statblocktable").append('<tr><td class="stat_name">Maneuver:</td><td colspan="2" class="statvalue">' + level.mb + '</td>');
		$("#statblocktable tr:last").append('<td colspan="9" id="Secondary_Attack"></td></tr>');
		if (role_name == 'Artillery' || role_name == 'Skirmisher') {
			$("#Secondary_Attack").replaceWith('<td colspan="3" class="stat_name">Secondary Attack:</td><td colspan="2" class="statvalue">' + level.secondary_attack + '</td>	<td class="stat_name" colspan="2">Damage:</td><td colspan="2" class="statvalue">' + level.damage + '</td>');
		}
		$("#statblocktable").append('<tr><td colspan="2" class="stat_name" style="font-style:italic; text-align:center">Defense</td><td class="stat_name" colspan="2">Flat-Footed:</td><td colspan="2" class="statvalue">' + level.base_defense + '<span class="Second_Defense"></span></td>');
		$("#statblocktable tr:last").append('<td class="stat_name">Dodge:</td><td colspan="2" class="statvalue">' + level.dodge + '<span class="Second_Dodge"></span></td>');
		$("#statblocktable tr:last").append('<td class="stat_name">Parry:</td><td colspan="2" class="statvalue">' + level.parry + '<span class="Second_Parry"></span></td></tr>');
		$("#statblocktable").append('<tr class="stat_name" style="text-align:center; background-color: grey; color:white"><td>Damage:</td><td colspan="2">0</td><td colspan="3">5+</td><td colspan="3">10+</td><td colspan="3">15+</td></tr>');
		$("#statblocktable").append('<tr class="stat_name" style="text-align:center"><td>/</td><td colspan="2">Bruised</td><td colspan="3">Dazed</td><td colspan="3">Staggered</td><td colspan="3">Unconscious</td></tr>');
		$("#statblocktable").append('<tr style="text-align:center;"><td>&nbsp;</td><td colspan="2"><table width="100%"><tr><td class="checkbox">&nbsp;</td><td>&nbsp;</td><td class="checkbox">&nbsp;</td><td>&nbsp;</td><td class="checkbox">&nbsp;</td></tr></table></td><td colspan="3"><table width="100%"><tr><td>&nbsp;</td><td>&nbsp;</td><td class="checkbox">&nbsp;</td><td>&nbsp;</td><td class="checkbox">&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr></table></td><td colspan="3"><table width="100%"><tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td class="checkbox">&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr></table></td><td colspan="3"><table width="100%"><tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td class="checkbox">&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr></table></td></tr>');
		$("#statblocktable").append('<tr class="stat_name" style="text-align:center"><td>X</td><td colspan="2">Hurt</td><td colspan="3">Wounded</td><td colspan="3">Disabled</td><td colspan="3">Dying</td></tr>');
		$("#statblocktable").append('<tr class="stat_name" style="text-align:center; background-color: grey; color:white"><td>Fatigue:</td><td colspan="11"></td></tr>');
		$("#statblocktable").append('<tr class="stat_name" style="text-align:center"><td></td><td colspan="2">Strained</td><td colspan="3">Winded</td><td colspan="3">Fatigued</td><td colspan="3">Exhausted</td></tr>');
		$("#statblocktable").append('<tr style="text-align:center"><td>/</td><td colspan="2"><table width="100%"><tr><td>&nbsp;</td><td>&nbsp;</td><td class="checkbox">&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr></table></td><td colspan="3"><table width="100%"><tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td class="checkbox">&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr></table></td><td colspan="3"><table width="100%"><tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td class="checkbox">&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr></table></td><td colspan="3"><table width="100%"><tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td class="checkbox">&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr></table></td></tr>');
		$("#statblocktable").append('<tr class="titlebar"><td colspan="12">Saves</td></tr><tr><td colspan="2" class="stat_name">Toughness:</td><td class="statvalue">' + level.toughness + '</td>');
		$("#statblocktable tr:last").append('<td colspan="2" class="stat_name">Fortitude:</td><td class="statvalue">' + level.fortitude + '</td>');
		$("#statblocktable tr:last").append('<td colspan="2" class="stat_name">Reflex:</td><td class="statvalue">' + level.reflex + '</td>');
		$("#statblocktable tr:last").append('<td colspan="2" class="stat_name">Will:</td><td class="statvalue">' + level.will + '</td>');
		if (level.secondary_combat_bonus) {
			$(".Second_Defense").html(' (' + level.secondary_defense + ')');
			$(".Second_Dodge").html(' (' + level.secondary_dodge + ')');
			$(".Second_Parry").html(' (' + level.secondary_parry + ')');
		}
		$(statblock_div_id).show();
	};
};