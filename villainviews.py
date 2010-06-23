from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings

def villain_picker(request, villain=None, level='0'):

	villain_data = []
	villain_skills = []
	villain_url = ''
	if villain:
		try:
			villain_stats = open(settings.ROLES_URL + villain + '.data')
		except IOError:
			villain = None
			villain_stats = None
			villain_lines = None
		if villain_stats:
			villain_lines = villain_stats.readlines()
		if villain_lines:
			for line in villain_lines:
				line = line.rstrip('\n')
				line = line.split('|')
				villain_data.append(line)
		
		try:
			skills = open(settings.ROLES_URL + 'Skills.data')
		except IOError:
			skills = None
		if skills:
			if villain_data != []:
				skill_list = skills.readlines()
				villain_skills_names = villain_data[1][16].split(', ')
				for skill in villain_skills_names:
					skill_entry = []
					skill_entry.append(skill)
					for item in skill_list:
						item = item.rstrip('\n')
						item = item.split('|')
						if item[0] == skill:
							skill_entry.append(item[1])
					villain_skills.append(skill_entry)
		if villain:
			villain_url = '/dponiwiki/villains/' + villain
	
	if villain == "WarLeader":
		villain_name = "War Leader"
	else:
		villain_name = villain
		
	try:
		level = int(level)
		if 1 > level or level > 20:
			level = '0'
	except ValueError:
		level = '0'
		

	template_params = { 'villain': villain,
						'villain_data': villain_data,
						'villain_skills': villain_skills,
						'villain_name': villain_name,
						'villain_level': level,
						'villain_url': villain_url
	}

	return render_to_response(
		'templates/villain.html', 
		template_params, 
		context_instance=RequestContext(request)
	)