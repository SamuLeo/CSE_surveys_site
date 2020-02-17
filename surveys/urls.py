from django.urls import path, include

from .views import fillSurvey

urlpatterns = [
    path('<survey_name>/', fillSurvey, name="survey_view")

]
