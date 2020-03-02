import xlwt, re

from django.shortcuts import render, HttpResponse
from .models import Patient, Caregiver, Answer, Survey,Patient_Survey_Question_Answer,Caregiver_Survey_Question_Answer, Question



# def export_to_xls_single_survey(request, patient, survey, date):
#
#     try:
#         raw_rows = Patient_Survey_Question_Answer.objects.filter(patient=patient, date=date,survey=survey).values_list('patient', 'date', 'survey', 'question', 'answer', )
#         rows = []
#         for raw_patient, raw_date, raw_survey, raw_question, raw_answer in raw_rows:
#             patient = Patient.objects.get(pk=raw_patient).__str__()
#             date = raw_date.__str__()
#             survey = raw_survey.__str__()
#             question = Question.objects.get(pk=raw_question).__str__()
#             answer = Answer.objects.get(pk=raw_answer).__str__()
#             rows.append((patient,date,survey,question,answer))
#     except:
#         return render(request, "surveys/export_error.html")
#
#     response = HttpResponse(content_type='application/ms-excel')
#     name = f"{survey}_{date}_patient.xls"
#     response['Content-Disposition'] = f"attachment; filename={survey}_{date}_{patient}.xls"
#
#     wb = xlwt.Workbook(encoding='utf-8')
#     ws = wb.add_sheet('Questionario')
#
#     # Sheet header, first row
#     row_num = 0
#
#     font_style = xlwt.XFStyle()
#     font_style.font.bold = True
#
#     columns = ['ID Paziente', 'Data(y-m-d)', 'Questionario', 'Domanda', 'Risposta', ]
#
#     for col_num in range(len(columns)):
#         ws.write(row_num, col_num, columns[col_num], font_style)
#
#     # Sheet body, remaining rows
#     font_style = xlwt.XFStyle()
#
#     for row in rows:
#         row_num += 1
#         for col_num in range(len(row)):
#             ws.write(row_num, col_num, row[col_num], font_style)
#
#     wb.save(response)
#     return response




def get_surveys_of_patient(patient, surveys_list, date_from, date_to):
    surveys_dict = {}
    for survey in surveys_list:
        if date_to:
            raw_rows = Patient_Survey_Question_Answer.objects.filter(patient=patient,
                                                                date__gte=date_from,
                                                                date__lte=date_to,
                                                                survey=survey).values_list('date',
                                                                                        'question',
                                                                                         'answer', )
        else:
            raw_rows = Patient_Survey_Question_Answer.objects.filter(patient=patient,
                                                                            date=date_from,
                                                                            survey=survey).values_list('date',
                                                                                                    'question',
                                                                                                     'answer', )
        # list of lists
        surveys_of_one_type_list = []
        # list
        single_survey = []
        # store date of first survey in order to know when the survey change(thanks to 'date')
        current_survey_date = raw_rows[0][0]

        for raw_date, raw_question, raw_answer in raw_rows:

            if not single_survey:
                single_survey.append(("Data di Compilazione", raw_date.__str__()))
                single_survey.append(('Numero Sequenza Domanda', 'Domanda', 'Numero Sequenza Risposta', 'Risposta'))

            if raw_date != current_survey_date:
                surveys_of_one_type_list.append(single_survey)
                single_survey = []
                single_survey.append(("Data di Compilazione", raw_date.__str__()))
                single_survey.append(('Numero Sequenza Domanda', 'Domanda', 'Numero Sequenza Risposta', 'Risposta'))
                current_survey_date = raw_date

            question = Question.objects.get(pk=raw_question)
            q_seq_subseq_number = f"{question.question_sequence_number}"
            if question.question_subsequence_number is not None:
                q_seq_subseq_number = q_seq_subseq_number + f".{question.question_subsequence_number}"

            answer = Answer.objects.get(pk=raw_answer)
            a_seq_number =  answer.answer_sequence_number


            single_survey.append((q_seq_subseq_number, question.__str__(), a_seq_number, answer.__str__()))
# necessary for final survey where the date check won't work
        surveys_of_one_type_list.append(single_survey)

        surveys_dict[survey.__str__()] = surveys_of_one_type_list

    return surveys_dict






def write_surveys_of_patient_on_work_sheet(work_sheet, row_num, initial_col_num, patient, surveys_list):
    """ This function write all the surveys passed to it through surveys_list(list of lists) to the work_sheet, the surveys abs
        passed must be of the same type, the row_num and the column num are used as starting point"""

    head = ("Paziente", patient.__str__())
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    for col_num in range(len(head)):
        work_sheet.write(row_num, col_num + initial_col_num, head[col_num], font_style)

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
    return (row_num, col_num)

