from django.shortcuts import render, HttpResponse
from .form_survey import FormSurvey
from .models import Survey

# Create your views here.

def fillSurvey(request, survey_name):
    if request.method == "POST":
        form = FormSurvey(request.POST)
        if form.is_valid():
            print("Il Form è Valido!")
            # new_post = form.save()
            # print("new_post: ", new_post)
            return HttpResponse("<h1>survey compilato creato con successo!</h1>")
    else:
        form = FormSurvey(survey_name=survey_name).get_survey()
        survey_description = Survey.objects.get(pk=survey_name).description
    context = {"survey_name": survey_name, "survey_description": survey_description, "form": form}
    return render(request, "surveys/s_t.html", context)
