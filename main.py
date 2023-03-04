from sqlalchemy import func, desc, and_

from src.models import Teacher, Student, Discipline, Grade
from src.db import session


def select_one():
    """
    Найти 5 студентов с наибольшим средним баллом по всем предметам.
    :return: list[dict]
    """

    result = session.query(Student.name, func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
        .select_from(Grade).join(Student).group_by(Student.id).order_by(desc('avg_grade')).limit(5).all()

    return result


def select_two(discipline_id):
    """
    Найти студента с наивысшим средним баллом по определенному предмету.
    :return: list[dict]
    """

    result = session.query(Discipline.name, Student.name, func.avg(Grade.grade).label('avg_grade')) \
        .select_from(Grade) \
        .join(Student) \
        .join(Discipline) \
        .filter(Discipline.id == discipline_id) \
        .group_by(Student.id, Discipline.name) \
        .order_by(desc('avg_grade')) \
        .limit(1).all()
    return result


def select_three(subj_name):
    """
    Найти средний балл в группах по определенному предмету.
    :return: list[dict]
    """
    result = session.query(Student.group_id, Discipline.name, func.avg(Grade.grade).label('avg_grade')) \
        .select_from(Student) \
        .join(Grade) \
        .join(Discipline) \
        .filter(Discipline.name == subj_name) \
        .group_by(Student.group_id, Discipline.name).all()
    return result


def select_four():
    """
    Найти средний балл на потоке (по всей таблице оценок).
    :return: list[dict]
    """

    result = session.query(func.avg(Grade.grade)).all()

    return result


def select_five(teacher_id):
    """
    Найти какие курсы читает определенный преподаватель.
    :return: list[dict]
    """

    result = session.query(Teacher.name, Discipline.name) \
        .select_from(Teacher) \
        .join(Discipline) \
        .filter(Teacher.id == teacher_id).all()

    return result


def select_six(group_id):
    """
    Найти список студентов в определенной группе.
    :return: list[dict]
    """

    result = session.query(Student.name) \
        .select_from(Student) \
        .filter(Student.group_id == group_id).all()

    return result


def select_seven(group_id, discipline_id):
    """
    Найти список студентов в определенной группе.
    :return: list[dict]
    """

    result = session.query(Grade.grade) \
        .select_from(Grade) \
        .join(Student) \
        .filter(and_(Student.group_id == group_id, Grade.discipline_id == discipline_id)).all()

    return result


def select_eight(teacher_id):
    """
    Найти средний балл, который ставит определенный преподаватель по своим предметам.
    :return: list[dict]
    """

    result = session.query(Teacher.name, Discipline.name, func.avg(Grade.grade).label('avg_grade')) \
        .select_from(Teacher) \
        .join(Discipline) \
        .join(Grade) \
        .filter(Discipline.teacher_id == teacher_id) \
        .group_by(Discipline.name, Teacher.name).all()
    return result


def select_nine(student_id):
    """
    Найти средний балл, который ставит определенный преподаватель по своим предметам.
    :return: list[dict]
    """

    result = session.query(Grade.student_id, Discipline.name) \
        .select_from(Discipline) \
        .join(Grade) \
        .filter(Grade.student_id == student_id) \
        .group_by(Discipline.name, Grade.student_id).all()
    return result


def select_ten(teacher_id, student_id):
    """
    Найти средний балл, который ставит определенный преподаватель по своим предметам.
    :return: list[dict]
    """

    result = session.query(Discipline.name, Teacher.name) \
        .select_from(Grade) \
        .join(Discipline) \
        .join(Teacher) \
        .filter(and_(Grade.student_id == student_id, Teacher.id == teacher_id)) \
        .group_by(Discipline.name, Teacher.name).all()
    return result


if __name__ == "__main__":
    print(select_one())
    print(select_two(1))
    print(select_three('trigonometry'))
    print(select_four())
    print(select_five(2))
    print(select_six(3))
    print(select_seven(3, 5))
    print(select_eight(3))
    print(select_nine(4))
    print(select_ten(3, 5))
