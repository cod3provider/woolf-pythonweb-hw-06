from sqlalchemy.orm import aliased, sessionmaker
from sqlalchemy import func
from models import Student, Group, Teacher, Subject, Grade, init_db
from colorama import Fore, Style, init

engine = init_db()
Session = sessionmaker(bind=engine)
session = Session()

init(autoreset=True)


def round_results(results):
    if isinstance(results, tuple):
        return tuple(
            round(value, 2) if isinstance(value, float) else value for value in results
        )
    elif isinstance(results, list):
        return [round_results(result) for result in results]
    return results


def select_1():
    result = (
        session.query(Student.name, func.avg(Grade.grade).label("average_grade"))
        .join(Grade)
        .group_by(Student.id)
        .order_by(func.avg(Grade.grade).desc())
        .limit(5)
        .all()
    )
    return round_results(result)


def select_2(subject_name):
    result = (
        session.query(Student.name, func.avg(Grade.grade).label("average_grade"))
        .join(Grade)
        .join(Subject)
        .filter(Subject.name == subject_name)
        .group_by(Student.id)
        .order_by(func.avg(Grade.grade).desc())
        .first()
    )
    if result:
        return round_results([result])[0]
    return result


def select_3(subject_name):
    SubjectAlias = aliased(Subject)

    query = (
        session.query(Group.name, func.avg(Grade.grade).label("average_grade"))
        .select_from(Group)
        .join(Student)
        .join(Grade, Grade.student_id == Student.id)
        .join(SubjectAlias, SubjectAlias.id == Grade.subject_id)
        .filter(SubjectAlias.name == subject_name)
        .group_by(Group.name)
        .all()
    )

    return round_results(query)


def select_4():
    result = session.query(func.avg(Grade.grade).label("average_grade")).scalar()
    if result is not None:
        return round(result, 2)
    return result


def select_5(teacher_name):
    result = (
        session.query(Subject.name)
        .join(Teacher)
        .filter(Teacher.name == teacher_name)
        .all()
    )
    return result


def select_6(group_name):
    result = (
        session.query(Student.name).join(Group).filter(Group.name == group_name).all()
    )
    return result


def select_7(group_name, subject_name):
    result = (
        session.query(Student.name, Grade.grade)
        .join(Group)
        .join(Grade)
        .join(Subject)
        .filter(Group.name == group_name, Subject.name == subject_name)
        .all()
    )
    return result


def select_8(teacher_name):
    result = (
        session.query(func.avg(Grade.grade).label("average_grade"))
        .join(Subject)
        .join(Teacher)
        .filter(Teacher.name == teacher_name)
        .scalar()
    )
    return round(result, 2) if result is not None else result


def select_9(student_name):
    result = (
        session.query(Subject.name)
        .join(Grade)
        .join(Student)
        .filter(Student.name == student_name)
        .all()
    )
    return result


def select_10(student_name, teacher_name):
    result = (
        session.query(Subject.name)
        .join(Grade)
        .join(Student)
        .join(Teacher)
        .filter(Student.name == student_name, Teacher.name == teacher_name)
        .all()
    )
    return result


def print_query_result(query_result, title):
    print(Fore.CYAN + Style.BRIGHT + title)
    if query_result:
        for row in query_result:
            print(Fore.GREEN + str(row))
    else:
        print(Fore.RED + "No results found.")
    print("\n" + "-" * 50)


if __name__ == "__main__":
    print_query_result(select_1(), "Top 5 Students by Average Grade")

    student_2 = select_2("Alchemy")
    if student_2:
        print_query_result([student_2], "Student with Highest Average in Alchemy")
    else:
        print(Fore.RED + "No student found with the highest average in Alchemy.")

    select_3_result = select_3("Potion making")
    if select_3_result:
        print_query_result(select_3_result, "Average Grade by Groups in Potion making")
    else:
        print(Fore.RED + "No groups found for the subject 'Potion making'.")

    overall_avg = select_4()
    if overall_avg is not None:
        print(Fore.YELLOW + f"Overall Average Grade: {overall_avg}")
    else:
        print(Fore.RED + "No average grade found.")

    select_5_result = select_5("George Wilkinson")
    if select_5_result:
        print_query_result(select_5_result, "Courses Taught by George Wilkinson")
    else:
        print(Fore.RED + "No courses found taught by George Wilkinson.")

    select_6_result = select_6("Group 1")
    if select_6_result:
        print_query_result(select_6_result, "Students in Group 1")
    else:
        print(Fore.RED + "No students found in Group 1.")

    select_7_result = select_7("Group 1", "Potion making")
    if select_7_result:
        print_query_result(select_7_result, "Grades in Group 1 for Potion making")
    else:
        print(Fore.RED + "No grades found in Group 1 for the 'Potion making' subject.")

    avg_8 = select_8("George Wilkinson")
    if avg_8 is not None:
        print(Fore.YELLOW + f"George Wilkinson Average Grade: {avg_8}")
    else:
        print(Fore.RED + "No average grade found for George Wilkinson.")

    select_9_result = select_9("Labokka Willaribo")
    if select_9_result:
        print_query_result(select_9_result, "Courses Attended by Labokka Willaribo")
    else:
        print(Fore.RED + "No courses found for Labokka Willaribo.")

    select_10_result = select_10("Labokka Willaribo", "George Wilkinson")
    if select_10_result:
        print_query_result(
            select_10_result, "Courses Taught by George Wilkinson to Labokka Willaribo"
        )
    else:
        print(Fore.RED + "No courses found for Labokka Willaribo taught by George Wilkinson.")