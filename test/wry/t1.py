import openpyxl

wb = openpyxl.load_workbook('C://Users//57567//Desktop//1234.xlsx')
sheet = wb.worksheets[0]
sheet['A1'].value='1111111'
wb.save('1234.xlsx')