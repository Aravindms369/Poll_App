from django.contrib import admin
# import all models fom models.py
from .models import Choice, Question, User, Change_choice, Vote_count
# register all models in admin interface
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(User)
admin.site.register(Change_choice)
admin.site.register(Vote_count)