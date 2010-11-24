from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from forms import IslandForm
from models import Island

@login_required
def update_island(request, slug=None):
	try:
		island = Island.objects.get(slug__exact=slug)
	except Island.DoesNotExist:
		island = None
	if request.method == 'POST':
		form = IslandForm(request.POST, instance=island)
		if form.is_valid():
			island = form.save(commit=False)
			if slug == None:
				island.owner = request.user
			island.save(editor=request.user)
			
			return HttpResponseRedirect(island.get_absolute_url())
	
	else:
		form = IslandForm(instance=island)
	
	return render_to_response(
		'templates/island_form.html', 
		locals(), 
		context_instance=RequestContext(request)
	)