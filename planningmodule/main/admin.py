from django.contrib import admin
from .models import *
from .views import *
from .forms import BinaryWidget, MultiSelectors
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
            path('<int:id>/change/import/', self.import_themes),
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
        errors = []
        if request.method == 'POST':
            form = ImportForm(request.POST)
            errors = self.save_themes(request.FILES['file'], id)
            if not errors:
                messages.info(request, 'Темы успешно импортированы')
            else:
                messages.error(request, f'Не удалось импортировать темы: {", ".join(errors)}')
        form = ImportForm()
        context = dict(self.admin_site.each_context(request), form=form)
        return render(request, 'main/import.html', context)

    def save_themes(self, file, id):
        def to_float(s):
            try: 
                return float(s)
            except ValueError:
                return 0 
        
        file_format = file.name.split('.')[-1]
        idx = 0 if 'DI-L30В' in file.name else 1
        if file_format == 'docx':
            path = os.path.dirname(os.path.abspath(__file__)) + \
                '/files/theme_import.' + file_format
            with open(path, 'wb+') as dest:
                for chunk in file.chunks():
                    dest.write(chunk)
            
            doc = Document(path)
            for table in doc.tables:
                for row in table.rows:
                    c1 = row.cells[idx].text
                    if c1.startswith('Тема') or c1.startswith('Итог'):
                        if c1.startswith('Тема'):
                            th = c1.split(' ')
                            number, name = th[1], ' '.join(th[2:])
                        else:
                            number, name = '', c1
                        t_h, p_h = map(lambda x: to_float(x.text.replace(',', '.')), 
                                       row.cells[idx + 2:idx + 4])

                        theme, created = Theme.objects.get_or_create(name=name)
                        c_theme = CourseTheme(
                            course=Course.objects.get(pk=id),
                            theme=theme, number=number,
                            p_hours=p_h,
                            t_hours=t_h
                        )
                        c_theme.save()
            return []
        return ('недопустимый формат файла, допустим только docx', )


@admin.register(Teacher)
class TeacherAdmin(MyModelAdmin):
    SHIFTS = [(0, 'Смена № 1'), (1, 'Смена № 2'),
              (2, 'Смена № 3'), (3, 'Смена № 4')]
    formfield_overrides = {
        models.BinaryField: {'widget': BinaryWidget(choices=SHIFTS)},
    }
    
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
                teacher.save()
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
            year = timezone.now().year
            for index, row in table.iterrows():
                if len(str(row[1])) > 3:
                    try:
                        teacher = Teacher.objects.get(name__contains=str(row[1]).split(' ')[0])
                    except Teacher.DoesNotExist:
                        continue
                    vac_type = bool(int(row[2]) - 1)
                    for m, i in enumerate(range(4, 28, 2), start=1):
                        decade, duration = int(row[i]), int(row[i + 1])
                        vac = Vacation(
                            teacher=teacher, vacation_type=vac_type,
                            begin=timezone.datetime(year=year, month=m, day=decade * 10),
                            end=timezone.datetime(year=year, month=m, day=decade * 10 + duration)
                        )
                        vac.save()
            return []

        return ('недопустимый формат файла, допустимы только xls и xlsx', )


@admin.register(Day)
class DayAdmin(MyModelAdmin):
    formfield_overrides = {
        models.BinaryField: {'widget': MultiSelectors},
    }
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
            return []
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
admin.site.register(Group)
