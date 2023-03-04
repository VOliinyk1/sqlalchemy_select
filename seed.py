from datetime import date, datetime, timedelta
from random import randint, choice
import faker
from sqlalchemy import select

from src.models import Teacher, Student, Discipline, Grade, StudentsGroups
from src.db import session


def date_range(start: date, end:date) -> list:
    result = []
    current_date = start
    while current_date < end:
        if current_date.isoweekday() < 6:
            result.append(current_date)
        current_date += timedelta(1)
    return result


def fill_fake_data(number_students=40, number_teachers=6):
    subjects = ['trigonometry', 'biology', 'calculus', 'data analysis', 'statistics', 'philosophy', 'algorithms']
    groups = ['first', 'second', 'third']

    fake_data = faker.Faker()

    def seed_students():
        for _ in range(number_students):
            student = Student(name=fake_data.name(),
                              group_id=randint(1, 3))
            session.add(student)
        session.commit()

    def seed_teachers():
        for _ in range(number_teachers):
            teacher = Teacher(name=fake_data.name())
            session.add(teacher)
        session.commit()

    def seed_discipline():
        teacher_ids = session.scalars(select(Teacher.id)).all()
        for discipline in subjects:
            session.add(Discipline(name=discipline, teacher_id=choice(teacher_ids)))
        session.commit()

    def seed_groups():
        for group in groups:
            session.add(StudentsGroups(name=group))
        session.commit()

    def seed_grades():
        start_date = datetime.strptime('2020-09-01', '%Y-%m-%d')

        end_date = datetime.strptime('2021-05-25', '%Y-%m-%d')
        d_range = date_range(start=start_date, end=end_date)
        discipline_ids = session.scalars(select(Discipline.id)).all()
        student_ids = session.scalars(select(Student.id)).all()

        for d in d_range:
            random_id_discipline = choice(discipline_ids)
            random_ids_student = [choice(student_ids) for _ in range(5)]

            for student_id in random_ids_student:
                grade = Grade(
                    grade=randint(1, 5),
                    date_of=d,
                    student_id=student_id,
                    discipline_id=random_id_discipline
                )
                session.add(grade)
        session.commit()

    seed_teachers()
    seed_discipline()
    seed_groups()
    seed_students()
    seed_grades()


if __name__ == "__main__":
    fill_fake_data()

