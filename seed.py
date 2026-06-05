import random
from faker import Faker

from connect import session, engine
from models import Base, Group, Student, Course, Teacher, Grade, student_m2m_course

fake = Faker()


def seed_data():
    try:
        groups = [
            Group(name=f"Group {fake.bothify(text='??-##').upper()}") for _ in range(3)
        ]
        session.add_all(groups)
        session.flush()

        num_teachers = random.randint(3, 5)
        teachers = [Teacher(name=fake.name()) for _ in range(num_teachers)]
        session.add_all(teachers)
        session.flush()

        subject_pool = [
            "Mathematics",
            "Physics",
            "Chemistry",
            "History",
            "Literature",
            "Biology",
            "Computer Science",
            "Geography",
        ]
        num_courses = random.randint(5, 8)
        selected_subjects = random.sample(subject_pool, num_courses)

        courses = []
        for subject_name in selected_subjects:
            teacher = random.choice(teachers)
            courses.append(Course(description=subject_name, teacher=teacher))
        session.add_all(courses)
        session.flush()

        num_students = random.randint(30, 50)
        students = []
        for _ in range(num_students):
            student = Student(
                name=fake.name(),
                group=random.choice(groups),
                created=fake.date_time_between(start_date="-1y", end_date="now"),
            )
            students.append(student)
        session.add_all(students)
        session.flush()

        m2m_rows = []
        grade_objects = []

        for student in students:
            num_student_courses = random.randint(3, len(courses))
            student_courses = random.sample(courses, num_student_courses)

            for course in student_courses:
                m2m_rows.append({"student_id": student.id, "course_id": course.id})

                num_grades = random.randint(1, 5)
                for _ in range(num_grades):
                    grade_objects.append(
                        Grade(
                            student_id=student.id,
                            course_id=course.id,
                            score=random.randint(50, 100),
                            created_at=fake.date_time_between(
                                start_date="-6m", end_date="now"
                            ),
                        )
                    )

        if m2m_rows:
            session.execute(student_m2m_course.insert(), m2m_rows)

        if grade_objects:
            session.add_all(grade_objects)

        session.commit()
        print("The database has been populated with random data.")
        print(f"  Groups:   {len(groups)}")
        print(f"  Teachers: {len(teachers)}")
        print(f"  Courses:  {len(courses)}")
        print(f"  Students: {len(students)}")
        print(f"  Grades:   {len(grade_objects)}")

    except Exception as e:
        session.rollback()
        print(f"An error occurred while seeding the database: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    seed_data()
