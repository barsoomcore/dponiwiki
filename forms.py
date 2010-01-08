from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from models import WikiComponent, Island, IslandComponent

class WikiComponentForm(forms.ModelForm):
	content = forms.CharField(
				widget=forms.Textarea(attrs={'rows':'20'}))
	class Meta:
		model = WikiComponent


class IslandForm(WikiComponentForm):
	class Meta:
		model = Island
		exclude = ('slug', 'created', 'modified', 'components', 'iscanonical')

class IslandComponentForm(WikiComponentForm):
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