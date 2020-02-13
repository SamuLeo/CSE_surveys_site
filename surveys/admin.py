from django.contrib import admin

from .models import TransplantType, Patient, Caregiver, Survey, QuestionType, Question, Answer, Patient_Survey_Question_Answer, Caregiver_Survey_Question_Answer

# Register your models here.

ordering = ['Patient', 'Caregiver',]

class SurveyAdmin(admin.ModelAdmin):
    model = Survey
    list_display = ['name', 'description', 'patient_survey']

    # def get_questions(self, obj):
    #     for question in obj.questions.all():
    #         return question
    # get_questions.admin_order_field = 'question.question_sequence_number'
    # get_questions.short_description = 'Questions'


class QuestionAdmin(admin.ModelAdmin):
    model = Question
    list_display = ['get_survey', 'question_sequence_number', 'content', ]

    def get_survey(self, obj):
        return obj.survey.name
    get_survey.admin_order_field = 'name'
    get_survey.short_description = 'Survey Name'

class AnswerAdmin(admin.ModelAdmin):
    model = Answer
    list_display = ['get_survey', 'get_question_sequence_number', 'get_question_content', 'value']

    def get_survey(self, obj):
        return obj.question.survey.name
    get_survey.admin_order_field = 'name'
    get_survey.short_description = 'Survey Name'

    def get_question_sequence_number(self, obj):
        return obj.question.question_sequence_number
    get_question_sequence_number.admin_order_field = 'question_sequence_number'
    get_question_sequence_number.short_description = 'Question Sequence Number'

    def get_question_content(self, obj):
        return obj.question.content
    get_question_content.short_description = 'Question Content'


admin.site.register(TransplantType)
admin.site.register(Patient)
admin.site.register(Caregiver)
admin.site.register(Survey, SurveyAdmin)
admin.site.register(QuestionType)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Patient_Survey_Question_Answer)
admin.site.register(Caregiver_Survey_Question_Answer)
