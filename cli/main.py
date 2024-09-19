import click
from database import setup_db
from student import Student
from instructor import Instructor
from course import Course
from enrollment import Enrollment
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

Session = setup_db()

@click.group()
def cli():
    """Online Learning System"""
    pass

@cli.command()
@click.option('--name', prompt='Student Name', help='The name of the student.')
def add_student(name):
    """Add a new student."""
    session = Session()
    student = Student(name=name)
    session.add(student)
    session.commit()
    click.echo(f"Student '{student.name}' added with ID {student.id}")

@cli.command()
@click.option('--name', prompt='Instructor Name', help='The name of the instructor.')
def add_instructor(name):
    """Add a new instructor."""
    session = Session()
    instructor = Instructor(name=name)
    session.add(instructor)
    session.commit()
    click.echo(f"Instructor '{instructor.name}' added with ID {instructor.id}")

@cli.command()
@click.option('--title', prompt='Course Title', help='The title of the course.')
@click.option('--instructor_id', prompt='Instructor ID', help='The ID of the instructor.')
def add_course(title, instructor_id):
    """Add a new course."""
    session = Session()
    course = Course(title=title, instructor_id=instructor_id)
    session.add(course)
    session.commit()
    click.echo(f"Course '{course.title}' added with ID {course.id}")

@cli.command()
@click.option('--student_id', prompt='Student ID', help='The ID of the student.')
@click.option('--course_id', prompt='Course ID', help='The ID of the course.')
def enroll_student(student_id, course_id):
    """Enroll a student in a course."""
    session = Session()
    enrollment = Enrollment(student_id=student_id, course_id=course_id)
    session.add(enrollment)
    session.commit()
    click.echo(f"Student with ID {student_id} enrolled in Course with ID {course_id}")

@cli.command()
def view_all_courses():
    """View all courses."""
    session = Session()
    courses = session.query(Course).all()
    for course in courses:
        click.echo(f"Course ID: {course.id}, Title: {course.title}, Instructor ID: {course.instructor_id}")

@cli.command()
def view_all_students():
    """View all students."""
    session = Session()
    students = session.query(Student).all()
    for student in students:
        click.echo(f"Student ID: {student.id}, Name: {student.name}")

@cli.command()
def exit():
    """Exit the system."""
    click.echo("Exiting...")
    raise SystemExit(0)

def menu():
    """Displays a menu and takes user input to call specific commands."""
    while True:
        click.echo("\nCommands:")
        click.echo("1. Add a new course.")
        click.echo("2. Add a new instructor.")
        click.echo("3. Add a new student.")
        click.echo("4. Enroll a student in a course.")
        click.echo("5. View all courses.")
        click.echo("6. View all students.")
        click.echo("7. Exit.")
        
        choice = click.prompt("Enter your choice", type=int)

        if choice == 1:
            add_course()
        elif choice == 2:
            add_instructor()
        elif choice == 3:
            add_student()
        elif choice == 4:
            enroll_student()
        elif choice == 5:
            view_all_courses()
        elif choice == 6:
            view_all_students()
        elif choice == 7:
            exit()
        else:
            click.echo("Invalid choice, please try again.")

if __name__ == '__main__':
    menu()
