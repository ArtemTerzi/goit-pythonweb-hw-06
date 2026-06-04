from sqlalchemy import func, desc, select

from connect import session
from models import Base, Group, Student, Course, Teacher, student_m2m_course


def select_1():
    avg_score = func.round(func.avg(student_m2m_course.c.score), 2).label("avg_score")

    result = (
        session.query(Student, avg_score)
        .join(student_m2m_course, Student.id == student_m2m_course.c.student_id)
        .group_by(Student.id)
        .order_by(desc("avg_score"))
        .limit(5)
        .all()
    )

    return result


def select_2(course_id):
    avg_score = func.round(func.avg(student_m2m_course.c.score), 2).label("avg_score")

    stmt = (
        select(Student, avg_score)
        .join(student_m2m_course, Student.id == student_m2m_course.c.student_id)
        .filter(student_m2m_course.c.course_id == course_id)
        .group_by(Student.id)
        .order_by(desc("avg_score"))
        .limit(1)
    )

    result = session.execute(stmt).first()
    return result


def select_3(course_id):
    avg_score = func.round(func.avg(student_m2m_course.c.score), 2).label("avg_score")

    stmt = (
        select(Group.name, avg_score)
        .select_from(student_m2m_course)
        .join(Student, Student.id == student_m2m_course.c.student_id)
        .join(Group, Group.id == Student.group_id)
        .filter(student_m2m_course.c.course_id == course_id)
        .group_by(Group.id)
        .order_by(Group.name)
    )

    result = session.execute(stmt).all()
    return result


def select_4():
    stmt = select(func.round(func.avg(student_m2m_course.c.score), 2))

    result = session.execute(stmt).scalar()
    return result


def select_5(teacher_id):
    stmt = select(Course.description).filter(Course.teacher_id == teacher_id)
    return session.execute(stmt).all()


def select_6(group_id):
    stmt = (
        select(Student.name).filter(Student.group_id == group_id).order_by(Student.name)
    )
    return session.execute(stmt).all()


def select_7(group_id, course_id):
    stmt = (
        select(Student.name, student_m2m_course.c.score)
        .join(student_m2m_course, Student.id == student_m2m_course.c.student_id)
        .filter(
            Student.group_id == group_id, student_m2m_course.c.course_id == course_id
        )
        .order_by(Student.name)
    )
    return session.execute(stmt).all()


def select_8(teacher_id):
    stmt = (
        select(func.round(func.avg(student_m2m_course.c.score), 2))
        .select_from(student_m2m_course)
        # Об'єднуємо оцінки з курсами, щоб перевірити, хто викладач
        .join(Course, Course.id == student_m2m_course.c.course_id)
        .filter(Course.teacher_id == teacher_id)
    )
    return session.execute(stmt).scalar()


def select_9(student_id):
    stmt = (
        select(Course.description)
        .join(student_m2m_course, Course.id == student_m2m_course.c.course_id)
        .filter(student_m2m_course.c.student_id == student_id)
        .order_by(Course.description)
    )
    return session.execute(stmt).all()


def select_10(student_id, teacher_id):
    stmt = (
        select(Course.description)
        .join(student_m2m_course, Course.id == student_m2m_course.c.course_id)
        # Фільтруємо за студентом та викладачем курсу одночасно
        .filter(
            student_m2m_course.c.student_id == student_id,
            Course.teacher_id == teacher_id,
        )
        .order_by(Course.description)
    )
    return session.execute(stmt).all()


def select_additional_1(student_id, teacher_id):
    stmt = (
        select(func.round(func.avg(student_m2m_course.c.score), 2))
        .select_from(student_m2m_course)
        .join(Course, Course.id == student_m2m_course.c.course_id)
        .filter(
            student_m2m_course.c.student_id == student_id,
            Course.teacher_id == teacher_id,
        )
    )
    return session.execute(stmt).scalar()


def select_additional_2(group_id, course_id):
    subq = (
        select(func.max(student_m2m_course.c.created))
        .join(Student, Student.id == student_m2m_course.c.student_id)
        .filter(
            Student.group_id == group_id, student_m2m_course.c.course_id == course_id
        )
        .scalar_subquery()
    )

    stmt = (
        select(Student.name, student_m2m_course.c.score, student_m2m_course.c.created)
        .join(student_m2m_course, Student.id == student_m2m_course.c.student_id)
        .filter(
            Student.group_id == group_id,
            student_m2m_course.c.course_id == course_id,
            student_m2m_course.c.created == subq,
        )
    )
    return session.execute(stmt).all()


