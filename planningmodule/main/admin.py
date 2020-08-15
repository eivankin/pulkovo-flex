from django.contrib import admin
from .models import *
from .views import MyModelAdmin
import pandas as pd
import os


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


@admin.register(CourseTheme)
class CourseThemeAdmin(MyModelAdmin):
    def save_data(self, file):
        pass


@admin.register(Teacher)
class TeacherAdmin(MyModelAdmin):
    def save_data(self, file):
        pass


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


admin.site.register(Theme)
admin.site.register(Subject)
admin.site.register(ScheduleTemplate)
admin.site.register(Lesson)
admin.site.register(Day)
