from django.urls import path, include, re_path

from .views import fillSurvey, ListSurveyCBV, export_survey_home, export_single_survey_view, export_patient_surveys_view

urlpatterns = [
    path('lista-questionari', ListSurveyCBV.as_view(), name="list_survey_name"),
    path('questionario/<survey_name>/', fillSurvey, name="survey_view"),
    path('esporta-questionari', export_survey_home, name="export_survey_home"),
    path('esporta-questionari/esporta-singolo-questionario/', export_single_survey_view, name="export_single_survey"),
    # path('esporta-questionari/esporta-questionari-paziente/', export_single_survey_view, name="export_single_survey"),    
    # re_path(r'^xls/$', export_xls_patient_survey_date, name='export_xls_patient_survey_date'),
]
