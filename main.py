import argparse
from sqlalchemy import select
from connect import session
from models import Teacher, Group, Student, Course


def handle_teacher(action, args):
    if action == "create":
        if not args.name:
            print("Error: --name (-n) is required to create a Teacher.")
            return
        teacher = Teacher(name=args.name)
        session.add(teacher)
        session.commit()
        print(f"Successfully created Teacher: ID={teacher.id}, Name='{teacher.name}'")

    elif action == "list":
        stmt = select(Teacher).order_by(Teacher.id)
        teachers = session.execute(stmt).scalars().all()
        for t in teachers:
            print(f"ID: {t.id:<5} | Name: {t.name}")

    elif action == "update":
        if not args.id or not args.name:
            print("Error: both --id and --name (-n) are required for update.")
            return
        teacher = session.get(Teacher, args.id)
        if teacher:
            teacher.name = args.name
            session.commit()
            print(f"Successfully updated Teacher ID={args.id} with Name='{args.name}'")
        else:
            print(f"Teacher with ID={args.id} not found.")

    elif action == "remove":
        if not args.id:
            print("Error: --id is required for removal.")
            return
        teacher = session.get(Teacher, args.id)
        if teacher:
            session.delete(teacher)
            session.commit()
            print(f"Successfully removed Teacher ID={args.id}")
        else:
            print(f"Teacher with ID={args.id} not found.")


def handle_group(action, args):
    if action == "create":
        if not args.name:
            print("Error: --name (-n) is required to create a Group.")
            return
        group = Group(name=args.name)
        session.add(group)
        session.commit()
        print(f"Successfully created Group: ID={group.id}, Name='{group.name}'")

    elif action == "list":
        stmt = select(Group).order_by(Group.id)
        groups = session.execute(stmt).scalars().all()
        for g in groups:
            print(f"ID: {g.id:<5} | Name: {g.name}")

    elif action == "update":
        if not args.id or not args.name:
            print("Error: both --id and --name (-n) are required for update.")
            return
        group = session.get(Group, args.id)
        if group:
            group.name = args.name
            session.commit()
            print(f"Successfully updated Group ID={args.id} with Name='{args.name}'")
        else:
            print(f"Group with ID={args.id} not found.")

    elif action == "remove":
        if not args.id:
            print("Error: --id is required for removal.")
            return
        group = session.get(Group, args.id)
        if group:
            session.delete(group)
            session.commit()
            print(f"Successfully removed Group ID={args.id}")
        else:
            print(f"Group with ID={args.id} not found.")


def handle_student(action, args):
    if action == "create":
        if not args.name:
            print("Error: --name (-n) is required to create a Student.")
            return
        student = Student(name=args.name, group_id=args.group_id)
        session.add(student)
        session.commit()
        print(
            f"Successfully created Student: ID={student.id}, Name='{student.name}', Group ID={student.group_id}"
        )

    elif action == "list":
        stmt = select(Student).order_by(Student.id)
        students = session.execute(stmt).scalars().all()
        for s in students:
            print(f"ID: {s.id:<5} | Name: {s.name:<25} | Group ID: {s.group_id}")

    elif action == "update":
        if not args.id:
            print("Error: --id is required for update.")
            return
        student = session.get(Student, args.id)
        if student:
            if args.name:
                student.name = args.name
            if args.group_id is not None:
                student.group_id = args.group_id
            session.commit()
            print(f"Successfully updated Student ID={args.id}")
        else:
            print(f"Student with ID={args.id} not found.")

    elif action == "remove":
        if not args.id:
            print("Error: --id is required for removal.")
            return
        student = session.get(Student, args.id)
        if student:
            session.delete(student)
            session.commit()
            print(f"Successfully removed Student ID={args.id}")
        else:
            print(f"Student with ID={args.id} not found.")


def handle_course(action, args):
    if action == "create":
        if not args.description or not args.teacher_id:
            print(
                "Error: both --description and --teacher_id are required to create a Course."
            )
            return
        course = Course(description=args.description, teacher_id=args.teacher_id)
        session.add(course)
        session.commit()
        print(
            f"Successfully created Course: ID={course.id}, Description='{course.description}', Teacher ID={course.teacher_id}"
        )

    elif action == "list":
        stmt = select(Course).order_by(Course.id)
        courses = session.execute(stmt).scalars().all()
        for c in courses:
            print(
                f"ID: {c.id:<5} | Description: {c.description:<20} | Teacher ID: {c.teacher_id}"
            )

    elif action == "update":
        if not args.id:
            print("Error: --id is required for update.")
            return
        course = session.get(Course, args.id)
        if course:
            if args.description:
                course.description = args.description
            if args.teacher_id is not None:
                course.teacher_id = args.teacher_id
            session.commit()
            print(f"Successfully updated Course ID={args.id}")
        else:
            print(f"Course with ID={args.id} not found.")

    elif action == "remove":
        if not args.id:
            print("Error: --id is required for removal.")
            return
        course = session.get(Course, args.id)
        if course:
            session.delete(course)
            session.commit()
            print(f"Successfully removed Course ID={args.id}")
        else:
            print(f"Course with ID={args.id} not found.")


def main():
    parser = argparse.ArgumentParser(
        description="CLI program for CRUD operations on Database."
    )

    parser.add_argument(
        "-a",
        "--action",
        choices=["create", "list", "update", "remove"],
        required=True,
        help="CRUD action",
    )

    parser.add_argument(
        "-m",
        "--model",
        choices=["Teacher", "Group", "Student", "Course"],
        required=True,
        help="Database model",
    )

    parser.add_argument(
        "--id", type=int, help="Identifier of record (needed for update/remove)"
    )

    parser.add_argument(
        "-n", "--name", type=str, help="Name of Teacher, Student or Group"
    )

    parser.add_argument("--group_id", type=int, help="Group ID for Student")

    parser.add_argument("--teacher_id", type=int, help="Teacher ID for Course")

    parser.add_argument("--description", type=str, help="Description for Course")

    args = parser.parse_args()

    if args.model == "Teacher":
        handle_teacher(args.action, args)
    elif args.model == "Group":
        handle_group(args.action, args)
    elif args.model == "Student":
        handle_student(args.action, args)
    elif args.model == "Course":
        handle_course(args.action, args)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        session.close()
