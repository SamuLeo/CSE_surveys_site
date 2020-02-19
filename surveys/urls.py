from django.urls import path, include

from .views import fillSurvey, ListSurveyCBV

urlpatterns = [
    path('lista_questionari', ListSurveyCBV.as_view(), name="list_survey_name"),
    path('questionario/<survey_name>/', fillSurvey, name="survey_view")

]
