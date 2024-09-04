from openpyxl import Workbook
from django.http import HttpResponse

def generate_excel(request):
    # Create a new Excel workbook
    wb = Workbook()
    ws = wb.active

    # Add data to the Excel sheet
    ws.append(['Name', 'Age'])
    ws.append(['Alice', 30])
    ws.append(['Bob', 25])
    ws.append(['Charlie', 35])

    # Save the workbook
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="sample.xlsx"'
    wb.save(response)

    return response