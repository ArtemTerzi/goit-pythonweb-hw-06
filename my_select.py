from sqlalchemy import func, desc, select

from connect import session
from models import Base, Group, Student, Course, Teacher, Grade, student_m2m_course


def select_1():
    # 1. 5 students with the highest average score in all courses.
    avg_score = func.round(func.avg(Grade.score), 2).label("avg_score")

    stmt = (
        select(Student, avg_score)
        .join(Grade, Student.id == Grade.student_id)
        .group_by(Student.id)
        .order_by(desc("avg_score"))
        .limit(5)
    )

    return session.execute(stmt).all()


def select_2(course_id):
    # 2. The student with the highest grade point average in a particular course.
    avg_score = func.round(func.avg(Grade.score), 2).label("avg_score")

    stmt = (
        select(Student, avg_score)
        .join(Grade, Student.id == Grade.student_id)
        .filter(Grade.course_id == course_id)
        .group_by(Student.id)
        .order_by(desc("avg_score"))
        .limit(1)
    )

    return session.execute(stmt).first()


def select_3(course_id):
    # 3. Average score in groups in a particular subject.
    avg_score = func.round(func.avg(Grade.score), 2).label("avg_score")

    stmt = (
        select(Group.name, avg_score)
        .join(Student, Student.group_id == Group.id)
        .join(Grade, Grade.student_id == Student.id)
        .filter(Grade.course_id == course_id)
        .group_by(Group.id)
        .order_by(Group.name)
    )

    return session.execute(stmt).all()


def select_4():
    # 4.  Average score on the stream (across the entire grading scale).
    stmt = select(func.round(func.avg(Grade.score), 2))
    return session.execute(stmt).scalar()


def select_5(teacher_id):
    # 5. What courses a particular teacher teaches.
    stmt = select(Course.description).filter(Course.teacher_id == teacher_id)
    return session.execute(stmt).all()


def select_6(group_id):
    # 6. A list of students in a particular group.
    stmt = (
        select(Student.name).filter(Student.group_id == group_id).order_by(Student.name)
    )
    return session.execute(stmt).all()


def select_7(group_id, course_id):
    # 7. The grades of students in a particular group in a particular subject.
    stmt = (
        select(Student.name, Grade.score, Grade.created_at)
        .join(Grade, Student.id == Grade.student_id)
        .filter(Student.group_id == group_id, Grade.course_id == course_id)
        .order_by(Student.name, Grade.created_at)
    )
    return session.execute(stmt).all()


def select_8(teacher_id):
    # 8. The average grade that a particular teacher gives in his subjects.
    stmt = (
        select(func.round(func.avg(Grade.score), 2))
        .join(Course, Course.id == Grade.course_id)
        .filter(Course.teacher_id == teacher_id)
    )
    return session.execute(stmt).scalar()


def select_9(student_id):
    # 9. A list of courses that a particular student attends.
    stmt = (
        select(Course.description)
        .join(student_m2m_course, Course.id == student_m2m_course.c.course_id)
        .filter(student_m2m_course.c.student_id == student_id)
        .order_by(Course.description)
    )
    return session.execute(stmt).all()


def select_10(student_id, teacher_id):
    # 10. A list of courses that a particular teacher teaches to a particular student.
    stmt = (
        select(Course.description)
        .join(student_m2m_course, Course.id == student_m2m_course.c.course_id)
        .filter(
            student_m2m_course.c.student_id == student_id,
            Course.teacher_id == teacher_id,
        )
        .order_by(Course.description)
    )
    return session.execute(stmt).all()


def select_additional_1(student_id, teacher_id):
    # 11. The average grade that a particular teacher gives to a particular student.
    stmt = (
        select(func.round(func.avg(Grade.score), 2))
        .join(Course, Course.id == Grade.course_id)
        .filter(
            Grade.student_id == student_id,
            Course.teacher_id == teacher_id,
        )
    )
    return session.execute(stmt).scalar()


def select_additional_2(group_id, course_id):
    # 12. The grades of students in a particular group in a particular subject in the last class.
    subq = (
        select(func.max(Grade.created_at))
        .join(Student, Student.id == Grade.student_id)
        .filter(Student.group_id == group_id, Grade.course_id == course_id)
        .scalar_subquery()
    )

    stmt = (
        select(Student.name, Grade.score, Grade.created_at)
        .join(Grade, Student.id == Grade.student_id)
        .filter(
            Student.group_id == group_id,
            Grade.course_id == course_id,
            Grade.created_at == subq,
        )
    )
    return session.execute(stmt).all()


if __name__ == "__main__":
    # 1. 5 students with the highest average score in all courses.
    print("--- 1. 5 students with the highest average score in all courses. ---")
    for student, avg in select_1():
        print(f"  {student.name:<25} | Середній бал: {avg}")

    # 2. The student with the highest grade point average in a particular course.
    print(
        "\n--- 2. The student with the highest grade point average in a particular course ---"
    )
    result = select_2(1)
    if result:
        student, avg = result
        print(f"  {student.name} | Середній бал: {avg}")

    # 3. Average score in groups in a particular subject.
    print("\n--- 3. Average score in groups in a particular subject. ---")
    for group_name, avg in select_3(1):
        print(f"  {group_name:<12} | {avg}")

    # 4.  Average score on the stream (across the entire grading scale).
    print(
        "\n--- 4.  Average score on the stream (across the entire grading scale). ---"
    )
    print(f"  {select_4()}")

    # 5. What courses a particular teacher teaches.
    print("\n--- 5. What courses a particular teacher teaches. ---")
    for (name,) in select_5(2):
        print(f"  - {name}")

    # 6 A list of students in a particular group.
    print("\n---- 6 A list of students in a particular group.---")
    for (name,) in select_6(1):
        print(f"  - {name}")

    # 7. The grades of students in a particular group in a particular subject.
    print(
        "\n--- 7. The grades of students in a particular group in a particular subject. ---"
    )
    for name, score, date in select_7(1, 1):
        print(f"  {name:<25} | {score} | {date}")

    # 8. The average grade that a particular teacher gives in his subjects.
    print(
        "\n--- 8. The average grade that a particular teacher gives in his subjects.---"
    )
    print(f"  {select_8(2)}")

    # 9. A list of courses that a particular student attends.
    print(
        "--------------- 9. A list of courses that a particular student attends.-----------------"
    )
    for (name,) in select_9(1):
        print(f"  - {name}")

    # 10. A list of courses that a particular teacher teaches to a particular student.
    print(
        "--------------- 10. A list of courses that a particular teacher teaches to a particular student.-----------------"
    )
    for (name,) in select_10(1, 2):
        print(f"  - {name}")

    # 11. The average grade that a particular teacher gives to a particular student.
    print(
        "--------------- 11. The average grade that a particular teacher gives to a particular student.-----------------"
    )
    print(f"  {select_additional_1(1, 2)}")

    # 12. The grades of students in a particular group in a particular subject in the last class.
    print(
        "--------------- 12. The grades of students in a particular group in a particular subject in the last class.-----------------"
    )
    for name, score, date in select_additional_2(1, 1):
        print(f"  {name:<25} | {score} | {date}")
