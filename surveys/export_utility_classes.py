class SingleSurvey():
    def __init__(self, date, raw_filled_survey_rows):
        self.date = date
        self.raw_filled_survey_rows = raw_filled_survey_rows

    def get_cleaned_survey(self):
        cleaned_survey = []
        # header
        cleaned_survey.append(("Data di Compilazione", self.date.__str__()))
        cleaned_survey.append(('Numero Sequenza Domanda', 'Domanda', 'Numero Sequenza Risposta', 'Risposta'))
        # content
        for raw_question, raw_answer in raw_rows:
            question = Question.objects.get(pk=raw_question)
            q_seq_subseq_number = f"{question.question_sequence_number}"
            if question.question_subsequence_number is not None:
                q_seq_subseq_number = f"{q_seq_subseq_number}.{question.question_subsequence_number}"

            answer = Answer.objects.get(pk=raw_answer)
            a_seq_number =  answer.answer_sequence_number

            cleaned_survey.append((q_seq_subseq_number, question.__str__(), a_seq_number, answer.__str__()))

        return cleaned_survey 
