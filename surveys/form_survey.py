from django import forms
from django.core.exceptions import ValidationError

from .models import Survey,Question,Answer,QuestionType,Patient, Patient_Survey_Question_Answer
from .export_to_xls_module import export_to_xls_patient_surveys


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



class FormExportSurveysSinglePerson(forms.Form):

    def get_surveys_names():
        surveys_names_list = []
        for survey_name in Survey.objects.all():
            surveys_names_list.append((survey_name,survey_name))
        return surveys_names_list

    def get_patients():
        patients_list = []
        for patient in Patient.objects.all():
            patients_list.append((patient.id_patient, patient.__str__()))
        return patients_list



    patient = forms.ChoiceField(
                        choices = get_patients(),
                        label="Numero Identificativo del Paziente:",
                        widget = forms.Select(attrs=  {"class": "form-control  col-4",
                                    "name":"patient",
                                    "id":"patient"}),
                        required=True)

    surveys = forms.MultipleChoiceField(
                        choices = get_surveys_names(),
                        label = "Nomi dei questionari da esportare:",
                        widget = forms.CheckboxSelectMultiple(attrs = {"multiple class": "form-control col-4",
                                                                    "id": "surveys",
                                                                    "name":"surveys",}),
                        required=True)

    date_from = forms.DateField(
                        label = "Dalla Data:",
                        widget = forms.widgets.DateInput(attrs={"class": "form-control col-4",
                                                            "type": "date",
                                                            }),
                        required=True)

    date_to = forms.DateField(
                        label = "Alla Data: (Lasciare vuoto in caso si è interessati ad una data singola)",
                        widget = forms.widgets.DateInput(attrs={"class": "form-control col-4",
                                                            "type": "date",
                                                            }),
                        required=False)

    def clean(self):
        cleaned_data = super(FormExportSurveysSinglePerson, self).clean()
        surveys_name = cleaned_data['surveys']
        date_from = cleaned_data['date_from']
        date_to = cleaned_data['date_to']
        id_patient = cleaned_data['patient']
        patient = Patient.objects.get(pk=id_patient)

        if date_to is not None and date_from > date_to:
            raise ValidationError("Specificare un range di date valido")

        for survey_name in surveys_name:
            survey = Survey.objects.get(pk=survey_name)
            patient_surveys = Patient_Survey_Question_Answer.objects.filter(patient=patient, survey=survey)
            for patient_survey in patient_surveys:
                if date_to is None:
                    if patient_survey.date == date_from:
                        return cleaned_data
                elif patient_survey.date > date_from and patient_survey.date < date_to:
                    return cleaned_data
# if the code arrive here the survey is not in the DB
        if date_to is None:
            raise ValidationError(f"Non sono stati compilati questionari dal paziente {patient} in data {date_from}")
        else:
            raise ValidationError(f"Non sono stati compilati questionari dal paziente {patient} dalla data {date_from} alla data {date_to}")


    def process(self):
        id_patient = self.cleaned_data["patient"]
        patient = Patient.objects.get(pk=id_patient)
        surveys_name = self.cleaned_data["surveys"]
        survey_list = []
        for survey_name in surveys_name:
            survey_list.append(Survey.objects.get(pk=survey_name))
        date_from = self.cleaned_data["date_from"]
        # if self.cleaned_data["date_to"]:
        date_to = self.cleaned_data["date_to"]
        return export_to_xls_patient_surveys(patient=patient, surveys_list=survey_list,  date_from=date_from, date_to=date_to)
        # else:
            # return export_to_xls_patient_surveys(patient=patient, surveys_list=survey_list,  date_from=date_from)
        # if self.validate_form_export_single_survey_view(patient=patient, survey=survey, date=date):


    # def clean_date_from(self):

        # date_from = self.cleaned_data['date_from']
        # date_to = self.cleaned_data['date_to']
        # id_patient = self.cleaned_data['patient']
        # patient = Patient.objects.get(pk=id_patient)
        # surveys_name = self.cleaned_data['surveys']
        #
        # if date_from > date_to:
        #     raise ValidationError("Specificare un range di date valido")
        #
        # for survey_name in surveys_name:
        #     survey = Survey.objects.get(pk=surveys_name)
        #     patient_surveys = Patient_Survey_Question_Answer.objects.filter(patient=patient, survey=survey)
        #     for patient_survey in patient_surveys:
        #         if date_to is None:
        #             if patient_survey.date is date_from:
        #                 return date_from
        #         elif patient_survey.date > date_from and patient_survey.date < date_to:
        #             return date_from
        #
        # if date_to is None:
        #     raise ValidationError(f"Non sono stati compilati questionari dal paziente {patient} in data {date_from}")
        # else:
        #     raise ValidationError(f"Non sono stati compilati questionari dal paziente {patient} dalla data {date_from} alla data {date_to}")




