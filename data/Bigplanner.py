import pandas as pd
from munkres import Munkres, print_matrix
import numpy as np


db_example = 'тут будет прикрепленная дбшка по которой буду исправлять логику'

class Planner:
    def __init__(planner, db):
        planner.teachers = db['Teachers']
        planner.subjects = db['Subjects']
        planner.scheduletemplate = db['ScheduleTemplate']
        planner.courses = db['Courses']
        planner.coursethemes = db['CoursThemes']
        planner.classrooms = db['Classrooms']
        planner.lessons = db['Lessons']                                         #Мб на русском
        planner.vacations = db['Vacations']
        planner.days = db['Days']

        dayschedule = ['09.00-09.30',
                       '09.30-10.00',
                       '10.00-10.30',
                       '10.30-11.00',
                       '11.00-11.30',
                       '11.30-12.00',
                       '12.00-12.30',
                       '12.30-13.00',
                       # нид пофиксить и в приоритете ставить так, чтобы учителя сидели в одних и тех же кабинетах,
                       '13.00-13.30',
                       # а не бегали по всему заведению каждые 30 минут, но пока так, т.к. есть короткие и длинные темы
                       '13.30-14.00',
                       '14.00-14.30',
                       '14.30-15.00',
                       '15.00-15.30',
                       '15.30-16.00'
                       ]
        workdays = []
        free = []
        for day in planner.days:
            if day.is_holiday == False:
                workdays.append((day.date, )) # надо сделать через производственный календарь - https://isdayoff.ru/extapi/

        planner.freeschedule = pd.DataFrame(columns=workdays, index=dayschedule).fillna(free).T
        #########planner.shifts = db['Shifts']
        #       Teacher:
        #           PRIORITIES
        #           NAME
        #           EMAIL
        #           SСHEDULE
        #           THEMES

        #       Subject:
        #           TYPE(avic i ne o4en')

        #       ScheduleTemplate:
        #           BEGIN
        #           ENG

        #       Course:
        #           FULLNAME
        #           NAME
        #           @Subject

        #       CourseTheme:
        #           @Course
        #           THEME
        #           NUMBER (id)
        #           HOURS

        #       Classroom:
        #           LESSON_TYPES(0-2)
        #           NAME
        #           EMAIL
        #           CAPACITY
        #           TOP_PRIORITY_SUBJECT
        #           POSSIBLE_COURSES

        #       Lesson:
        #           @Teacher
        #           @Classrom
        #           TIME_INTERVAL (@ScheduleTemplate)
        #           DATE (@ScheduleTemplate)
        #           @Theme

        #       Vacation:
        #           TYPES(add., main)
        #           @Teacher
        #           BEGIN
        #           END

        #       Day:
        #           DATE
        #           IS_HOLIDAY
        #           SHIFTS

        #       Shift - через дни


    @property
    def planning_a_schedule(planner):

        """
        ____________________________________________________________

        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$ Вложенные циклы ~O(n!)

        ITER = list(schedule.itertuples(index=True))

        for day in ITER:
            for halfhour in enumerate(day[1:]):
                for cabinet in planner.classroms: # Дальше все функциями
                    if cabinet.check_for_free(day[0], halfhour[0]) == True:     #проверка доступности кабинета, поиск по всем lessonам в это время
                        for courses in cabinet.possible_courses:
                            for course in courses:
                                for theme in course.themes:
                                    for group in planner.courses.course.groups:
                                        if theme.number == group.status[0]:          #status = [id_theme, num_of_minutes passed]
                                            for teacher in theme.teacher_set:
                                                if teacher.check_for_free(day[0], halfhour[0]) == True: #проверка доступности учителя, поиск по всем lessonам в это время

                                                        # тут должен быть фидбэк на изменение статуса группы +1
                                                        # (но нужно помнить, что на некоторые темы нужно больше времени, а на некоторые ***** 0,3 часа),
                                                        # На изменение расписания, конкретного дня
                                                    time = schedule.columns[halfhour[0]]
                                                    new_lesson = Lesson(teacher=teacher, classroom=cabinet, time_interavl=time, date=day[0], themes=theme.theme) #Серьезно CourseTheme.theme?
                                                    schedule.loc[day[0], time].append(new_lesson)  #наверное как-то так, Жень, импортни класс Lesson, либо как-то в обходную, хз
                                                    group.status[1] += 30                          #пока пишу цифрами, потом нид переменную ввести и переименовать halfhour

                                                    if group.status[1] >= theme.hours * 60:
                                                        group.status[0] += 1
                                                        group.status[1] = 0
                                                        #нид фидбэк
                                                    break


                                            break
                                                                                         #Добавить элемент рандома, чтобы человеческим глазом подобрать более подходящее расписание


    _______________________________________________________________________________

        # $$$$$$$$$$$$$$$$        Функциональный перебор ~ O(n^в какой-то довольно большой степени)  .предположительно. Никаких тестов

        def check_for_free_cabinet(date, time, cabinet):
            def check_for_free_course_groups(date, time, course):
                def check_for_free_group(date, time, group):
                    def check_to_need_theme_for_group(date, time, group, theme):
                        def check_for_free_teacher(date, time, teacher):
                            def create_new_lesson(teacher, cabinet, time, day, theme):  # time = planner.freeschedule.columns[halfhour[0]]
                                def change_group_status(group, theme):
                                    if group.status[1] >= theme.hours * 60:
                                        group.status[0] += 1
                                        group.status[1] = 0
                                        # нид фидбэк в планировщик, пока сущности нет - хз как писать
                                try:

                                    new_lesson = Lesson(teacher=teacher, classroom=cabinet, time_interavl=time, date=day[0],
                                                    themes=theme.theme)  # Серьезно CourseTheme.theme?
                                    planner.freeschedule.loc[day[0], time].append(new_lesson)

                                    change_group_status(group, theme)

                                    return True
                                except:
                                    print('Возникла ошибка с созданием нового урока')
                                    return False

                            for lesson in planner.freeschedule.loc[date, time]:
                                if teacher.name == lesson.teacher.name:
                                    print('Учитель ведет урок')
                                    return False
                                # elif teacher.name not in day.shifts: print('Учитель работает не в эту смену')
                                # elif teacher.name in holidays: print('Учитель в отпуске')
                                else:
                                    feedback = create_new_lesson(teacher, cabinet, time, date, theme)
                                    return feedback
                            else:
                                print('Не удалось создать новое занятие')
                                return False

                        if theme.number == group.status[0]:
                            for teacher in theme.teacher_set:
                                feedback = check_for_free_teacher(date, time, teacher)
                                if feedback == True:
                                    return feedback
                            else:
                                print('Не удалось найти свободных учителей')
                                return False
                        else:
                            print('Эта тема уже пройдена этой групппой')
                            return False

                    for lesson in planner.freeschedule.loc[date, time]:
                        if type(lesson) == Lesson and group.name == lesson.group.name: #нужно добавить ссылку на группу в сущности урока
                            print('Эта группа в данный момент занята')
                            return False
                        else:
                            for theme in course.themes:
                                feedback = check_to_need_theme_for_group(date, time, group, theme)
                                if feedback == True:
                                    return feedback
                            else:
                                print('Эта группа прошла все темы курса, либо в программе что-то сбилось')
                                return False

                for group in course.groups:
                    feedback = check_for_free_group(date, time, group)
                    if feedback == True:
                        return feedback
                else:
                    print('Все подходящие группы в данный момент заняты')
                    return False

            for lesson in planner.freeschedule.loc[date, time]:
                if cabinet.name == lesson.classroom.name:
                    print('Этот кабинет в данный момент занят')
                    return False
                else:
                    print('Кабинет свободен, ведем проверку необходимости')
                    for course in cabinet.courses:
                        feedback = check_for_free_course_groups(date, time, course)
                        if feedback == True:
                            return feedback
            else:
                print('Группам этого курса ничего не надо.')
                return False

        __________________________________________________

        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$       Венгерский алгоритм O(n^3) Для каждой матрицы
        """

        def check_for_free_classrooms(date, time, classrooms, schedule):
            lock_names = []
            free_classrooms = []
            for lesson in schedule.loc[date, time]:
                lock_names.append(lesson.name)

            for classroom in classrooms:
                if classroom.name not in lock_names:
                    free_classrooms.append(classroom)

            return free_classrooms

        def reverse_matrix(matrix_np):
            max = np.max(matrix_np)
            return np.fromiter(map(lambda el: max - el, matrix_np))


        def square_matrix(matrix_pd):

            w = len(matrix_pd.columns)
            h = len(matrix_pd.index)

            for i in range(w - h):
                matrix_pd.loc['Empty slot ' + str(i)] = 0
            for j in range(h - w):
                matrix_pd['Empty slot ' + str(j)] = 0

            return matrix_pd

        def check_for_need_themes(date, time, groups):
            need_themes = []
            for group in groups:
                 need_themes.append(group.theme) #cделать связность группы и актуальной темы и переделать все циклы под map(lambda...)

            return need_themes

        def calculate_matrix_for_teachers_classrooms(need_themes, teachers, classrooms):
            munkres = Munkres()

            matrix_pd = pd.DataFrame(columns=classrooms.map(lambda c: c.name), index=teachers.map(lambda c: c.name))
            for classroom in enumerate(classrooms):
                for teacher in enumerate(teachers):
                    matrix_pd.iloc[teacher[0], classroom[0]] = set(need_themes) & set(teacher[1].themes) & set(classroom[1].themes)

            matrix_pd = square_matrix(matrix_pd)

            matrix_np_with_themes = matrix_pd.values
            matrix_np_with_numbers = matrix_np_with_themes.map(lambda themes: len(themes))
            matrix_np = reverse_matrix(matrix_np_with_numbers)
            index = munkres.calculate(matrix_np_with_numbers)

            total = 0
            triplets = []
            for row, column in index:
                value = matrix_pd.iloc[row, column]
                total += value
                triplets.append([matrix_pd.index[row], matrix_pd.columns[column], len(matrix_pd.iloc[row, column]), matrix_pd.iloc[row, column]])
                #print(f'({row}, {column}) -> {total}')
            #print(f'total profit = {total}')

            matrix_triplets = pd.DataFrame(columns=('Учитель', 'Кабинет', 'Кол-во доступных тем', 'Доступные темы:'), data=triplets).sort_values('Доступных тем').reset_index(drop=True)

            #matrix_triplets['Доступные темы'].apply(check_for_intersections, axis=1, raw=True, result_type=None)


            return matrix


        algorithm = Munkres()

        schedule = planner.freeschedule
        ITER = list(schedule.itertuples(index=True))

        for day in ITER:
            for slot in enumerate(day[1:]):
                free_classrooms = check_for_free_classrooms(day[0], slot[0], planner.classrooms, schedule)



