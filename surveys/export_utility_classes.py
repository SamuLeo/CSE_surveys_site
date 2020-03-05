import xlwt

from .models import Patient_Survey_Question_Answer, Caregiver_Survey_Question_Answer

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
        for raw_question, raw_answer in self.raw_filled_survey_rows:
            question = Question.objects.get(pk=raw_question)
            q_seq_subseq_number = f"{question.question_sequence_number}"
            if question.question_subsequence_number is not None:
                q_seq_subseq_number = f"{q_seq_subseq_number}.{question.question_subsequence_number}"

            answer = Answer.objects.get(pk=raw_answer)
            a_seq_number =  answer.answer_sequence_number

            cleaned_survey.append((q_seq_subseq_number, question.__str__(), a_seq_number, answer.__str__()))

        return cleaned_survey

class SurveysOneTypeOnePerson():
    def __init__(self, person, date_from, date_to, survey):
        self.person = person
        self.single_survey_list = single_survey_list
        self.date_from = date_from
        if date_to:
            self.date_to = date_to
        self.survey = survey

    def __get_raw_filled_rows_one_person_one_type(self):
        if survey.patient_survey:
            if date_to:
                return Patient_Survey_Question_Answer.objects.filter(patient=self.person, date__gte=self.date_from,
                                date__lte=self.date_to,survey=self.survey).values_list('date','question','answer',)
            else:
                return Patient_Survey_Question_Answer.objects.filter(patient=self.person, date=self.date_from,
                                survey=self.survey).values_list('date','question','answer', )
        else:
            if date_to:
                return Caregiver_Survey_Question_Answer.objects.filter(caregiver=self.person,date__gte=self.date_from,
                                date__lte=self.date_to, survey=self.survey).values_list('date','question','answer',)
            else:
                return Caregiver_Survey_Question_Answer.objects.filter(caregiver=self.person, date=self.date_from,
                                survey=self.survey).values_list('date','question', 'answer',)

    def __get_cleaned_surveys_list(self):
        surveys_list = []
        raw_filled_rows_one_person_one_type = self.__get_raw_filled_rows_one_person_one_type()
        # get list of surveys dates with list comprehension
        surveys_dates_list = [row[0] : for row in raw_filled_rows_one_person_one_type if raw_filled_rows_one_person_one_type[0] not in surveys_dates_list]

        for date in surveys_dates_list:
            # get survey rows tuple(question, answer) with list comprehension
            single_survey_raw_rows = [(row[1], row[2]) : for row in raw_filled_rows_one_person_one_type if raw_filled_rows_one_person_one_type[0] == date]
            single_survey = SingleSurvey(date=date, raw_filled_survey_rows=single_survey_raw_rows).get_cleaned_survey()
            surveys_list.append(single_survey)

        return surveys_list

    def __get_cleaned_person(self):
        return (("Paziente", self.person.__str__())


    def write_surveys_on_excel_sheet(self, work_sheet, initial_row, initial_column):
        head = self.__get_cleaned_person()
        surveys_list = self.__get_cleaned_surveys_list()

        row_num = initial_row

        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        for col_num in range(len(head)):
            work_sheet.write(row_num, col_num + initial_column, head[col_num], font_style)
        row_num += 1

        for survey in surveys_list:
            header = survey[:2]
            survey_content = survey[2:]

            font_style = xlwt.XFStyle()
            font_style.font.bold = True
            for header_element in header:
                for col_num in range(len(header_element)):
                    work_sheet.write(row_num, col_num + initial_col_num, header_element[col_num], font_style)
                row_num += 1

            # Sheet body, remaining rows
            font_style = xlwt.XFStyle()

            for row in survey_content:
                for col_num in range(len(row)):
                    work_sheet.write(row_num, col_num + initial_col_num, row[col_num], font_style)
                row_num += 1

        col_growth = max(len(head), len(header), len(row))
        col_num = initial_col_num + col_growth
        return col_num


class SurveysOneType():
    def __init__(self, surveys_one_type_one_person_list):
        # surveys_one_type_one_person_list needs to be a list of SurveysOneTypeOnePerson
        self.surveys_one_type_one_person_list = surveys_one_type_one_person_list

    def write_surveys_on_excel_sheet(self, work_sheet):
        initial_row = 0
        initial_column = 0

        for surveys_one_type_one_person in self.surveys_one_type_one_person_list:
            initial_column += surveys_one_type_one_person.write_surveys_on_excel_sheet(work_sheet=work_sheet, initial_row=initial_row, initial_column=initial_column)
