from django.db import models

# Create your models here.

class TransplantType(models.Model):

    value = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.value

    class Meta:
        verbose_name="Type Of Transplant"
        verbose_name_plural="Types Of Transplant"


class Patient(models.Model):

    id_patient = models.IntegerField(primary_key=True)

    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    birth_date = models.DateTimeField(blank=True,null=True)

    recovery_date = models.DateTimeField(blank=True,null=True)
    transplant_date = models.DateTimeField(blank=True,null=True)
    resignation_date = models.DateTimeField(blank=True,null=True)

    transplant_type = models.ForeignKey(TransplantType, on_delete=models.DO_NOTHING)

    number_of_sons = models.SmallIntegerField(blank=True,null=True)

    def __str__(self):
        return self.name + " " + self.surname

    class Meta:
        verbose_name="Pazient"
        verbose_name_plural="Pazients"


class Caregiver(models.Model):

    id_patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    birth_date = models.DateTimeField(blank=True,null=True)

    relationship_with_patient = models.CharField(max_length=200)
    number_of_sons = models.SmallIntegerField(blank=True,null=True)
    cohabitant = models.BooleanField()

    def __str__(self):
        return self.name + " " + self.surname

    class Meta:
        verbose_name="Caregiver"
        verbose_name_plural="Caregivers"


class Survey(models.Model):

    id_survey = models.CharField(primary_key=True, max_length=100)

    description = models.TextField(blank=True, null=True)
    patient_survey = models.BooleanField()

    def __str__(self):
        return self.id_survey

    class Meta:
        verbose_name="Survey"
        verbose_name_plural="Surveys"


class QuestionType(models.Model):

    value = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.value

    class Meta:
        verbose_name="Type Of Question"
        verbose_name_plural="Types Of Question"


class Question(models.Model):

    id_survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="questions")
    question_sequence_number = models.SmallIntegerField()

    type = models.ForeignKey(QuestionType, on_delete=models.DO_NOTHING)

    content = models.CharField(max_length=1000)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name="Question"
        verbose_name_plural="Questions"
        models.UniqueConstraint(fields=['id_survey', 'question_sequence_number'], name='unique_survey_QuestionSequenceNumber')

class Answer(models.Model):

    id_question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    answer_sequence_number = models.SmallIntegerField()

    value = models.CharField(max_length=300)

    def __str__(self):
        return self.value

    class Meta:
        verbose_name="Answer"
        verbose_name_plural="Answers"
        models.UniqueConstraint(fields=['id_question', 'answer_sequence_number'], name='unique_question_AnswerSequenceNumber')



class Patient_Survey_Question_Answer(models.Model):

    id_patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="patient_answers")
    id_survey = models.ForeignKey(Survey, on_delete=models.DO_NOTHING)
    id_question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
    id_answer = models.ForeignKey(Answer, on_delete=models.DO_NOTHING)
    date = models.DateTimeField()

    def __str__(self):
        return f"Data: {self.date} \n Paziente: {self.id_patient} \n {self.id_survey}.{self.id_question} = {self.id_question}"

    class Meta:
        verbose_name="Patient's Answer"
        verbose_name_plural="Patient's Answers"
        models.UniqueConstraint(fields=['id_patient', 'id_survey', 'id_question', 'id_answer', 'date'], name='unique_filling_patient')


class Caregiver_Survey_Question_Answer(models.Model):

    id_caregiver = models.ForeignKey(Caregiver, on_delete=models.CASCADE, related_name="caregiver_answers")
    id_survey = models.ForeignKey(Survey, on_delete=models.DO_NOTHING)
    id_question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
    id_answer = models.ForeignKey(Answer, on_delete=models.DO_NOTHING)
    date = models.DateTimeField()

    def __str__(self):
        return f"Data: {self.date} \n Caregiver: {self.id_caregiver} \n {self.id_survey}.{self.id_question} = {self.id_question}"

    class Meta:
        verbose_name="Caregiver's Answer"
        verbose_name_plural="Caregiver's Answers"
        models.UniqueConstraint(fields=['id_caregiver', 'id_survey', 'id_question', 'id_answer', 'date'], name='unique_filling_caregiver')
