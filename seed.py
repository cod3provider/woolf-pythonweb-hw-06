import random
from faker import Faker
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base, Student, Group, Teacher, Subject, Grade
from pprint import pprint
from colorama import init, Fore

init(autoreset=True)

fake = Faker()

DATABASE_URL = "postgresql+psycopg2://postgres:db_password@localhost:5432/postgres"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

NUM_GROUPS = 3
NUM_TEACHERS = 5
NUM_SUBJECTS = 8
NUM_STUDENTS = 50
MAX_GRADES_PER_STUDENT = 20


def seed_data():
    try:
        session.query(Grade).delete()
        session.query(Student).delete()
        session.query(Subject).delete()
        session.query(Teacher).delete()
        session.query(Group).delete()
        session.commit()

        groups = []
        for i in range(NUM_GROUPS):
            group_name = f"Group {i+1}"
            groups.append(Group(name=group_name))

        session.add_all(groups)
        session.commit()

        print(
            Fore.GREEN
            + f"Групи: {', '.join([group.name for group in groups])} успішно додано!"
        )

        teachers = [Teacher(name=fake.name()) for _ in range(NUM_TEACHERS)]
        session.add_all(teachers)
        session.commit()

        print(
            Fore.GREEN
            + f"Викладачі: {', '.join([teacher.name for teacher in teachers])} успішно додано!"
        )

        subjects = [
            Subject(name=fake.word().capitalize(), teacher=random.choice(teachers))
            for _ in range(NUM_SUBJECTS)
        ]
        session.add_all(subjects)
        session.commit()

        print(
            Fore.GREEN
            + f"Предмети: {', '.join([subject.name for subject in subjects])} успішно додано!"
        )

        students = [
            Student(name=fake.name(), group=random.choice(groups))
            for _ in range(NUM_STUDENTS)
        ]
        session.add_all(students)
        session.commit()

        print(Fore.GREEN + f"Студенти:")
        pprint([student.name for student in students])

        grades = []
        for student in students:
            for _ in range(random.randint(1, MAX_GRADES_PER_STUDENT)):
                grade = Grade(
                    student=student,
                    subject=random.choice(subjects),
                    grade=random.uniform(1.0, 5.0),
                    date_received=fake.date_between(start_date="-2y", end_date="today"),
                )
                grades.append(grade)

        session.add_all(grades)
        session.commit()

        print(Fore.GREEN + "Оцінки для студентів успішно додано!")

        print(Fore.CYAN + "Дані успішно додано до бази даних!")
    except Exception as e:
        session.rollback()
        print(Fore.RED + f"Помилка при заповненні бази даних: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    seed_data()