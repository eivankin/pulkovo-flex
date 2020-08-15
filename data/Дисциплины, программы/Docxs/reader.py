from docx import Document
from glob import glob
import os

paths = glob(os.path.dirname(os.path.abspath(__file__)) + '/' + '*.docx')
for path in paths:
    doc = Document(path)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells[1:]:
                print(cell.text, end='\t')
            print()
    break