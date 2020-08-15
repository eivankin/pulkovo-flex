
from glob import glob
import os
import pandas as pd

if __name__ == '__main__':

    paths = glob(os.path.dirname(os.path.abspath(__file__)) + '/Расписание по дням.xlsx', recursive=True)


    bigdata = []
    for path in paths:
        xl = pd.ExcelFile(path)
        for sheet_name in xl.sheet_names:
            minidata = xl.parse(sheet_name=sheet_name)
            bigdata.append(minidata)
        """
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
        """


    Excel = pd.ExcelWriter('ExcelDays.xlsx')
    for sheet_id in range(len(bigdata)):
        bigdata[sheet_id].to_excel(excel_writer=Excel ,sheet_name='Week '+ str(sheet_id))
    Excel.save()