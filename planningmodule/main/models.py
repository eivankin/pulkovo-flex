from django.db import models


class Theme(models.Model):
    name = models.CharField('Наименование', max_length=255)

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'


class Teacher(models.Model):
    PRIORITIES = [(0, 'Если нет других свободных преподавателей'),
                  (1, 'Минимальный'),
                  (2, 'Средний'),
                  (3, 'Максимальный')]
    name = models.CharField('ФИО', max_length=255)
    email = models.EmailField('Корпоративный аккаунт')
    additional_email = models.EmailField('Дополнительный e-mail', null=True)
    priority = models.IntegerField('Приоритет при распределении', 
                                   choices=PRIORITIES)
    schedule = models.CharField('График работы', max_length=50, default='{"type":0,"args":[5]}')
    themes = models.ManyToManyField(Theme, verbose_name='Может проводить занятия по темам')

    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'


class Subject(models.Model):
    TYPES = [(False, 'Неавиационный персонал'),
                    (True, 'Авиационный персонал')]
    name = models.CharField('Наименование', max_length=255)
    students_type = models.BooleanField('Тип', choices=TYPES)

    class Meta:
        verbose_name = 'Дисциплина'
        verbose_name_plural = 'Дисциплины'


class ScheduleTemplate(models.Model):
    begin = models.TimeField('Начало лекции')
    end = models.TimeField('Конец лекции')

    def __str__(self):
        return f'{self.begin}-{self.end}'

    class Meta:
        verbose_name = 'Расписание лекций'
        verbose_name_plural = 'Расписание лекций'


class Course(models.Model):
    name = models.CharField('Наименование', max_length=50)
    full_name = models.CharField('Полное наименование', max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, 
                                verbose_name='Дисциплина')

    class Meta:
        verbose_name = 'Учебная программа'
        verbose_name_plural = 'Учебные программы'


class CourseTheme(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, unique=True, 
                               verbose_name='Учебная программа')
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, unique=True,
                              verbose_name='Тема')
    number = models.CharField('Номер темы в курсе', max_length=5)
    hours = models.IntegerField('Количество часов')

    def __str__(self):
        return f'Тема {self.number}. {self.theme.name}'

    class Meta:
        verbose_name = 'Тема курса'
        verbose_name_plural = 'Темы курса'


class Classroom(models.Model):
    LESSON_TYPES = [(0, 'практические'), (1, 'теоретические'), 
                    (2, 'практические/теоретические')]
    name = models.CharField('Наименование', max_length=10)
    email = models.EmailField('E-mail')
    capacity = models.IntegerField('Количество мест')
    lesson_type = models.IntegerField('Вид занятий', choices=LESSON_TYPES)
    top_priority_subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, 
                                             verbose_name='Преимущество у дисциплины')
    possible_courses = models.ManyToManyField(Course, verbose_name='Подходит для программ')

    class Meta:
        verbose_name = 'Аудитория'
        verbose_name_plural = 'Аудитории'


class Lesson(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, 
                                verbose_name='Преподаватель')
    classrom = models.ForeignKey(Classroom, on_delete=models.CASCADE,
                                 verbose_name='Аудитория')
    time_interval = models.ForeignKey(ScheduleTemplate, on_delete=models.CASCADE,
                                      verbose_name='Время проведения лекции')
    date = models.DateField('Дата')
    themes = models.ManyToManyField(CourseTheme, verbose_name='Темы лекции')

    class Meta:
        verbose_name = 'Лекция'
        verbose_name_plural = 'Лекции'


class Vacation(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE,
                                verbose_name='Преподаватель')
    begin = models.DateField('Начало отпуска')
    end = models.DateField('Конец отпуска')

    class Meta:
        verbose_name = 'Отпуск'
        verbose_name_plural = 'Отпуска'


class Day(models.Model):
    date = models.DateField('Дата')
    is_holiday = models.BooleanField('Выходной день')
    shifts = models.CharField('Смены', max_length=50)

    class Meta:
        verbose_name = 'День'
        verbose_name_plural = 'Дни'