class FormExportSurveys(forms.Form):

    def get_surveys_names():
        surveys_names_list = []
        for survey_name in Survey.objects.all():
            surveys_names_list.append((survey_name,survey_name))
        return surveys_names_list

    def get_patients():
        patients_list = []
        for patient in Patient.objects.all():
            patients_list.append((patient.id_patient, patient.__str__()))
        return patients_list



    patient_filter = forms.ChoiceField(
                                choices=[(1,"Solo Maschi"), (2,"Solo Femmine"), (3,"Tutti")],
                                label="Gruppo di persone di cui si vuole fare l'esportazione:",
                                widget=forms.RadioSelect(attrs={
                                                            "class": "form-check-input pb-5",
                                                            "type": "radio",
                                                            "required": "required"}),
                                required=True)

    surveys = forms.MultipleChoiceField(
                        choices = get_surveys_names(),
                        label = "Nomi dei questionari da esportare:",
                        widget = forms.CheckboxSelectMultiple(attrs = {"multiple class": "form-control col-4",
                                                                    "id": "surveys",
                                                                    "name":"surveys",
                                                                    "required": "required",}),
                        required=True)

    date_from = forms.DateField(
                        label = "Dalla Data:",
                        widget = forms.widgets.DateInput(attrs={"class": "form-control col-4",
                                                            "type": "date",
                                                            "required": "required"
                                                            }),
                        required=True)

    date_to = forms.DateField(
                        label = "Alla Data: (Lasciare vuoto in caso si è interessati ad una data singola)",
                        widget = forms.widgets.DateInput(attrs={"class": "form-control col-4",
                                                            "type": "date",
                                                            }),
                        required=False)


    def get_filtered_patients_list(patient_filter):
        patients_list = []
        if patient_filter == 1:
            for patient in Patient.objects.get(gender=GenderType.objects.get(pk="M")):
                patients_list.append(patient)
        elif patient_filter == 2:
            for patient in Patient.objects.get(gender=GenderType.objects.get(pk="F")):
                patients_list.append(patient)
        else:
            patients_list = Patient.objects.all()

        return patients_list


    def clean(self):
        cleaned_data = super(FormExportSurveys, self).clean()

        if not cleaned_data['surveys']:
            raise ValidationError("Selezionare i questionari da esportare")
        surveys_name = cleaned_data['surveys']
        date_from = cleaned_data['date_from']
        date_to = cleaned_data['date_to']
        patient_filter = cleaned_data['patient_filter']

        patients_list = self.get_filtered_patients_list(patient_filter=patient_filter)

        if date_to is not None and date_from > date_to:
            raise ValidationError("Specificare un range di date valido")

        for survey_name in surveys_name:
            survey = Survey.objects.get(pk=survey_name)
            for patient in patients_list:
                patient_surveys = Patient_Survey_Question_Answer.objects.filter(patient=patient, survey=survey)
                for patient_survey in patient_surveys:
                    if date_to is None:
                        if patient_survey.date == date_from:
                            return cleaned_data
                    elif patient_survey.date > date_from and patient_survey.date < date_to:
                        return cleaned_data
# if the code arrive here the survey is not in the DB
        if date_to is None:
            raise ValidationError(f"Non sono stati compilati questionari dal paziente {patient} in data {date_from}")
        else:
            raise ValidationError(f"Non sono stati compilati questionari dal paziente {patient} dalla data {date_from} alla data {date_to}")


    def process(self):
        id_patient = self.cleaned_data["patient"]
        # export_to_xls_patient_surveys expect a list, [] are necessary
        patient = [Patient.objects.get(pk=id_patient)]
        surveys_name = self.cleaned_data["surveys"]
        survey_list = []
        for survey_name in surveys_name:
            survey_list.append(Survey.objects.get(pk=survey_name))
        date_from = self.cleaned_data["date_from"]
        # if self.cleaned_data["date_to"]:
        date_to = self.cleaned_data["date_to"]
        return export_to_xls_patient_surveys(patients_list=patient, surveys_list=survey_list,  date_from=date_from, date_to=date_to)





