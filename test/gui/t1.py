import openpyxl

wb = openpyxl.load_workbook('1234.xlsx')
sheet = wb.worksheets[0]
for row in sheet.iter_rows():
    for cell in row:
        print(cell.coordinate, cell.value)
