import threading
from models.database import SessionLocal, engine, Base
from models.course import Course
from models.student import Student
from models.instructor import Instructor
from models.enrollment import Enrollment
from sqlalchemy.exc import IntegrityError

# Create all tables
Base.metadata.create_all(bind=engine)

# Initialize session
session_lock = threading.Lock()

def main_menu():
    print("Welcome to the Advanced Online Learning Platform CLI")
    while True:
        print("\n1. Add Student")
        print("2. Add Instructor")
        print("3. Add Course")
        print("4. Enroll Student")
        print("5. View All Courses")
        print("6. View All Students")
        print("7. Exit")
        choice = input("Select an option: ")
        
        if choice == "1":
            threading.Thread(target=add_student).start()
        elif choice == "2":
            threading.Thread(target=add_instructor).start()
        elif choice == "3":
            threading.Thread(target=add_course).start()
        elif choice == "4":
            threading.Thread(target=enroll_student).start()
        elif choice == "5":
            threading.Thread(target=view_courses).start()
        elif choice == "6":
            threading.Thread(target=view_students).start()
        elif choice == "7":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

def add_student():
    with session_lock:
        session = SessionLocal()
        name = input("Enter student name: ")
        email = input("Enter student email: ")
        student = Student(name=name, email=email)
        try:
            session.add(student)
            session.commit()
            print(f"Student {name} added.")
        except IntegrityError:
            session.rollback()
            print("Error: Could not add student. Email might already exist.")
        finally:
            session.close()

def add_instructor():
    with session_lock:
        session = SessionLocal()
        name = input("Enter instructor name: ")
        instructor = Instructor(name=name)
        try:
            session.add(instructor)
            session.commit()
            print(f"Instructor {name} added.")
        except IntegrityError:
            session.rollback()
            print("Error: Could not add instructor.")
        finally:
            session.close()

def add_course():
    with session_lock:
        session = SessionLocal()
        title = input("Enter course title: ")
        description = input("Enter course description: ")
        instructor_id = input("Enter instructor ID: ")
        try:
            instructor = session.query(Instructor).filter(Instructor.id == instructor_id).one_or_none()
            if instructor is None:
                print("Error: Instructor not found.")
                return
            course = Course(title=title, description=description, instructor_id=instructor_id)
            session.add(course)
            session.commit()
            print(f"Course {title} added.")
        except IntegrityError:
            session.rollback()
            print("Error: Could not add course.")
        finally:
            session.close()

def enroll_student():
    with session_lock:
        session = SessionLocal()
        student_id = input("Enter student ID: ")
        course_id = input("Enter course ID: ")
        try:
            student = session.query(Student).filter(Student.id == student_id).one_or_none()
            course = session.query(Course).filter(Course.id == course_id).one_or_none()
            if student is None:
                print(f"Error: Student with ID {student_id} not found.")
                return
            if course is None:
                print(f"Error: Course with ID {course_id} not found.")
                return

            # Ensure the student isn't already enrolled in the course
            existing_enrollment = session.query(Enrollment).filter_by(student_id=student_id, course_id=course_id).one_or_none()
            if existing_enrollment:
                print(f"Student {student_id} is already enrolled in course {course_id}.")
                return

            enrollment = Enrollment(student_id=student_id, course_id=course_id)
            session.add(enrollment)
            session.commit()
            print(f"Student {student_id} successfully enrolled in course {course_id}.")
        except IntegrityError:
            session.rollback()
            print("Error: Could not enroll student.")
        finally:
            session.close()

def view_courses():
    with session_lock:
        session = SessionLocal()
        courses = session.query(Course).all()
        if not courses:
            print("No courses found.")
        for course in courses:
            instructor = session.query(Instructor).filter(Instructor.id == course.instructor_id).one()
            print(f"Course ID: {course.id}, Title: {course.title}, Instructor: {instructor.name}")
        session.close()

def view_students():
    with session_lock:
        session = SessionLocal()
        students = session.query(Student).all()
        if not students:
            print("No students found.")
        for student in students:
            print(f"Student ID: {student.id}, Name: {student.name}, Email: {student.email}")
        session.close()

if __name__ == "__main__":
    main_menu()
