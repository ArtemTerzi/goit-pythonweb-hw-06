from datetime import datetime

from sqlalchemy import (
    ForeignKey,
    Table,
    Column,
    Integer,
    PrimaryKeyConstraint,
    func,
    DateTime,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


student_m2m_course = Table(
    "student_m2m_course",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id", ondelete="CASCADE")),
    Column("course_id", Integer, ForeignKey("courses.id", ondelete="CASCADE")),
    PrimaryKeyConstraint("student_id", "course_id"),
)


class Group(Base):
    __tablename__ = "groups"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    students: Mapped[list["Student"]] = relationship(back_populates="group")


class Student(Base):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    created: Mapped[datetime] = mapped_column(default=func.now())
    group_id: Mapped[int | None] = mapped_column(
        ForeignKey("groups.id", ondelete="SET NULL"), nullable=True
    )
    group: Mapped["Group"] = relationship(back_populates="students")
    courses: Mapped[list["Course"]] = relationship(
        secondary=student_m2m_course, back_populates="students"
    )
    grades: Mapped[list["Grade"]] = relationship(back_populates="student")


class Course(Base):
    __tablename__ = "courses"
    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(nullable=False)
    teacher_id: Mapped[int] = mapped_column(
        ForeignKey("teachers.id", ondelete="CASCADE")
    )
    teacher: Mapped["Teacher"] = relationship(back_populates="courses")
    students: Mapped[list["Student"]] = relationship(
        secondary=student_m2m_course, back_populates="courses"
    )
    grades: Mapped[list["Grade"]] = relationship(back_populates="course")


class Teacher(Base):
    __tablename__ = "teachers"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    courses: Mapped[list["Course"]] = relationship(back_populates="teacher")


class Grade(Base):
    __tablename__ = "grades"
    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.id", ondelete="CASCADE"), nullable=False
    )
    course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.id", ondelete="CASCADE"), nullable=False
    )
    score: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=func.now())

    student: Mapped["Student"] = relationship(back_populates="grades")
    course: Mapped["Course"] = relationship(back_populates="grades")
