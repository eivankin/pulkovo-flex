from django.contrib import admin
from .models import *
from .views import MyModelAdmin
from .forms import BinaryWidget
import pandas as pd
import numpy as np
import os
from docx import Document
from django.urls import path
from django.utils import timezone
from requests import get


@admin.register(Classroom)
class ClassroomAdmin(MyModelAdmin):
    def save_data(self, file):
        LESSON_TYPES = {'практические': 0, 'теоретические': 1, 
                    'практические/теоретические': 2, 
                    'теоретические/практические': 2}
        CONFIGS = {'с партами': 0, 
                   'стулья без парт, для тренинговых форматов': 1, 
                   'с партами,\n муляжи для Авиационной безопасности': 2, 
                   'с партами, интерактивная доска': 3}
        
        file_format = file.name.split('.')[-1]
        if file_format == 'xls' or file_format == 'xlsx':
            path = os.path.dirname(os.path.abspath(__file__)) + \
                '/files/classroom_import.' + file_format
            with open(path, 'wb+') as dest:
                for chunk in file.chunks():
                    dest.write(chunk)
            
            table = pd.ExcelFile(path).parse('параметры аудиторий')
            for index, row in table.iterrows():
                classroom = Classroom(name=str(row[0]), capacity=int(row[1]), 
                                      lesson_type=LESSON_TYPES[str(row[2])],
                                      config=CONFIGS[str(row[3])])
                classroom.top_priority_subject = self.select_subjects(str(row[4]))
                classroom.save()
                for subj in self.select_subjects(str(row[5]), 0):
                    classroom.possible_subjects.add(subj)
            return []
        return ('недопустимый формат файла, допустимы только xls и xlsx', )
    
    def select_subjects(self, subj, mode=1):
        """mode=0: для допустимых дисциплин
        mode=1: для приоритетных"""
        subj = subj.replace('\n', ' ')
        if mode:
            if subj == 'нет':
                return None
            return Subject.objects.get(name=subj)
        if subj == 'все дисциплины':
            return Subject.objects.all()
        if subj.startswith('кроме'):
            return Subject.objects.exclude(name=subj[6:])
        if ',' in subj:
            return Subject.objects.filter(name=subj.split(',')[0])
        if ';' in subj:
            subjs = subj.split('; ')
            return Subject.objects.filter(name=subjs[0]).union(Subject.objects.filter(name=subjs[1]))
        return Subject.objects.filter(name=subj)    



@admin.register(Course)
class CourseAdmin(MyModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('<int:id>/import/', self.import_themes),
        ]
        return my_urls + urls

    def save_data(self, file):
        file_format = file.name.split('.')[-1]
        if file_format == 'xls' or file_format == 'xlsx':
            path = os.path.dirname(os.path.abspath(__file__)) + \
                '/files/course_import.' + file_format
            with open(path, 'wb+') as dest:
                for chunk in file.chunks():
                    dest.write(chunk)
            
            table = pd.ExcelFile(path).parse('параметры программ')
            for index, row in table.iterrows():
                if str(row[1]) != 'nan':
                    subj, created = Subject.objects.get_or_create(name=str(row[1]))
                course = Course(subject=subj, full_name=str(row[2]))
                course.save()
            return []
        return ('недопустимый формат файла, допустимы только xls и xlsx', )
    
    def import_themes(self, request, id):
        pass

    def save_themes(self, file):
        file_format = file.name.split('.')[-1]
        if file_format == 'docx':
            path = os.path.dirname(os.path.abspath(__file__)) + \
                '/files/theme_import.' + file_format
            with open(path, 'wb+') as dest:
                for chunk in file.chunks():
                    dest.write(chunk)
            
            doc = Document(path)
            for table in doc.tables:
                pass
            return []
        return ('недопустимый формат файла, допустим только docx', )


@admin.register(Teacher)
class TeacherAdmin(MyModelAdmin):
    # SHIFTS = [(0, 'Смена № 1'), ()]
    # formfield_overrides = {
    #     models.BinaryField: {'widget': BinaryWidget(choices=())},
    # }
    def save_data(self, file):
        file_format = file.name.split('.')[-1]
        if file_format == 'xls' or file_format == 'xlsx':
            path = os.path.dirname(os.path.abspath(__file__)) + \
                '/files/teacher_import.' + file_format
            with open(path, 'wb+') as dest:
                for chunk in file.chunks():
                    dest.write(chunk)
            
            table = pd.ExcelFile(path).parse('параметры преподавателей')
            for index, row in table.iterrows():
                teacher = Teacher(
                    name=str(row[1]), 
                    subject=Subject.objects.get(name=str(row[2])),
                    
                )
            return []
        return ('недопустимый формат файла, допустимы только xls и xlsx', )


@admin.register(Vacation)
class VacationAdmin(MyModelAdmin):
    def save_data(self, file):
        file_format = file.name.split('.')[-1]
        if file_format == 'xls' or file_format == 'xlsx':
            path = os.path.dirname(os.path.abspath(__file__)) + \
                '/files/vacation_import.' + file_format
            with open(path, 'wb+') as dest:
                for chunk in file.chunks():
                    dest.write(chunk)
            
            table = pd.ExcelFile(path).parse('План')
        return ('недопустимый формат файла, допустимы только xls и xlsx', )


@admin.register(Day)
class DayAdmin(MyModelAdmin):
    def save_data(self, file):
        SHIFT_TO_HEX = {'nan': '00', 'д': '01', 'н': '02'}
        file_format = file.name.split('.')[-1]
        if file_format == 'xls' or file_format == 'xlsx':
            path = os.path.dirname(os.path.abspath(__file__)) + \
                '/files/day_import.' + file_format
            with open(path, 'wb+') as dest:
                for chunk in file.chunks():
                    dest.write(chunk)
            
            table = pd.ExcelFile(path).parse('график смен')
            year = timezone.now().year
            for i in range(12):
                month = table.iloc[i * 7 + 1:(i + 1) * 7, :32]
                month = month[1:].set_index('График работы смен на 2019 год').T
                month = month.rename(columns={np.nan: 'День месяца'}).dropna(how='all')
                month = month.astype({'День месяца': 'int8'}).set_index('День месяца')
                month = month.sort_index(axis=1)
                for index, row in month.iterrows():
                    date = timezone.datetime(year=year, month=i + 1, day=index)
                    day = Day(
                        shifts=bytearray.fromhex(''.join([SHIFT_TO_HEX[str(x)] for x in row])),
                        is_holiday=self.check_holiday(date),
                        date=date) 
                    day.save()
        return ('недопустимый формат файла, допустимы только xls и xlsx', )
    
    def check_holiday(self, date):
        if date.weekday() > 4:
            return True
        return bool(int(get(
            f'https://isdayoff.ru/api/getdata?year={date.year}&month={date.month}&day={date.day}').content))



admin.site.register(CourseTheme)
admin.site.register(Theme)
admin.site.register(Subject)
admin.site.register(ScheduleTemplate)
admin.site.register(Lesson)
