from django.contrib import admin

from .models import TransplantType, Patient, Caregiver, Survey, QuestionType, Question, Answer, Patient_Survey_Question_Answer, Caregiver_Survey_Question_Answer

# Register your models here.
admin.site.register(TransplantType)
admin.site.register(Patient)
admin.site.register(Caregiver)
admin.site.register(Survey)
admin.site.register(QuestionType)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Patient_Survey_Question_Answer)
admin.site.register(Caregiver_Survey_Question_Answer)