def get_valid_work_sheet_name(survey_name):
    """This function return a valid name for the Excel work sheet associated to the survey"""

    survey = Survey.objects.get(pk=survey_name)

    if survey.short_name is not None:
        pattern = re.compile(r'[\\/\*\?:\[\] -]')
        work_sheet_name = pattern.sub("_", survey.short_name)
    else:
        pattern = re.compile(r'[\\/\*\?:\[\] -]')
        work_sheet_name = pattern.sub("_", survey_name)[:31]

    return work_sheet_name

def export_to_xls_patient_surveys(patient, surveys_list, date_from, date_to):

    surveys_dict = get_surveys_of_patient(patient=patient, surveys_list=surveys_list, date_from=date_from, date_to=date_to)

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f"attachment; filename=questionari_{patient}.xls"

    work_book = xlwt.Workbook(encoding='utf-8')

    # Sheet header, first row
    row_num = 0
    col_num = 0

    for survey_name in surveys_dict:
        work_sheet = work_book.add_sheet(get_valid_work_sheet_name(survey_name=survey_name))

        surveys_of_one_type_list = surveys_dict[survey_name]
        write_surveys_of_patient_on_work_sheet(work_sheet=work_sheet, row_num=row_num, initial_col_num = col_num, patient=patient, surveys_list=surveys_of_one_type_list)

    work_book.save(response)
    return response





def export_to_xls_single_survey(request, patient, survey, date):

    try:
        raw_rows = Patient_Survey_Question_Answer.objects.filter(patient=patient, date=date,survey=survey).values_list('question', 'answer', )
        rows = []
        for raw_question, raw_answer in raw_rows:

            question = Question.objects.get(pk=raw_question)
            q_seq_subseq_number = f"{question.question_sequence_number}"
            if question.question_subsequence_number is not None:
                q_seq_subseq_number = q_seq_subseq_number + f".{question.question_subsequence_number}"

            answer = Answer.objects.get(pk=raw_answer)
            a_seq_number =  answer.answer_sequence_number

            rows.append((q_seq_subseq_number, question.__str__(), a_seq_number, answer.__str__()))
    except:
        return render(request, "surveys/export_error.html")

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f"attachment; filename={survey}_{date}_{patient}.xls"

    work_book = xlwt.Workbook(encoding='utf-8')
    work_sheet = work_book.add_sheet('Questionario')

    # Sheet header, first row
    row_num = 0

    head = [("Questionario", survey)]
    header = [('Questionario', survey.__str__()),
             ('Paziente', patient.__str__()),
             ('Data(y-m-d)', date.__str__()),
             ('Numero Sequenza Domanda', 'Domanda', 'Numero Sequenza Risposta', 'Risposta'),]


    for row in header:
        for col_num in range(len(row)):
            if col_num == 0:
                    font_style = xlwt.XFStyle()
                    font_style.font.bold = True
            else:
                    font_style = xlwt.XFStyle()
                    font_style.font.bold = False
            work_sheet.write(row_num, col_num, row[col_num], font_style)
        row_num += 1

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    for col_num in range(len(columns)):
        work_sheet.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            work_sheet.write(row_num, col_num, row[col_num], font_style)

    work_book.save(response)
    return response


    def export_to_xls_patient_surveys(request, patient, survey):

        try:
            raw_rows = Patient_Survey_Question_Answer.objects.filter(patient=patient, date=date,survey=survey).values_list('question', 'answer', )
            rows = []
            for raw_question, raw_answer in raw_rows:

                question = Question.objects.get(pk=raw_question)
                q_seq_subseq_number = f"{question.question_sequence_number}"
                if question.question_subsequence_number is not None:
                    q_seq_subseq_number = q_seq_subseq_number + f".{question.question_subsequence_number}"

                answer = Answer.objects.get(pk=raw_answer)
                a_seq_number =  answer.answer_sequence_number

                rows.append((q_seq_subseq_number, question.__str__(), a_seq_number, answer.__str__()))
        except:
            return render(request, "surveys/export_error.html")

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f"attachment; filename={survey}_{date}_{patient}.xls"

        work_book = xlwt.Workbook(encoding='utf-8')
        work_sheet = work_book.add_sheet('Questionario')

        # Sheet header, first row
        row_num = 0

        head = [("Questionario", survey)]
        header = [('Questionario', survey.__str__()), ('Paziente', patient.__str__()), ('Data(y-m-d)', date.__str__()),]
        columns = [('Numero Sequenza Domanda', 'Domanda', 'Numero Sequenza Risposta', 'Risposta')]

    #
        for row in header:
            for col_num in range(len(row)):
                if col_num == 0:
                        font_style = xlwt.XFStyle()
                        font_style.font.bold = True
                else:
                        font_style = xlwt.XFStyle()
                        font_style.font.bold = False
                work_sheet.write(row_num, col_num, row[col_num], font_style)
            row_num += 1

        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        for col_num in range(len(columns)):
            work_sheet.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                work_sheet.write(row_num, col_num, row[col_num], font_style)

        work_book.save(response)
        return response
