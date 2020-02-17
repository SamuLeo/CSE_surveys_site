from django import forms
from .models import Survey,Question,Answer,QuestionType

class FormSurvey(forms.Form):

    def __init__(self, survey_name):
        super().__init__(self);
        self.survey_name=survey_name


    def get_answers_list_for_question(self, question):
        answers_list = []
        for answer in question.answers.all():
            answers_list.append((answer.answer_sequence_number,answer.value))
        return answers_list


    def get_survey(self):
        form_survey = {}
        survey = Survey.objects.get(pk=self.survey_name)
        for question in survey.questions.all():
        # caso di domanda composta da gestire qua
            print(question.__str__())
            answers_list = self.get_answers_list_for_question(question)
            print(answers_list)
        # if "Single Choice" in question.type:
            form_survey[question.__str__()] = self.get_answers_list_for_question(question)
        return form_survey        

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
