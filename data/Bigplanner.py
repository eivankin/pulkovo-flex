
from glob import glob
import os
import pandas as pd


db_example = 'тут будет прикрепленная дбшка по которой буду исправлять логику'

class Planner:
    def __init__(planner, db):
        planner.teachers = db['Teachers']
        planner.subjects = db['Subjects']
        planner.scheduletemplate = db['ScheduleTemplate']
        planner.courses = db['Courses']
        planner.coursethemes = db['CoursThemes']
        planner.classroms = db['Classrooms']
        planner.lessons = db['Lessons']                                         #Мб на русском
        planner.vacations = db['Vacations']
        planner.days = db['Days']
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


    def planning_a_schedule(planner):
        free = []
        workdays = []

        for day in planner.days:
            if day.is_holiday == False:
                workdays.append((day.date, )) # надо сделать через производственный календарь - https://isdayoff.ru/extapi/
            """
        dayschedule = ['09.00-09.20',
                       '09.20-09.40',
                       '09.40-10.00',
                       '10.00-10.20',
                       '10.20-10.40',
                       '10.40-11.00',
                       '11.00-11.20',
                       '11.20-11.40',
                       '11.40-12.00',
                       '12.00-12.20',
                       '12.20-12.40',
                       '12.40-13.00',
                       '13.00-13.20',
                       '13.20-13.40',
                       '13.40-14.00',
                       '14.00-14.20',
                       '14.20-14.40',
                       '14.40-15.00',
                       '15.00-15.20',
                       '15.20-15.40',
                       '15.40-16.00'
                       ]
        """
        dayschedule = ['09.00-09.30',
                       '09.30-10.00',
                       '10.00-10.30',
                       '10.30-11.00',
                       '11.00-11.30',
                       '11.30-12.00',
                       '12.00-12.30',
                       '12.30-13.00',       # нид пофиксить и в приоритете ставить так, чтобы учителя сидели в одних и тех же кабинетах,
                       '13.00-13.30',       # а не бегали по всему заведению каждые 30 минут, но пока так, т.к. есть короткие и длинные темы
                       '13.30-14.00',
                       '14.00-14.30',
                       '14.30-15.00',
                       '15.00-15.30',
                       '15.30-16.00'
                       ]

        schedule = pd.DataFrame(columns=workdays, index=dayschedule).fillna(free).T
        ITER = list(schedule.itertuples(index=True))

        for day in ITER:
            for halfhour in enumerate(day[1:]):
                for cabinet in planner.classroms:
                    if cabinet.check_for_free(day[0], halfhour[0]) == True:     #проверка доступности кабинета, поиск по всем lessonам в это время
                        for courses in cabinet.possible_courses:
                            for course in courses:
                                for themes in course.themes:
                                    for theme in themes:
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
                                                        group.status[1] += 30  #пока пишу цифрами, потом нид переменную ввести и переименовать halfhour

                                                        if group.status[1] >= theme.hours:
                                                            group.status[0] += 1
                                                            group.status[1] = 0
                                                            #нид фидбэк
                                                        break


                                                break
                                                                                         #Добавить элемент рандома, чтобы человеческим глазом подобрать более подходящее расписание




