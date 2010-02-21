from django.conf.urls.defaults import *
from django.contrib.auth.views import login

urlpatterns = patterns('django.contrib.auth.views',
    url(r'^login/$',  
    	'login', 
    	{ 'template_name': 'templates/registration/login.html'}, 
    	name='login'
    ),
    url(r'^logout/$', 
    	'logout', 
    	{'next_page': '/dponiwiki/'}, 
    	name='logout'
    ),
	url(r'^password_change/$', 
		'password_change', 
		{'template_name': 'templates/registration/password_change_form.html'}, 
		name='password_change'
	),
	url(r'^password_change/done/$', 
		'password_change_done', 
		{'template_name': 'templates/registration/password_change_done.html'}
	),
	url(r'^password_reset/$',
		'password_reset',
		{'template_name': 'templates/registration/password_reset_form.html',
		'email_template_name': 'templates/registration/password_reset_email.html'},
		name='password_reset'
	),
	url(r'^password_reset/done/$',
		'password_reset_done',
		{'template_name': 'templates/registration/password_reset_done.html'},
		name='password_reset_done'
	),
	url(r'^password_reset_confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
		'password_reset_confirm',
		{'template_name': 'templates/registration/password_reset_confirm.html'},
		name='password_reset_confirm'
	),
	url(r'^password_reset_complete/$',
		'password_reset_complete',
		{'template_name': 'templates/registration/password_reset_complete.html'},
		name='password_reset_complete'
	),
)