from django import forms
from django.core.exceptions import ValidationError

from .models import Survey,Question,Answer,QuestionType,Patient, Patient_Survey_Question_Answer


class FormExportSingleSurvey(forms.Form):

    def get_surveys_names():
        surveys_names_list = []
        for survey_name in Survey.objects.all():
            surveys_names_list.append((survey_name,survey_name))
        return surveys_names_list

    def get_patients():
        patients_list = []
        for patient in Patient.objects.all():
            patients_list.append((patient.id_patient, patient.id_patient))
        return patients_list

    patient = forms.ChoiceField(
                        choices = get_patients(),
                        label="Numero Identificativo del Paziente:",
                        widget = forms.Select(attrs=  {"class": "form-control  col-4",
                                    "name":"patient",
                                    "id":"patient"}),
                        required=True)

    survey = forms.ChoiceField(
                        choices = get_surveys_names(),
                        label="Nome del questionario:",
                        widget=forms.Select(attrs=  {"class": "form-control col-4",
                                    "name":"survey",
                                    "id":"survey"}),
                        required=True)

    date = forms.DateField(
                        label = "Data di Compilazione:",
                        widget = forms.widgets.DateInput(attrs={"class": "form-control col-4",
                                                            "type": "date",
                                                            }),
                        required=True)


    def clean_date(self):

        date = self.cleaned_data['date']
        id_patient = self.cleaned_data['patient']
        patient = Patient.objects.get(pk=id_patient)
        survey_name = self.cleaned_data['survey']
        survey = Survey.objects.get(pk=survey_name)

        filling_dates_list = []
        patient_surveys = Patient_Survey_Question_Answer.objects.filter(patient=patient, survey=survey, date=date)

#       checking for empty QuerySet
        if not patient_surveys:
            raise ValidationError(f"Non è stato compilato il questionario {survey} dal paziente {patient} in data {date}")

        return date

    # class Meta:
    #     model = Patient_Survey_Question_Answer
    #     fields = ["patient", "survey", "date"]


class FormExportPatientSurveys(forms.Form):

    def get_surveys_names():
        surveys_names_list = []
        for survey_name in Survey.objects.all():
            surveys_names_list.append((survey_name,survey_name))
        return surveys_names_list

    def get_patients():
        patients_list = []
        for patient in Patient.objects.all():
            patients_list.append((patient.id_patient, patient.id_patient))
        return patients_list

    patient = forms.ChoiceField(
                        choices = get_patients(),
                        label="Numero Identificativo del Paziente:",
                        widget = forms.Select(attrs=  {"class": "form-control  col-4",
                                    "name":"patient",
                                    "id":"patient"}),
                        required=True)

    survey = forms.ChoiceField(
                        choices = get_surveys_names(),
                        label="Nome del questionario:",
                        widget=forms.Select(attrs=  {"class": "form-control col-4",
                                    "name":"survey",
                                    "id":"survey"}),
                        required=True)


class FormSurvey(forms.Form):
    #
    # id_paziente = forms.IntegerField()
    # data = forms.DateField()

    def __init__(self, survey_name):
        super().__init__(self);
        self.survey_name=survey_name


    def get_answers_list_for_question(self, question):
        answers_list = []
        for answer in question.answers.all():
            answers_list.append((answer.id, answer.answer_sequence_number, answer.value))
        return answers_list


    def get_survey(self):
        form_survey = {}
        survey = Survey.objects.get(pk=self.survey_name)
        for question in survey.questions.all():
        # caso di domanda composta da gestire qua
            answers_list = self.get_answers_list_for_question(question)
        # if "Single Choice" in question.type:
            form_survey[question.__str__()] = answers_list
        return form_survey

    # def validate(self, request):
    #     """Check if the specified patient id exist."""
    #     super().validate(value)


    # def get_survey(self):
    #     form_survey = []
    #     survey = Survey.objects.get(pk=self.survey_name)
    #     for q in survey.questions.all():
    #     # caso di domanda composta da gestire qua
    #         print(q.__str__())
    #         answers_list = self.get_answers_list_for_question(q)
    #         print(answers_list)
    #     # if "Single Choice" in question.type:
    #         question = forms.ChoiceField(
    #                             choices=answers_list,
    #                             widget=forms.RadioSelect(attrs={
    #                                                         "id": q.id,
    #                                                         "class": "form-check-input",
    #                                                         "type": "radio",
    #                                                         "label": q.__str__()}))
    #         form_survey.append(question)
    #     return form_survey
