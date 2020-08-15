from django.db import models


class Theme(models.Model):
    name = models.CharField('Наименование', max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'


class Teacher(models.Model):
    PRIORITIES = [(0, 'Если нет других свободных преподавателей'),
                  (1, 'Минимальный'),
                  (2, 'Средний'),
                  (3, 'Максимальный')]
    SCHEDULES = [(0, 'N дней в неделю (например, пятидневка)'),
                 (1, 'Сменный'),
                 (2, 'Индивидуальный (выходной после N дней)')]
    name = models.CharField('ФИО', max_length=255)
    email = models.EmailField('Корпоративный аккаунт')
    additional_email = models.EmailField('Дополнительный e-mail', null=True)
    priority = models.IntegerField('Приоритет при распределении', 
                                   choices=PRIORITIES)
    schedule_type = models.IntegerField('Тип графика работы', choices=SCHEDULES)
    schedule_days = models.IntegerField('Сколько дней может работать (оставить пустым для сменного графика)', 
                                        null=True)
    shifts = models.BinaryField('Смены', max_length=4, null=True)
    themes = models.ManyToManyField(Theme, verbose_name='Может проводить занятия по темам')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'


class Subject(models.Model):
    TYPES = [(False, 'Неавиационный персонал'),
                    (True, 'Авиационный персонал')]
    name = models.CharField('Наименование', max_length=255)
    students_type = models.BooleanField('Тип', choices=TYPES, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Дисциплина'
        verbose_name_plural = 'Дисциплины'


class ScheduleTemplate(models.Model):
    begin = models.TimeField('Начало лекции')
    end = models.TimeField('Конец лекции')

    def __str__(self):
        return f'{self.begin.strftime("%H:%M")}-{self.end.strftime("%H:%M")}'

    class Meta:
        verbose_name = 'Расписание лекций'
        verbose_name_plural = 'Расписание лекций'


class Course(models.Model):
    name = models.CharField('Наименование', max_length=50, null=True)
    full_name = models.CharField('Полное наименование', max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, 
                                verbose_name='Дисциплина')
    
    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Учебная программа'
        verbose_name_plural = 'Учебные программы'


class CourseTheme(models.Model):
    TYPES = [(0, 'практическая'), (1, 'теоретическая'), 
             (2, 'оба типа')]
    course = models.ForeignKey(Course, on_delete=models.CASCADE, unique=True, 
                               verbose_name='Учебная программа')
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, unique=True,
                              verbose_name='Тема')
    number = models.CharField('Номер темы в курсе', max_length=5)
    hours = models.IntegerField('Количество часов')
    theme_type = models.IntegerField('Тип темы', choices=TYPES)

    def __str__(self):
        return f'Тема {self.number}. {self.theme.name}'

    class Meta:
        verbose_name = 'Тема курса'
        verbose_name_plural = 'Темы курса'


class Classroom(models.Model):
    LESSON_TYPES = [(0, 'практические'), (1, 'теоретические'), 
                    (2, 'практические/теоретические')]
    CONFIGS = [(0, 'с партами'), 
               (1, 'стулья без парт, для тренинговых форматов'), 
               (2, 'с партами, муляжи для Авиационной безопасности'),
               (3, 'с партами, интерактивная доска')]
    name = models.CharField('Наименование', max_length=10)
    email = models.EmailField('E-mail', null=True)
    capacity = models.IntegerField('Количество мест')
    lesson_type = models.IntegerField('Вид занятий', choices=LESSON_TYPES)
    config = models.IntegerField('Конфигурация аудитории', choices=CONFIGS)
    top_priority_subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, 
                                             verbose_name='Преимущество у дисциплины', 
                                             related_name='priority_subj')
    possible_subjects = models.ManyToManyField(Subject, verbose_name='Подходит для дисциплин')

    def __str__(self):
        return self.name

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
    TYPES = [(False, 'очередной'), (True, 'дополнительный')]
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE,
                                verbose_name='Преподаватель')
    begin = models.DateField('Начало отпуска')
    end = models.DateField('Конец отпуска')
    vacation_type = models.BooleanField('Тип отпуска', choices=TYPES)

    class Meta:
        verbose_name = 'Отпуск'
        verbose_name_plural = 'Отпуска'


class Day(models.Model):
    date = models.DateField('Дата')
    is_holiday = models.BooleanField('Выходной день')
    shifts = models.BinaryField('Смены', max_length=4)

    def __str__(self):
        return self.date

    class Meta:
        verbose_name = 'День'
        verbose_name_plural = 'Дни'
