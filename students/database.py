from dataclasses import dataclass
from datetime import datetime
import sqlite3


@dataclass
class Student:
    id: int | None
    enrollment_number: str
    name: str
    email: str
    phone: str | None
    mobile: str | None
    rg: str | None
    cpf: str | None
    birthdate: datetime | None
    course: str | None
    semester_year: str | None
    schedule: str | None
    address: str | None
    zip_code: str | None
    neighborhood: str | None
    city: str | None
    state: str | None
    pcd: bool
    responsible: str | None
    created_at: datetime = datetime.now()

    @staticmethod
    def from_db_row(row):
        return Student(*row)

    @staticmethod
    def from_file(
            enrollment_number, name, email, phone, mobile, rg, cpf, birthdate, course, semester_year, schedule, address,
            zip_code, neighborhood, city, state, pcd, responsible
    ):
        return Student(
            None, enrollment_number, name, email, phone, mobile, rg, cpf, birthdate, course, semester_year, schedule,
            address, zip_code, neighborhood, city, state, pcd, responsible, datetime.now()
        )


def get_connection():
    return sqlite3.connect('database.sqlite')


def save_student(student: Student) -> Student:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        'INSERT INTO students (enrollment_number, name, email, phone, mobile, rg, cpf, birthdate, '
        'course, semester_year, schedule, address, zip_code, neighborhood, city, state, pcd, responsible, created_at) '
        'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
        (student.enrollment_number, student.name, student.email, student.phone, student.mobile, student.rg,
         student.cpf,
         student.birthdate, student.course, student.semester_year, student.schedule, student.address,
         student.zip_code,
         student.neighborhood, student.city, student.state, student.pcd, student.responsible, student.created_at)
    )

    student.id = cursor.lastrowid

    connection.commit()
    connection.close()
    return student
