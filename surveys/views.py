from django.shortcuts import render, HttpResponse
from django.views.generic.list import ListView

from .form_survey import FormSurvey
from .models import Patient, Caregiver, Answer, Survey,Patient_Survey_Question_Answer,Caregiver_Survey_Question_Answer

# Create your views here.


def fillSurvey(request, survey_name):
    if request.method == "POST":
        form = FormSurvey(request.POST)
        if form.is_valid():
            print("Il Form è Valido!")
            survey = Survey.objects.get(pk=survey_name)
            id_patient = request.POST.get('id_patient')
            patient = Patient.objects.get(pk=id_patient)
            print(id_patient)
            date = request.POST.get('filling_date')
            print(date)

            for question in survey.questions.all():
                print(question)
                b = (str(question.type) is "Instructions in compound question")
                print(type(question.type.__str__()))
                print(type("Instructions in compound question"))
                print(question.type)

                print("Instructions in compound question")
                print(b)
                if question.type.__str__() == "Instructions in compound question":
                    print("in da zone")
                    continue

                id_answer = request.POST.get(question.__str__())
                print(str(id_answer))
                answer = Answer.objects.get(pk=id_answer)
                patient_answer = Patient_Survey_Question_Answer(
                                    patient=patient,
                                    survey=survey,
                                    question=question,
                                    answer=answer,
                                    date=date)
                patient_answer.save()
            # new_post = form.save()
            # print("new_post: ", new_post)
            return render(request, "surveys/survey_completed_success.html")
    else:
        form = FormSurvey(survey_name=survey_name).get_survey()
        survey_description = Survey.objects.get(pk=survey_name).description
    context = {"survey_name": survey_name, "survey_description": survey_description, "form": form}
    return render(request, "surveys/survey_template.html", context)

def extractAnswerFromForm(self, request, survey_name):
    pass

class ListSurveyCBV(ListView):
    model = Survey
    paginate_by = 5
    template_name = "surveys/survey_list_template.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["surveys"] = Survey.objects.all()
        return context
