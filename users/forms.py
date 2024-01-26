from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone

class UserRegisterForm(UserCreationForm):
	email = forms.EmailField()
	complete_name = forms.CharField(max_length=255, label='Complete Name')
	
	class Meta:
		model = User
		fields = ['username','email','complete_name','password1', 'password2']
	
	def save(self, commit=True):
		user = super().save(commit=False)
		user.last_login = timezone.now()

		if commit:
			user.save()

		return user