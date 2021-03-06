from docx import Document
from glob import glob
import os
import pandas as pd
from docx import Document

if __name__ == '__main__':

    paths = glob(os.path.dirname(os.path.abspath(__file__)) + '/' + '*.docx', recursive=True)

    row = (0, '')
    bigdata = []
    needcolumns = ('Наименование разделов и тем', 'Всего (час)', 'Т', 'Т / ДОТ, ЭО* )', 'ПЗ', 'СП', 'Форма контроля')
    for path in paths:
        document = Document(path)


        table = document.tables[0]
        dictionary = dict()
        collumns = []
        minidata = []
        for cell in table.rows[1].cells:
            dictionary.update({cell.text:''})
            collumns.append(cell.text)
            minidata.append([])
        for row in enumerate(start=row[0], iterable=table.rows[2:]):
            for cell in enumerate(row[1].cells):
                minidata[cell[0]].append(cell[1].text)
        for col in enumerate(minidata):
            dictionary.update({collumns[col[0]]:tuple(col[1])})
        frame = pd.DataFrame(dictionary)
        bigdata.append(frame)

    print(bigdata[0].sample())

    Excel = pd.ExcelWriter('ExcelProgramms.xlsx')
    for sheet_id in range(len(bigdata)):
        bigdata[sheet_id].to_excel(excel_writer=Excel ,sheet_name='Programm '+ str(sheet_id))
    Excel.save()