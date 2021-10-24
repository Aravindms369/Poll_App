from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import fields
from .models import Question,Choice, Change_choice, Vote_count

# Create your forms here.
# postform for creating post
class PostForm(forms.ModelForm):
  

    class Meta:
        model = Question
        fields = ('question_text', 'my_field')
# choiceform for craeting choices
class ChoiceForm(forms.ModelForm):
  

    class Meta:
        model = Choice
        fields = ('question', 'choice_text')
# choice_edit_form for editing choices
class Choice_edit_Form(forms.ModelForm):
  
    class Meta:
        model = Change_choice
        fields = ('question', 'choice_text','new_choice')
# form for ensuring user only vote once
class Voted_count(forms.ModelForm):
    class Meta:
        model = Vote_count
        fields = ('question_voted','voter')

