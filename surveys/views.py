from django.shortcuts import render, HttpResponse
from django.views.generic.list import ListView

from .form_survey import FormSurvey, FormExportSingleSurvey, FormExportPatientSurveys
from .models import Patient, Caregiver, Answer, Survey,Patient_Survey_Question_Answer,Caregiver_Survey_Question_Answer, Question
from .export_to_xls_module import export_to_xls_single_survey
# Create your views here.


def fillSurvey(request, survey_name):
    if request.method == "POST":
        form = FormSurvey(request.POST)

        if form.is_valid():
            id_patient = request.POST.get('id_patient')
            survey = Survey.objects.get(pk=survey_name)
            patient = Patient.objects.get(pk=id_patient)
            date = request.POST.get('filling_date')

            for question in survey.questions.all():
                if question.type.__str__() == "Instructions in compound question":
                    continue

                id_answer = request.POST.get(question.__str__())
                answer = Answer.objects.get(pk=id_answer)
                patient_answer = Patient_Survey_Question_Answer(
                                    patient=patient,
                                    survey=survey,
                                    question=question,
                                    answer=answer,
                                    date=date)
                patient_answer.save()
            return render(request, "surveys/survey_completed_success.html")
    else:
        form = FormSurvey(survey_name=survey_name).get_survey()
        survey_description = Survey.objects.get(pk=survey_name).description
        patients = Patient.objects.values_list("id_patient", "name", "surname")
        context = {"survey_name": survey_name, "survey_description": survey_description, "form": form, "patients": patients}
    return render(request, "surveys/survey_template.html", context)


def export_survey_home(request):
    return render(request, "surveys/export_survey_home.html")


def export_single_survey_view(request):
    if request.method == "POST":
        # id_patient = request.POST.get('id_patient')
        # patient = Patient.objects.get(pk=id_patient)
        # survey_name = request.POST.get('survey')
        # survey = Survey.objects.get(pk=survey_name)
        # date = request.POST.get('filling_date')
        form = FormExportSingleSurvey(request.POST)

        if form.is_valid():
            id_patient = form.cleaned_data["patient"]
            patient = Patient.objects.get(pk=id_patient)
            survey_name = form.cleaned_data["survey"]
            survey = Survey.objects.get(pk=survey_name)
            date = form.cleaned_data["date"]
            # if self.validate_form_export_single_survey_view(patient=patient, survey=survey, date=date):
            return export_to_xls_single_survey(request=request, patient=patient, survey=survey, date=date)
    else:
        # patients = Patient.objects.values_list("id_patient", "name", "surname")
        # surveys = Survey.objects.all()
        # context = {"patients": patients, "surveys": surveys}
        # return render(request, "surveys/export_single_survey.html", context)
        form = FormExportSingleSurvey()

    context = {"form": form}
    return render(request, "surveys/export_single_survey.html", context)


def export_patient_surveys_view(request):
    if request.method == "POST":
        # id_patient = request.POST.get('id_patient')
        # patient = Patient.objects.get(pk=id_patient)
        # survey_name = request.POST.get('survey')
        # survey = Survey.objects.get(pk=survey_name)
        # date = request.POST.get('filling_date')
        form = FormExportPatientSurveys(request.POST)

        if form.is_valid():
            id_patient = form.cleaned_data["patient"]
            patient = Patient.objects.get(pk=id_patient)
            survey_name = form.cleaned_data["survey"]
            survey = Survey.objects.get(pk=survey_name)
            # if self.validate_form_export_single_survey_view(patient=patient, survey=survey, date=date):
            return export_to_xls_patient_surveys(request=request, patient=patient, survey=survey)
    else:
        # patients = Patient.objects.values_list("id_patient", "name", "surname")
        # surveys = Survey.objects.all()
        # context = {"patients": patients, "surveys": surveys}
        # return render(request, "surveys/export_single_survey.html", context)
        form = FormExportPatientSurveys()

    context = {"form": form}
    return render(request, "surveys/export_patient_surveys.html", context)


class ListSurveyCBV(ListView):
    model = Survey
    paginate_by = 5
    template_name = "surveys/survey_list_template.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["surveys"] = Survey.objects.all()
        return context
