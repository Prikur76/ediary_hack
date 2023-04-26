import logging
from random import choice

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from datacenter.models import Schoolkid, Mark, Lesson, \
    Chastisement, Commendation


logger = logging.getLogger(__name__)
logging.basicConfig(
        format='[%(levelname)s] - %(asctime)s - %(name)s - %(message)s',
        level=logging.ERROR
    )


def fix_marks(schoolkid):
    """
    Исправляем негативные оценки школьника на '5'
    Если ученика не существует или более 1 - выбросит исключение
    """
    try:
        child = Schoolkid.objects.get(
            full_name__contains=schoolkid.title()
        )
        negative_marks = Mark.objects.filter(schoolkid=child, points__lt=4)
        if negative_marks:
            for mark in negative_marks:
                mark.points = 5
                mark.save()
            print('Оценки изменены')
        else:
            print('Негативных оценок нет')
    except ObjectDoesNotExist:
        logger.error('Ученик с такими данными не существует')
    except MultipleObjectsReturned:
        logger.error('Найдено более 1 ученика с такими данными')


def remove_chastisements(schoolkid):
    """
    Удаляем замечания от преподавателей.
    Если ученика не существует или более 1 - выбросит исключение
    """
    try:
        child = Schoolkid.objects.get(
            full_name__contains=schoolkid.title()
        )
        chastisements = Chastisement.objects.filter(schoolkid=child)
        if chastisements:
            chastisements.delete()
            print('Замечания удалены')
        else:
            print('Нет замечаний')
    except ObjectDoesNotExist:
        logger.error('Ученик с такими данными не существует')
    except MultipleObjectsReturned:
        logger.error('Найдено более 1 ученика с такими данными')


def create_commendations(schoolkid, subject='Физкультура'):
    """
    Создаем похвалы от препадавателей
    """
    praises = [
        'Молодец!', 'Отлично!', 'Хорошо!',
        'Приятно удивлен!', 'Великолепно!', 'Прекрасно!',
        'Ты меня очень обрадовал!', 'Очень хороший ответ!',
        'Замечательно!', 'Так держать!', 'Ты на верном пути!',
        'Здорово!', 'Я тобой горжусь!', 'Я вижу, как ты стараешься!'
    ]
    try:
        child = Schoolkid.objects.get(
            full_name__contains=schoolkid.title()
        )
        transform_subject = subject.strip().capitalize()
        if transform_subject:
            lessons = Lesson.objects.filter(
                year_of_study=child.year_of_study,
                group_letter=child.group_letter,
                subject__title__contains=transform_subject
            )
            if lessons:
                lesson_for_commendation = Lesson.objects.filter(
                    year_of_study=child.year_of_study,
                    group_letter=child.group_letter,
                    subject__title__contains=transform_subject
                ).order_by('-date').first()

                commendations = Commendation.objects.filter(
                    created=lesson_for_commendation.date,
                    schoolkid=child,
                    subject=lesson_for_commendation.subject,
                    teacher=lesson_for_commendation.teacher
                )

                if commendations:
                    print('Похвала уже существует')
                else:
                    Commendation.objects.create(
                        text=choice(praises),
                        created=lesson_for_commendation.date,
                        schoolkid=child,
                        subject=lesson_for_commendation.subject,
                        teacher=lesson_for_commendation.teacher
                    )
                    print('Похвала создана')
            else:
                print('Предмет не найден')
        else:
            print('Предмет указан некорректно')
    except ObjectDoesNotExist:
        logger.error('Ученик с такими данными не существует')
    except MultipleObjectsReturned:
        logger.error('Найдено более 1 ученика с такими данными')
