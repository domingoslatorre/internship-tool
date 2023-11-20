from flask import Blueprint, request, redirect, url_for, render_template, flash

from students.database import Student, save_student

students = Blueprint('students', __name__, url_prefix='/students')


@students.route('/import-from-file', methods=['GET'])
def import_students():
    return render_template('students/import-from-file.html')


@students.route('/import-from-file', methods=['POST'])
def import_students_post():
    file = request.files.get('file')
    if not file:
        return redirect(url_for('students.import_students'))

    count = 0
    for line in file:
        line = line.decode('utf-8')
        fields = [field.strip() for field in line.split(sep=",")]
        save_student(Student.from_file(*fields))
        count += 1

    flash(f'{count} students imported successfully', 'success')
    return redirect(url_for('students.import_students'))