if __name__ == "__main__":
    # 1. 5 students with the highest average score in all courses.
    print(
        "--------------- 1. 5 students with the highest average score in all courses-----------------"
    )
    top_students = select_1()
    for student, avg in top_students:
        print(f"Student: {student.name:<25} | Average Score: {avg}")

    # 2. The student with the highest grade point average in a particular course.
    print(
        "--------------- 2. The student with the highest grade point average in a particular course.-----------------"
    )
    course_id_to_check = 1
    best_student_data = select_2(course_id_to_check)

    if best_student_data:
        student, avg_score = best_student_data
        print(f"The best student in course #{course_id_to_check}:")
        print(f"Name: {student.name} | Average score: {avg_score}")
    else:
        print(f"No grades found for course with ID {course_id_to_check}.")

    # 3 Average score in groups in a particular subject.
    print(
        "--------------- 3 Average score in groups in a particular subject.-----------------"
    )
    group_averages = select_3(course_id_to_check)

    if group_averages:
        print(f"Average score in groups for course #{course_id_to_check}:")
        for group_name, avg_score in group_averages:
            print(f"Group: {group_name:<12} | Average score: {avg_score}")
    else:
        print(f"No grades found in any group for course with ID {course_id_to_check}.")

    # 4 Average score on the stream (across the entire grading scale).
    print(
        "--------------- 4 Average score on the stream (across the entire grading scale)-----------------"
    )
    overall_average = select_4()

    if overall_average is not None:
        print(
            f"Overall average score across all students and courses: {overall_average}"
        )
    else:
        print("No grades found in the database.")

    # 5 What courses a particular teacher teaches.
    print(
        "--------------- 5 What courses a particular teacher teaches.-----------------"
    )
    teacher_id = 2
    courses = select_5(teacher_id)
    print(f"Courses taught by teacher #{teacher_id}:")
    for (course_name,) in courses:
        print(f"- {course_name}")

    # 6 A list of students in a particular group.
    print(
        "--------------- 6 A list of students in a particular group.-----------------"
    )
    group_id = 1
    students = select_6(group_id)
    print(f"Students in group #{group_id}:")
    for (student_name,) in students:
        print(f"- {student_name}")

    # 7 The grades of students in a particular group in a particular subject.
    print(
        "--------------- 7 The grades of students in a particular group in a particular subject.-----------------"
    )
    group_id, course_id = 1, 1
    grades = select_7(group_id, course_id)
    print(f"Grades in group #{group_id} for course #{course_id}:")
    for student_name, score in grades:
        print(f"Student: {student_name:<25} | Score: {score}")

    # 8 The average grade that a particular teacher gives in his subjects.
    print(
        "--------------- 8 The average grade that a particular teacher gives in his subjects.-----------------"
    )
    teacher_id = 1
    avg_score = select_8(teacher_id)
    if avg_score is not None:
        print(f"Average score given by teacher #{teacher_id}: {avg_score}")
    else:
        print(f"No grades found for courses taught by teacher #{teacher_id}.")

    # 9 A list of courses that a particular student attends.
    print(
        "--------------- 9 A list of courses that a particular student attends.-----------------"
    )
    student_id = 1
    courses = select_9(student_id)
    print(f"Courses attended by student #{student_id}:")
    for (course_name,) in courses:
        print(f"- {course_name}")

    # 10 A list of courses that a particular teacher teaches to a particular student.
    print(
        "--------------- 10 A list of courses that a particular teacher teaches to a particular student.-----------------"
    )
    student_id, teacher_id = 1, 1
    courses = select_10(student_id, teacher_id)
    print(f"Courses taught to student #{student_id} by teacher #{teacher_id}:")
    for (course_name,) in courses:
        print(f"- {course_name}")

    # 11 The average grade that a particular teacher gives to a particular student.
    print(
        "--------------- 11 The average grade that a particular teacher gives to a particular student.-----------------"
    )
    s_id, t_id = 1, 1
    avg_score = select_additional_1(s_id, t_id)
    print(f"Average score given by teacher #{t_id} to student #{s_id}: {avg_score}")

    # 12 The grades of students in a particular group in a particular subject in the last class.
    print(
        "--------------- 12 The grades of students in a particular group in a particular subject in the last class.-----------------"
    )
    g_id, c_id = 1, 1
    last_lesson_grades = select_additional_2(g_id, c_id)
    print(f"Grades in group #{g_id} for course #{c_id} on the last lesson:")
    for student_name, score, date in last_lesson_grades:
        print(f"Student: {student_name:<25} | Score: {score} | Date: {date}")
