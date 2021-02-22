from django import forms

from .models import *


class AddTaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['title', 'completed']


class AddGroupForm(forms.ModelForm):

    class Meta:
        model = Group
        fields = '__all__'

