import os
import random

from datacenter.models import (Chastisement, Commendation, Lesson, Mark,
                               Schoolkid)
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from dotenv import load_dotenv


PRAISES = [
    'Молодец!', 'Отлично!','Хорошо!','Гораздо лучше, чем я ожидал!','Ты меня приятно удивил!','Великолепно!',
    'Прекрасно!','Ты меня очень обрадовал!','Именно этого я давно ждал от тебя!','Сказано здорово – просто и ясно!',
    'Ты, как всегда, точен!','Очень хороший ответ!','Талантливо!','Ты сегодня прыгнул выше головы!','Я поражен!',
    'Уже существенно лучше!','Потрясающе!','Замечательно!','Прекрасное начало!','Так держать!','Ты на верном пути!',
    'Здорово!','Это как раз то, что нужно!','Я тобой горжусь!','С каждым разом у тебя получается всё лучше!',
    'Мы с тобой не зря поработали!','Я вижу, как ты стараешься!','Ты растешь над собой!','Ты многое сделал, я это вижу!',
    'Теперь у тебя точно все получится!',
]
    
    
def fix_marks(schoolkid):
    poor_grades = Mark.objects.filter(schoolkid=schoolkid, points__in=[2,3]).update(points=5)
        
        
def remove_chastisements(schoolkid):
    bad_remarks = Chastisement.objects.filter(schoolkid=schoolkid)
    bad_remarks.delete()
    
    
def create_commendation(schoolkid, lesson):
    text_praise = random.choice(PRAISES)

    subject_at_school = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject__title=lesson
    ).first()

    if subject_at_school:
        Commendation.objects.create(
            text=text_praise,
            created=subject_at_school.date,
            schoolkid=schoolkid,
            subject=subject_at_school.subject,
            teacher=subject_at_school.teacher
        )


def find_student_by_name(name):
    student = Schoolkid.objects.get(full_name=name)
    return student

    
def main():
    load_dotenv()
    
    name = os.getenv('NAME')
    lesson = os.getenv('LESSON')
    
    if not name or not lesson:
        print("Не указаны переменные окружения.")
        return
    
    try:
        student = find_student_by_name(name)
        fix_marks(student)
        remove_chastisements(student)
        create_commendation(student, lesson)
    except Schoolkid.MultipleObjectsReturned:
        print(f"Найдены ученики с именем '{name}'. Пожалуйста, уточните запрос.")
        return None
    except Schoolkid.DoesNotExist:
        print(f"Ученика с именем '{name}' не существует.")
        return None
    

if __name__ == '__main__':
    main()