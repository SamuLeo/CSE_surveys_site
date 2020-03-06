from django import forms
from django.core.exceptions import ValidationError

from .models import GenderType, Survey,Question,Answer,QuestionType,Patient, Patient_Survey_Question_Answer, Caregiver, Caregiver_Survey_Question_Answer
from .export_to_xls_module import export_to_xls_surveys


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



class FormExportSurveysSinglePatient(forms.Form):

    def get_surveys_names():
        surveys_names_list = []
        for survey in Survey.objects.all():
            if survey.patient_survey:
                surveys_names_list.append((survey.__str__(),survey.__str__()))
        return surveys_names_list

    def get_patients():
        patients_list = []
        for patient in Patient.objects.all():
            patients_list.append((patient.id_patient, patient.__str__()))
        return patients_list



    patient = forms.ChoiceField(
                        choices = get_patients(),
                        label="Paziente:",
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
        cleaned_data = super(FormExportSurveysSinglePatient, self).clean()
        surveys_name = cleaned_data.get('surveys')
        if surveys_name is None:
            raise ValidationError("Selezionare i questionari da esportare")
        date_from = cleaned_data.get('date_from')
        if date_from is None:
            raise ValidationError("Selezionare la data")
        date_to = cleaned_data.get('date_to')
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
        patient = [Patient.objects.get(pk=id_patient)]
        surveys_name = self.cleaned_data["surveys"]
        survey_list = []
        for survey_name in surveys_name:
            survey_list.append(Survey.objects.get(pk=survey_name))
        date_from = self.cleaned_data["date_from"]
        # if self.cleaned_data["date_to"]:
        date_to = self.cleaned_data["date_to"]
        return export_to_xls_surveys(people_list=patient, surveys_list=survey_list,  date_from=date_from, date_to=date_to)
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





class FormExportSurveysSingleCaregiver(forms.Form):

    def get_surveys_names():
        surveys_names_list = []
        for survey in Survey.objects.all():
            if not survey.patient_survey:
                surveys_names_list.append((survey.__str__(),survey.__str__()))
        return surveys_names_list

    def get_caregivers():
        caregivers_list = []
        for caregiver in Caregiver.objects.all():
            caregivers_list.append((caregiver.id, caregiver.__str__()))
        return caregivers_list



    caregiver = forms.ChoiceField(
                        choices = get_caregivers(),
                        label="Caregiver:",
                        widget = forms.Select(attrs=  {"class": "form-control  col-5",
                                    "name":"caregiver",
                                    "id":"caregiver"}),
                        required=True)

    surveys = forms.MultipleChoiceField(
                        choices = get_surveys_names(),
                        label = "Nomi dei questionari da esportare:",
                        widget = forms.CheckboxSelectMultiple(attrs = {"multiple class": "form-control col-5",
                                                                    "id": "surveys",
                                                                    "name":"surveys",}),
                        required=True)

    date_from = forms.DateField(
                        label = "Dalla Data:",
                        widget = forms.widgets.DateInput(attrs={"class": "form-control col-5",
                                                            "type": "date",
                                                            }),
                        required=True)

    date_to = forms.DateField(
                        label = "Alla Data: (Lasciare vuoto in caso si è interessati ad una data singola)",
                        widget = forms.widgets.DateInput(attrs={"class": "form-control col-5",
                                                            "type": "date",
                                                            }),
                        required=False)

    def clean(self):
        cleaned_data = super(FormExportSurveysSingleCaregiver, self).clean()
        surveys_name = cleaned_data.get('surveys')
        if surveys_name is None:
            raise ValidationError("Selezionare i questionari da esportare")
        date_from = cleaned_data.get('date_from')
        if date_from is None:
            raise ValidationError("Selezionare la data")
        date_to = cleaned_data.get('date_to')
        id_caregiver = cleaned_data.get('caregiver')
        caregiver = Caregiver.objects.get(pk=id_caregiver)

        if date_to is not None and date_from > date_to:
            raise ValidationError("Specificare un range di date valido")

        for survey_name in surveys_name:
            survey = Survey.objects.get(pk=survey_name)
            caregiver_surveys = Caregiver_Survey_Question_Answer.objects.filter(caregiver=caregiver, survey=survey)
            for caregiver_survey in caregiver_surveys:
                if date_to is None:
                    if caregiver_survey.date == date_from:
                        return cleaned_data
                elif caregiver_survey.date > date_from and caregiver_survey.date < date_to:
                    return cleaned_data
# if the code arrive here the survey is not in the DB
        if date_to is None:
            raise ValidationError(f"Non sono stati compilati questionari da {caregiver} in data {date_from}")
        else:
            raise ValidationError(f"Non sono stati compilati questionari da {caregiver} dalla data {date_from} alla data {date_to}")


    def process(self):
        id_caregiver = self.cleaned_data["caregiver"]
        caregiver = [Caregiver.objects.get(pk=id_caregiver)]
        surveys_name = self.cleaned_data["surveys"]
        survey_list = []
        for survey_name in surveys_name:
            survey_list.append(Survey.objects.get(pk=survey_name))
        date_from = self.cleaned_data["date_from"]
        # if self.cleaned_data["date_to"]:
        date_to = self.cleaned_data["date_to"]
        return export_to_xls_surveys(people_list=caregiver, surveys_list=survey_list,  date_from=date_from, date_to=date_to)






class FormExportSurveysPatients(forms.Form):

    def get_surveys_names():
        surveys_names_list = []
        for survey in Survey.objects.all():
            if survey.patient_survey:
                surveys_names_list.append((survey.__str__(),survey.__str__()))
        return surveys_names_list

    def get_patients():
        patients_list = []
        for patient in Patient.objects.all():
            patients_list.append((patient.id_patient, patient.__str__()))
        return patients_list



    patient_filter = forms.ChoiceField(
                                choices=[(1,"Solo Maschi"), (2,"Solo Femmine"), (3,"Tutti")],
                                label="Gruppo di pazienti di cui si vuole fare l'esportazione:",
                                widget=forms.RadioSelect(attrs={
                                                            "class": "form-check-input pb-5",
                                                            "type": "radio",
                                                            "required": "true"}),
                                required=True)

    surveys = forms.MultipleChoiceField(
                        choices = get_surveys_names(),
                        label = "Nomi dei questionari da esportare:",
                        widget = forms.CheckboxSelectMultiple(attrs = {"multiple class": "form-control col-4",
                                                                    "id": "surveys",
                                                                    "name":"surveys",
                                                                    "required": "true",}),
                        required=True)

    date_from = forms.DateField(
                        label = "Dalla Data:",
                        widget = forms.widgets.DateInput(attrs={"class": "form-control col-4",
                                                            "type": "date",
                                                            "required": "true"
                                                            }),
                        required=True)

    date_to = forms.DateField(
                        label = "Alla Data: (Lasciare vuoto in caso si è interessati ad una data singola)",
                        widget = forms.widgets.DateInput(attrs={"class": "form-control col-4",
                                                            "type": "date",
                                                            }),
                        required=False)


    def get_filtered_patients_list(self, patient_filter):
        patients_list = []
        if patient_filter == str(1):
            patients_list = Patient.objects.filter(gender=GenderType.objects.get(pk="M"))
        elif patient_filter == str(2):
            patients_list = Patient.objects.filter(gender=GenderType.objects.get(pk="F"))
        else:
            patients_list = Patient.objects.all()
        return patients_list


    def clean(self):
        cleaned_data = super(FormExportSurveysPatients, self).clean()
        surveys_name = cleaned_data.get('surveys')
        if surveys_name is None:
            raise ValidationError("Selezionare i questionari da esportare")
        date_from = cleaned_data.get('date_from')
        if date_from is None:
            raise ValidationError("Selezionare la data")
        date_to = cleaned_data.get('date_to')
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
            raise ValidationError(f"Non sono stati compilati questionari da pazienti del gruppo richiesto in data {date_from}")
        else:
            raise ValidationError(f"Non sono stati compilati questionari da pazienti del gruppo richiesto dalla data {date_from} alla data {date_to}")


    def process(self):
        # export_to_xls_patient_surveys expect a list, [] are necessary
        patient_filter = self.cleaned_data['patient_filter']
        patients_list = self.get_filtered_patients_list(patient_filter=patient_filter)
        surveys_name = self.cleaned_data["surveys"]
        survey_list = []
        for survey_name in surveys_name:
            survey_list.append(Survey.objects.get(pk=survey_name))
        date_from = self.cleaned_data["date_from"]
        # if self.cleaned_data["date_to"]:
        date_to = self.cleaned_data["date_to"]
        return export_to_xls_surveys(people_list=patients_list, surveys_list=survey_list,  date_from=date_from, date_to=date_to)


class FormExportSurveysCaregivers(forms.Form):

    def get_surveys_names():
        surveys_names_list = []
        for survey in Survey.objects.all():
            if not survey.patient_survey:
                surveys_names_list.append((survey.__str__(),survey.__str__()))
        return surveys_names_list

    def get_caregivers():
        caregivers_list = []
        for caregiver in Caregiver.objects.all():
            caregivers_list.append((caregiver.id_caregiver, caregiver.__str__()))
        return caregivers_list



    caregiver_filter = forms.ChoiceField(
                                choices=[(1,"Solo Maschi"), (2,"Solo Femmine"), (3,"Tutti")],
                                label="Gruppo di caregivers di cui si vuole fare l'esportazione:",
                                widget=forms.RadioSelect(attrs={
                                                            "class": "form-check-input pb-5",
                                                            "type": "radio",
                                                            "required": "true"}),
                                required=True)

    surveys = forms.MultipleChoiceField(
                        choices = get_surveys_names(),
                        label = "Nomi dei questionari da esportare:",
                        widget = forms.CheckboxSelectMultiple(attrs = {"multiple class": "form-control col-4",
                                                                    "id": "surveys",
                                                                    "name":"surveys",
                                                                    "required": "true",}),
                        required=True)

    date_from = forms.DateField(
                        label = "Dalla Data:",
                        widget = forms.widgets.DateInput(attrs={"class": "form-control col-4",
                                                            "type": "date",
                                                            "required": "true"
                                                            }),
                        required=True)

    date_to = forms.DateField(
                        label = "Alla Data: (Lasciare vuoto in caso si è interessati ad una data singola)",
                        widget = forms.widgets.DateInput(attrs={"class": "form-control col-4",
                                                            "type": "date",
                                                            }),
                        required=False)


    def get_filtered_caregivers_list(self, caregiver_filter):
        caregivers_list = []
        if caregiver_filter == str(1):
            caregivers_list = Caregiver.objects.filter(gender=GenderType.objects.get(pk="M"))
        elif caregiver_filter== str(2):
            caregivers_list = Caregiver.objects.filter(gender=GenderType.objects.get(pk="F"))
        else:
            caregivers_list = Caregiver.objects.all()
        return caregivers_list


    def clean(self):
        cleaned_data = super(FormExportSurveysCaregivers, self).clean()
        surveys_name = cleaned_data.get('surveys')
        if surveys_name is None:
            raise ValidationError("Selezionare i questionari da esportare")
        date_from = cleaned_data.get('date_from')
        if date_from is None:
            raise ValidationError("Selezionare la data")
        date_to = cleaned_data.get('date_to')
        caregiver_filter = cleaned_data['caregiver_filter']
        caregivers_list = self.get_filtered_caregivers_list(caregiver_filter=caregiver_filter)

        if date_to is not None and date_from > date_to:
            raise ValidationError("Specificare un range di date valido")

        for survey_name in surveys_name:
            survey = Survey.objects.get(pk=survey_name)
            for caregiver in caregivers_list:
                caregiver_surveys = Caregiver_Survey_Question_Answer.objects.filter(caregiver=caregiver, survey=survey)
                for caregiver_survey in caregiver_surveys:
                    if date_to is None:
                        if caregiver_survey.date == date_from:
                            return cleaned_data
                    elif caregiver_survey.date > date_from and caregiver_survey.date < date_to:
                        return cleaned_data
# if the code arrive here the survey is not in the DB
        if date_to is None:
            raise ValidationError(f"Non sono stati compilati questionari da alcun caregiver del gruppo richiesto in data {date_from}")
        else:
            raise ValidationError(f"Non sono stati compilati questionari da alcun caregiver del gruppo richiesto dalla data {date_from} alla data {date_to}")


    def process(self):
        # export_to_xls_caregiver_surveys expect a list, [] are necessary
        caregiver_filter = self.cleaned_data['caregiver_filter']
        caregivers_list = self.get_filtered_caregivers_list(caregiver_filter=caregiver_filter)
        surveys_name = self.cleaned_data["surveys"]
        survey_list = []
        for survey_name in surveys_name:
            survey_list.append(Survey.objects.get(pk=survey_name))
        date_from = self.cleaned_data["date_from"]
        # if self.cleaned_data["date_to"]:
        date_to = self.cleaned_data["date_to"]
        return export_to_xls_surveys(people_list=caregivers_list, surveys_list=survey_list,  date_from=date_from, date_to=date_to)



class FormSurveyPatient(forms.Form):

    def __init__(self, survey_name, *args, **kwargs):
        super(FormSurveyPatient, self).__init__(*args, **kwargs);
        self.survey_name=survey_name

    def get_patients():
        patients_list = []
        for patient in Patient.objects.all():
            patients_list.append((patient.id_patient, patient.__str__()))
        return patients_list


    patient = forms.ChoiceField(
                        choices = get_patients(),
                        label="Paziente:",
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

        cleaned_data = super(FormSurveyPatient, self).clean()
        id_patient = cleaned_data['patient']
        patient = Patient.objects.get(pk=id_patient)
        date = cleaned_data['date']
        survey = Survey.objects.get(pk=self.survey_name)
        if (patient.gender.__str__() == "M" and survey.__str__() == "Psychological Distress Inventory - PDI Versione Femminile") or (patient.gender.__str__() == "F" and survey.__str__() == "Psychological Distress Inventory - PDI Versione Maschile"):
            raise ValidationError("Scegliere la versione del questionario(PDI) adeguata al genere del paziente")
        patient_surveys = Patient_Survey_Question_Answer.objects.filter(patient=patient, survey=survey, date=date)
#       checking for empty QuerySet, if not empty the survey ha already been filled
        if patient_surveys:
            raise ValidationError(f"Il questionario {survey} è stato già compilato dal paziente {patient} in data {date}")
        return cleaned_data


    def get_patient_answers_from_form(self, request, patient, survey, date):
        print(request.POST)
        patient_answers = []
        for question in survey.questions.all():
            if question.type.__str__() == "Instructions in compound question":
                continue
            elif question.type.__str__() == "Single Choice":
                id_answer = request.POST.get(question.__str__())
                answer = Answer.objects.get(pk=id_answer)
                patient_answer = Patient_Survey_Question_Answer(patient=patient, survey=survey, question=question, answer=answer, date=date)
                patient_answers.append(patient_answer)
            elif question.type.__str__() == "Multiple Choice":
                ids_answers = request.POST.getlist(question.__str__())
                if not ids_answers:
                    if not Answer.objects.all().filter(question=question, value="Nessuno"):
                        Answer(question=question, value="Nessuno").save()
                    answer = Answer.objects.get(question=question, value="Nessuno")
                    patient_answer = Patient_Survey_Question_Answer(patient=patient, survey=survey, question=question, answer=answer, date=date)
                    patient_answers.append(patient_answer)
                else:
                    for id_answer in ids_answers:
                        answer = Answer.objects.get(pk=id_answer)
                        patient_answer = Patient_Survey_Question_Answer(patient=patient, survey=survey, question=question, answer=answer, date=date)
                        patient_answers.append(patient_answer)
            elif question.type.__str__() == "Alphanumerical Input":
                answer_value = request.POST.get(question.__str__())
                # this check allow to use past answers to be used instead of adding them again(memory saving)
                if not Answer.objects.filter(question=question, value=answer_value):
                    Answer(question=question, value=answer_value).save()
                answer = Answer.objects.get(question=question, value=answer_value)
                patient_answer = Patient_Survey_Question_Answer(patient=patient, survey=survey, question=question, answer=answer, date=date)
                patient_answers.append(patient_answer)
            elif question.type.__str__() == "Range Input [0-10]":
                # get the value of the answer, thanks to that and the question it is possible to retrieve the Answer from DB(necessary for Patient_Survey_Question_Answer)
                answer_value = request.POST.get(question.__str__())
                answer = Answer.objects.get(question=question, value=answer_value)
                patient_answer = Patient_Survey_Question_Answer(patient=patient, survey=survey, question=question, answer=answer, date=date)
                patient_answers.append(patient_answer)
        return patient_answers


    def process(self, request):
        patient_answers_list = []
        date = self.cleaned_data['date']
        id_patient = self.cleaned_data['patient']
        patient = Patient.objects.get(pk=id_patient)
        survey = Survey.objects.get(pk=self.survey_name)

        patient_answers_list = self.get_patient_answers_from_form(request=request, patient=patient, survey=survey, date=date)
        for ans in patient_answers_list:
                print(f"{ans.patient} - {ans.survey} - {ans.question} - {ans.answer}")
    #patient_answers creates a transaction: either all answers are written or nothing, to prevent DB corruption in case of error
        for patient_answers in patient_answers_list:
            patient_answers.save()



class FormSurveyCaregiver(forms.Form):

    def __init__(self, survey_name, *args, **kwargs):
        super(FormSurveyCaregiver, self).__init__(*args, **kwargs);
        self.survey_name=survey_name

    def get_caregivers():
        caregivers_list = []
        for caregiver in Caregiver.objects.all():
            caregivers_list.append((caregiver.id, caregiver.__str__()))
        return caregivers_list


    caregiver = forms.ChoiceField(
                        choices = get_caregivers(),
                        label="Caregiver:",
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
        cleaned_data = super(FormSurveyCaregiver, self).clean()
        id_caregiver = cleaned_data['caregiver']
        date = cleaned_data['date']
        survey = Survey.objects.get(pk=self.survey_name)
        caregiver = Caregiver.objects.get(pk=id_caregiver)
        caregiver_surveys = Caregiver_Survey_Question_Answer.objects.filter(caregiver=caregiver, survey=survey, date=date)
#       checking for empty QuerySet, if not empty the survey has already been filled
        if caregiver_surveys:
            raise ValidationError(f"Il questionario {survey} è stato già compilato da {caregiver} in data {date}")

        return cleaned_data


    def get_caregiver_answers_from_form(self, request, caregiver, survey, date):
        caregiver_answers = []
        for question in survey.questions.all():
            if question.type.__str__() == "Instructions in compound question":
                continue
            elif question.type.__str__() == "Single Choice":
                id_answer = request.POST.get(question.__str__())
                answer = Answer.objects.get(pk=id_answer)
                caregiver_answer = Caregiver_Survey_Question_Answer(caregiver=caregiver, survey=survey, question=question, answer=answer, date=date)
                caregiver_answers.append(caregiver_answer)
            elif question.type.__str__() == "Multiple Choice":
                ids_answers = request.POST.getlist(question.__str__())
                if not ids_answers:
                    if not Answer.objects.all().filter(question=question, value="Nessuno"):
                        Answer(question=question, value="Nessuno").save()
                    answer = Answer.objects.get(question=question, value="Nessuno")
                    caregiver_answer = Caregiver_Survey_Question_Answer(caregiver=caregiver, survey=survey, question=question, answer=answer, date=date)
                    caregiver_answers.append(caregiver_answer)
                else:
                    for id_answer in ids_answers:
                        answer = Answer.objects.get(pk=id_answer)
                        caregiver_answer = Caregiver_Survey_Question_Answer(caregiver=caregiver, survey=survey, question=question, answer=answer, date=date)
                        caregiver_answers.append(caregiver_answer)
            elif question.type.__str__() == "Alphanumerical Input":
                answer_value = request.POST.get(question.__str__())
                if not Answer.objects.filter(question=question, value=answer_value):
                    Answer(question=question, value=answer_value).save()
                answer = Answer.objects.get(question=question, value=answer_value)
                caregiver_answer = Caregiver_Survey_Question_Answer(caregiver=caregiver, survey=survey, question=question, answer=answer, date=date)
                caregiver_answers.append(caregiver_answer)
            elif question.type.__str__() == "Range Input [0-10]":
                # get the value of the answer, thanks to that and the question it is possible to retrieve the Answer from DB(necessary for caregiver_Survey_Question_Answer)
                answer_value = request.POST.get(question.__str__())
                answer = Answer.objects.get(question=question, value=answer_value)
                caregiver_answer = Caregiver_Survey_Question_Answer(caregiver=caregiver, survey=survey, question=question, answer=answer, date=date)
                caregiver_answers.append(caregiver_answer)
        return caregiver_answers

    def process(self, request):
        caregiver_answers_list = []
        date = self.cleaned_data['date']
        id_caregiver = self.cleaned_data['caregiver']
        caregiver = Caregiver.objects.get(pk=id_caregiver)
        survey = Survey.objects.get(pk=self.survey_name)
        caregiver_answers_list = self.get_caregiver_answers_from_form(request=request,caregiver=caregiver, survey=survey, date=date)
    #patient_answers creates a transaction: either all answers are written or nothing, to prevent DB corruption in case of error
        for caregiver_answers in caregiver_answers_list:
            caregiver_answers.save()
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
