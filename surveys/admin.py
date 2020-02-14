from django.contrib import admin

from .models import TransplantType, Patient, Caregiver, Survey, QuestionType, Question, Answer, Patient_Survey_Question_Answer, Caregiver_Survey_Question_Answer

# Register your models here.

class CaregiverAdmin(admin.ModelAdmin):
    model = Caregiver
    list_display = ['__str__', 'get_patient', ]

    def get_patient(self, obj):
        return obj.patient.surname
    get_patient.admin_order_field = 'surname'
    get_patient.short_description = 'Patient Surname'


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
    list_display = ['get_survey', 'question_sequence_number', 'question_subsequence_number', 'type', 'content', ]

    def get_survey(self, obj):
        return obj.survey.name
    get_survey.admin_order_field = 'name'
    get_survey.short_description = 'Survey Name'

class AnswerAdmin(admin.ModelAdmin):
    model = Answer
    list_display = ['get_survey', 'get_question_sequence_number','get_question_subsequence_number', 'get_question_type' , 'get_question_content', 'value', ]

    def get_survey(self, obj):
        return obj.question.survey.name
    get_survey.admin_order_field = 'name'
    get_survey.short_description = 'Survey Name'

    def get_question_sequence_number(self, obj):
        return obj.question.question_sequence_number
    get_question_sequence_number.admin_order_field = 'question_sequence_number'
    get_question_sequence_number.short_description = 'Question\'s Sequence Number'

    def get_question_subsequence_number(self, obj):
        return obj.question.question_subsequence_number
    get_question_subsequence_number.admin_order_field = 'question_subsequence_number'
    get_question_subsequence_number.short_description = 'Question\'s Subsequence Number'

    def get_question_content(self, obj):
        return obj.question.content
    get_question_content.short_description = 'Question\'s Content'

    def get_question_type(self, obj):
        return obj.question.type
    get_question_type.short_description = 'Question\'s Type'


admin.site.register(TransplantType)
admin.site.register(Patient)
admin.site.register(Caregiver, CaregiverAdmin)
admin.site.register(Survey, SurveyAdmin)
admin.site.register(QuestionType)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Patient_Survey_Question_Answer)
admin.site.register(Caregiver_Survey_Question_Answer)
