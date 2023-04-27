import logging
from random import choice

from datacenter.models import Schoolkid, Mark, Lesson, \
    Chastisement, Commendation

logger = logging.getLogger(__name__)
logging.basicConfig(
        format='[%(levelname)s] - %(asctime)s - %(name)s - %(message)s',
        level=logging.ERROR
    )


def check_schoolkid(schoolkid):
    """
    Проверка наличия ученика в списке.
    Если ученика не существует или более 1 - сообщит об ошибке
    """
    try:
        child = Schoolkid.objects.get(
            full_name__icontains=schoolkid
        )
        return child
    except Schoolkid.DoesNotExist:
        logger.error('Ученик с такими данными не существует')
    except Schoolkid.MultipleObjectsReturned:
        logger.error('Найдено более 1 ученика с такими данными')


def fix_marks(schoolkid):
    """
    Исправляем негативные оценки школьника на '5'
    """
    negative_marks = 0
    child = check_schoolkid(schoolkid)
    if child:
        negative_marks = Mark.objects\
            .filter(schoolkid=child, points__lt=4)\
            .update(points=5)
    if bool(negative_marks):
        print('Оценки изменены')
        return
    print('Негативных оценок нет')


def remove_chastisements(schoolkid):
    """
    Удаляем замечания от преподавателей.
    """
    chastisements = 0
    child = check_schoolkid(schoolkid)
    if child:
        chastisements = Chastisement.objects.filter(schoolkid=child)
    if chastisements:
        chastisements.delete()
        print('Замечания удалены')
        return
    print('Нет замечаний')


def create_commendations(schoolkid, subject='Физкультура'):
    """
    Создаем похвалы от препадавателей
    """
    praises = [
        'Молодец!', 'Отлично!', 'Хорошо!', 'Приятно удивлен!',
        'Великолепно!', 'Прекрасно!', 'Ты меня очень обрадовал!',
        'Очень хороший ответ!', 'Замечательно!', 'Так держать!',
        'Ты на верном пути!', 'Здорово!', 'Я тобой горжусь!',
        'Я вижу, как ты стараешься!'
    ]
    child = check_schoolkid(schoolkid)
    if not child:
        return
    stripped_subject = subject.strip()
    if not stripped_subject:
        print('Предмет указан некорректно')
        return
    lessons = Lesson.objects.filter(
        year_of_study=child.year_of_study,
        group_letter=child.group_letter,
        subject__title__icontains=stripped_subject
    )
    if not lessons:
        print('Предмет не найден')
        return
    lesson_for_commendation = lessons.order_by('-date').first()
    commendations = Commendation.objects.filter(
        created=lesson_for_commendation.date,
        schoolkid=child,
        subject=lesson_for_commendation.subject,
        teacher=lesson_for_commendation.teacher
    )
    if not commendations:
        Commendation.objects.create(
            text=choice(praises),
            created=lesson_for_commendation.date,
            schoolkid=child,
            subject=lesson_for_commendation.subject,
            teacher=lesson_for_commendation.teacher
        )
        print('Похвала создана')
        return
    print('Похвала уже существует')
