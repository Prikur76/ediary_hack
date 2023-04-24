from random import choice

from datacenter.models import Schoolkid, Mark, Lesson, Chastisement, Commendation


def fix_marks(schoolkid):
    """
    Исправляем негативные оценки школьника на '5'
    """
    child = Schoolkid.objects.get(full_name__contains=schoolkid)
    child_marks = Mark.objects.filter(schoolkid=child.id, points__lt=4)
    for mark in child_marks:
        mark.points = 5
        mark.save()


def remove_chastisements(schoolkid):
    """
    Удаляем замечания от препадавателей
    """
    child = Schoolkid.objects.get(full_name__contains=schoolkid)
    Chastisement.objects.filter(schoolkid=child.id).delete()


def create_commendations(schoolkid, lesson):
    """
    Создаем похвалы от препадавателей
    """
    praises = [
        'Молодец!', 'Отлично!', 'Хорошо!', 'Гораздо лучше, чем ожидалось!',
        'Приятно удивлен!', 'Великолепно!', 'Прекрасно!',
        'Ты меня очень обрадовал!', 'Ты, как всегда, точен!',
        'Очень хороший ответ!', 'Ты сегодня прыгнул выше головы!',
        'Уже существенно лучше!', 'Замечательно!', 'Прекрасное начало!',
        'Так держать!', 'Ты на верном пути!', 'Здорово!',
        'Это как раз то, что нужно!', 'Я тобой горжусь!',
        'С каждым разом у тебя получается всё лучше!',
        'Мы с тобой не зря поработали!', 'Я вижу, как ты стараешься!',
        'Ты растешь над собой!', 'Ты многое сделал, я это вижу!',
        'Теперь у тебя точно все получится!'
    ]
    child = Schoolkid.objects.get(full_name__contains=schoolkid)

    lesson = Lesson.objects.filter(
        year_of_study=child.year_of_study,
        group_letter=child.group_letter,
        subject__title=subject
    ).order_by('date').first()

    Commendation.objects.create(
        text=choice(praises),
        created=lesson.date,
        schoolkid=child,
        subject=lesson.subject,
        teacher=lesson.teacher
    )
