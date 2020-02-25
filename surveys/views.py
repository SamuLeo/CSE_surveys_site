import xlwt

from django.shortcuts import render, HttpResponse
from django.views.generic.list import ListView

from .form_survey import FormSurvey, FormExportSingleSurvey
from .models import Patient, Caregiver, Answer, Survey,Patient_Survey_Question_Answer,Caregiver_Survey_Question_Answer

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

def extractAnswerFromForm(self, request, survey_name):
    pass

def export_survey_home(request):
    return render(request, "surveys/export_survey_home.html")

# def validate_form_export_single_survey_view(id_patient, survey, date):
#
#     try:
#         Patient_Survey_Question_Answer.objects.get()


def export_xls_patient_survey_date(request, patient, survey, date):

    try:
        raw_rows = Patient_Survey_Question_Answer.objects.filter(patient=patient, date=date,survey=survey).values_list('patient', 'date', 'survey', 'question', 'answer', )
        rows = []
        for raw_patient, raw_date, raw_survey, raw_question, raw_answer in raw_rows:
            print(raw_date)
            print(raw_survey)
            print(raw_patient)
            print(raw_question)
            print(raw_answer)
            question = Question.objects.get(pk=raw_question).__str__()

            patient = Patient.objects.get(pk=raw_patient).__str__()
            print(patient)
            print(question)
            answer = Answer.objects.get(pk=raw_answer).__str__()
            print(answer)
            rows.append((patient,date,survey,question,answer))
            print(rows)
    except:
        # return HttpResponse("<h1>Non è possibile esportare il questionario</h1>")
        pass

    print(rows)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="questionario.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Questionario')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['ID Paziente', 'Data', 'Questionario', 'Domanda', 'Risposta', ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


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
            return export_xls_patient_survey_date(request=request, patient=patient, survey=survey, date=date)
    else:
        # patients = Patient.objects.values_list("id_patient", "name", "surname")
        # surveys = Survey.objects.all()
        # context = {"patients": patients, "surveys": surveys}
        # return render(request, "surveys/export_single_survey.html", context)
        form = FormExportSingleSurvey()

    context = {"form": form}
    return render(request, "surveys/prova.html", context)


class ListSurveyCBV(ListView):
    model = Survey
    paginate_by = 5
    template_name = "surveys/survey_list_template.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["surveys"] = Survey.objects.all()
        return context
