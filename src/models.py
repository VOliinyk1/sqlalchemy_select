from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import declarative_base, relationship

from src.db import engine

Base = declarative_base()


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    group_id = Column(Integer, ForeignKey('students_groups.id', ondelete='CASCADE'))
    group = relationship('StudentsGroups', backref='students')


class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)


class Discipline(Base):
    __tablename__ = 'disciplines'
    id = Column(Integer, primary_key=True)
    name = Column(String(120), unique=True, nullable=False)
    teacher_id = Column('teacher_id', ForeignKey("teachers.id", ondelete="CASCADE"))
    teacher = relationship('Teacher', backref='disciplines')


class StudentsGroups(Base):
    __tablename__ = 'students_groups'
    id = Column(Integer, primary_key=True)
    name = Column(String(25))


class Grade(Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True)
    grade = Column('grade', Integer)
    date_of = Column('date_of', Date, nullable=True)
    student_id = Column('student_id', ForeignKey('students.id', ondelete='CASCADE'))
    discipline_id = Column('discipline_id', ForeignKey('disciplines.id', ondelete='CASCADE'))
    student = relationship('Student', backref='grade')
    discipline = relationship('Discipline', backref='grade')


Base.metadata.create_all(engine)
