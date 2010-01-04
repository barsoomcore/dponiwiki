from django import forms
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