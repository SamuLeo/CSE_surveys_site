from django.shortcuts import render, HttpResponse
from django.views.generic.list import ListView

from .form_survey import FormSurvey, FormExportSingleSurvey, FormExportPatientSurveys, FormExportSurveysSinglePerson
from .models import Patient, Caregiver, Answer, Survey,Patient_Survey_Question_Answer,Caregiver_Survey_Question_Answer, Question
from .export_to_xls_module import export_to_xls_single_survey
# Create your views here.


def fillSurvey(request, survey_name):
    if request.method == "POST":
        form = FormSurvey(survey_name, request.POST)

        if form.is_valid():
            try:
                form.process(request)
            except:
                return render(request, "surveys/survey_filling_error.html")

            return render(request, "surveys/survey_filling_success.html")
    else:
        form = FormSurvey(survey_name)

    patients = Patient.objects.values_list("id_patient", "name", "surname")
    survey = form.get_survey()
    survey_description = Survey.objects.get(pk=survey_name).description
    context = {"survey_name": survey_name, "survey_description": survey_description, "form": form, "survey": survey, "patients": patients}
    return render(request, "surveys/survey_filling_template.html", context)


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


def export_surveys_single_person_view(request):
    if request.method == "POST":
        # id_patient = request.POST.get('id_patient')
        # patient = Patient.objects.get(pk=id_patient)
        # survey_name = request.POST.get('survey')
        # survey = Survey.objects.get(pk=survey_name)
        # date = request.POST.get('filling_date')
        form = FormExportSurveysSinglePerson(request.POST)

        if form.is_valid():
            # try:
            form.process()
            # except:
                # return render(request, "surveys/export_error.html")

            # print(form.cleaned_data["patient"])
            # id_patient = form.cleaned_data["patient"]
            # patient = Patient.objects.get(pk=id_patient)
            # surveys_name = form.cleaned_data["surveys"]
            # surveys = []
            # for survey_name in surveys_name:
            #     surveys.append(Survey.objects.get(pk=surveys_name))
            # date_from = form.cleaned_data["date_from"]
            # if form.cleaned_data["date_to"]:
            #     date_to = form.cleaned_data["date_to"]
            # # if self.validate_form_export_single_survey_view(patient=patient, survey=survey, date=date):
            # return export_to_xls_patient_surveys(request=request, patient=patient, survey=survey,  date_from=date_from, date_to=date_to)
    else:
        # patients = Patient.objects.values_list("id_patient", "name", "surname")
        # surveys = Survey.objects.all()
        # context = {"patients": patients, "surveys": surveys}
        # return render(request, "surveys/export_single_survey.html", context)
        form = FormExportSurveysSinglePerson()

    context = {"form": form}
    return render(request, "surveys/export_surveys_single_person_template.html", context)


class ListSurveyCBV(ListView):
    model = Survey
    paginate_by = 5
    template_name = "surveys/survey_list_template.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["surveys"] = Survey.objects.all()
        return context
