from flask import jsonify, Blueprint
from app.models import Employee, Department, Job

main_bp = Blueprint('main', __name__)
@main_bp.route('/')
def index():
    return jsonify(message='Welcome to the Rest API')


@main_bp.route('/departments', methods=['GET'])
def get_departments():
    departments = Department.query.all()
    departments_list = [{'id': department.id, 'Department': department.department} for department in departments]
    return jsonify({'departments': departments_list}), 200


@main_bp.route('/employees', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    employees_list = [{'id': employee.id, 'name': employee.name, 'datetime': employee.hired_date, 'department_id': employee.department_id, 'job_id': employee.job_id} for employee in employees]
    return jsonify({'employees': employees_list}), 200


@main_bp.route('/jobs', methods=['GET'])
def get_jobs():
    jobs = Job.query.all()
    jobs_list = [{'id': job.id, 'job': job.job} for job in jobs]
    return jsonify({'jobs': jobs_list}), 200