from docx import Document
from glob import glob
import csv

def csv_writer(data, path):
    """
    Write data to a CSV file path
    """
    with open(path, "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        for line in data:
            writer.writerow(line)

if __name__ == '__main__':
    data = []
    paths = glob('*.docx', recursive=True)
    for path in paths:
        document = Document(path)
        paragraphs = document.paragraphs

        table = document.tables[0]


        for row in range(2, len(table.rows)):
            string = []
            for cell in range(1, len(table.rows[row].cells)):
                string.append(table.rows[row].cells[cell].text)
            data.append(string)

    csv_writer(data, 'csvшник.csv')