from django.urls import path, include, re_path

from .views import fillSurvey, ListSurveyCBV, export_survey_home, export_single_survey_view, export_patient_surveys_view, export_surveys_single_person_view

urlpatterns = [
    path('lista-questionari', ListSurveyCBV.as_view(), name="list_survey_name"),
    path('questionario/<survey_name>/', fillSurvey, name="survey_view"),
    # path('esporta-questionari', export_surveys, name="export_surveys"),
    path('esporta-questionari', export_survey_home, name="export_survey_home"),
    path('esporta-questionari/esporta-questionari-singolo-paziente/', export_surveys_single_person_view, name="export_survey_single_person"),
    # path('esporta-questionari/esporta-questionari-paziente/', export_single_survey_view, name="export_single_survey"),
    # re_path(r'^xls/$', export_xls_patient_survey_date, name='export_xls_patient_survey_date'),
]