class FormSurvey(forms.Form):

    def __init__(self, survey_name, *args, **kwargs):
        super(FormSurvey, self).__init__(*args, **kwargs);
        self.survey_name=survey_name

    def get_patients():
        patients_list = []
        for patient in Patient.objects.all():
            patients_list.append((patient.id_patient, patient.__str__()))
        return patients_list



    patient = forms.ChoiceField(
                        choices = get_patients(),
                        label="Numero Identificativo del Paziente:",
                        widget = forms.Select(attrs=  {"class": "form-control  col-4",
                                    "name":"patient",
                                    "id":"patient"}),
                        required=True)

    date = forms.DateField(
                        label = "Data di compilazione:",
                        widget = forms.widgets.DateInput(attrs={"class": "form-control col-4",
                                                            "type": "date",
                                                            }),
                        required=True)


    def get_answers_list_for_question(self, question):
        answers_list = []
        for answer in question.answers.all():
            answers_list.append((answer.id, answer.answer_sequence_number, answer.value))
        return answers_list


    def get_survey(self):
        # self.survey_name = survey_name
        form_survey = {}
        survey = Survey.objects.get(pk=self.survey_name)
        for question in survey.questions.all():
        # caso di domanda composta da gestire qua
            answers_list = self.get_answers_list_for_question(question)
            key = (question.__str__(), question.type.__str__())
        # if "Single Choice" in question.type:
            form_survey[key] = answers_list
        return form_survey


    def clean(self):

        cleaned_data = super(FormSurvey, self).clean()
        id_patient = cleaned_data['patient']
        patient = Patient.objects.get(pk=id_patient)
        survey = Survey.objects.get(pk=self.survey_name)

        if (patient.gender.__str__() == "M" and survey.__str__() == "Psychological Distress Inventory - PDI Versione Femminile") or (patient.gender.__str__() == "F" and survey.__str__() == "Psychological Distress Inventory - PDI Versione Maschile"):
            raise ValidationError("Scegliere la versione del questionario(PDI) adeguata al genere del paziente")
            return id_patient

        date = cleaned_data['date']
        patient_surveys = Patient_Survey_Question_Answer.objects.filter(patient=patient, survey=survey, date=date)

#       checking for empty QuerySet
        if patient_surveys:
            raise ValidationError(f"Il questionario {survey} è stato già compilato dal paziente {patient} in data {date}")

        return cleaned_data



    def process(self, request):
        patient_answers = []

        id_patient = self.cleaned_data['patient']
        patient = Patient.objects.get(pk=id_patient)
        survey = Survey.objects.get(pk=self.survey_name)
        date = self.cleaned_data['date']

        for question in survey.questions.all():
            if question.type.__str__() == "Instructions in compound question":
                continue
            elif question.type.__str__() == "Single Choice":
                id_answer = request.POST.get(question.__str__())
                answer = Answer.objects.get(pk=id_answer)
                patient_answer = Patient_Survey_Question_Answer(
                                    patient=patient,
                                    survey=survey,
                                    question=question,
                                    answer=answer,
                                    date=date)
                patient_answers.append(patient_answer)
            elif question.type.__str__() == "Multiple Choice":
                ids_answers = request.POST.get(question.__str__())
                for id_answer in ids_answers:
                    answer = Answer.objects.get(pk=id_answer)
                    patient_answer = Patient_Survey_Question_Answer(
                                        patient=patient,
                                        survey=survey,
                                        question=question,
                                        answer=answer,
                                        date=date)
                    patient_answers.append(patient_answer)
            elif question.type.__str__() == "Alphanumerical Input":
                answer_value = request.POST.get(question.__str__())
                Answer(question=question, answer_sequence_number=1, value=answer_value).save()
                answer = Answer.objects.get(question=question, value=answer_value)
                patient_answer = Patient_Survey_Question_Answer(
                                        patient=patient,
                                        survey=survey,
                                        question=question,
                                        answer=answer,
                                        date=date)
                patient_answers.append(patient_answer)
            elif question.type.__str__() == "Range Input [0-10]":
                # get the value of the answer, thanks to that and the question it is possible to retrieve the Answer from DB(necessary for Patient_Survey_Question_Answer)
                answer_value = request.POST.get(question.__str__())
                answer = Answer.objects.get(question=question, value=answer_value)
                patient_answer = Patient_Survey_Question_Answer(
                                        patient=patient,
                                        survey=survey,
                                        question=question,
                                        answer=answer,
                                        date=date)
                patient_answers.append(patient_answer)
    #patient_answers creates a transaction: either all answers are written or nothing, to prevent DB corruption in case of error
        for patient_answer in patient_answers:
            patient_answer.save()


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
