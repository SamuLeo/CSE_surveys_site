import xlwt

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
    work_sheet = FitSheetWrapper(work_book.add_sheet('Questionario'))

    # Sheet header, first row
    row_num = 0

    head = [("Questionario", survey)]
    header = [('Questionario', survey.__str__()), ('Paziente', patient.__str__()), ('Data(y-m-d)', date.__str__()),]
    columns = ['Numero Sequenza Domanda', 'Domanda', 'Numero Sequenza Risposta', 'Risposta']

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
        work_sheet = FitSheetWrapper(work_book.add_sheet('Questionario'))

        # Sheet header, first row
        row_num = 0

        head = [("Questionario", survey)]
        header = [('Questionario', survey.__str__()), ('Paziente', patient.__str__()), ('Data(y-m-d)', date.__str__()),]
        columns = ['Numero Sequenza Domanda', 'Domanda', 'Numero Sequenza Risposta', 'Risposta']

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
