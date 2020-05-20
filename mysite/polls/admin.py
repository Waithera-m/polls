from django.contrib import admin

# Register your models here.
from .models import Question,Choice

class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Date Information', {'fields': ['pub_date'], 'classes':['collapse']}),
        ('Question', {'fields': ['question_text']}),
    ]
    inlines = [ChoiceInLine]
    list_display = ('question_text','pub_date')
    list_filter = ['pub_date']
    search_fields = ['question_text']

admin.site.register(Question,QuestionAdmin)
