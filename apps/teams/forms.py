from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from .models import Team


class CustomTeamCreationForm(forms.ModelForm):

    class Meta:
        model = Team
        fields = ('name',)


class CustomTeamChangeForm(forms.ModelForm):

    class Meta:
        model = Team
        fields = ('name',)
