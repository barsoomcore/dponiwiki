import cgi

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from tagging.forms import TagField
from models import WikiComponent, Island, IslandComponent, StaticPage

class WikiComponentForm(forms.ModelForm):
	content = forms.CharField(
				widget=forms.Textarea(attrs={'rows':'20', 'cols':'100'}))
	name = forms.CharField(
				widget=forms.TextInput(attrs={'size':'50'}))
	comment = forms.CharField(
				widget=forms.TextInput(attrs={'size':'50'}))
	class Meta:
		model = WikiComponent
	
	def clean_content(self):
		data = self.cleaned_data['content']
		data = cgi.escape(data)
		return data

class IslandForm(WikiComponentForm):
	summary = forms.CharField(
			widget=forms.Textarea(attrs={'cols':'45'}))
	class Meta:
		model = Island
		exclude = ('slug', 'created', 'modified', 'components', 'iscanonical')
	
	def clean_summary(self):
		data = self.cleaned_data['summary']
		data = cgi.escape(data)
		return data

class IslandComponentForm(WikiComponentForm):
	tags = TagField(
			widget=forms.TextInput(attrs={'size':'50'}))
	class Meta:
		model = IslandComponent
		exclude = ('slug', 'created', 'modified')

class UserCreationFormExtended(UserCreationForm):

	def __init__(self, *args, **kwargs):
		super(UserCreationFormExtended, self).__init__(*args,
			**kwargs)
		self.fields['email'].required = True

	class Meta:
		model = User
		fields = ('username', 'email')

class StaticPageForm(forms.ModelForm):
	class Meta:
		model = StaticPage