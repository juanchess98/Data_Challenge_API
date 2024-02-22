from flask import jsonify, Blueprint, request
from app.models import Employee, Department, Job
import csv
from app import upload_to_db
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
    employees_list = [{'id': employee.id, 'name': employee.name, 'datetime': employee.datetime, 'department_id': employee.department_id, 'job_id': employee.job_id} for employee in employees]
    return jsonify({'employees': employees_list}), 200


@main_bp.route('/jobs', methods=['GET'])
def get_jobs():
    jobs = Job.query.all()
    jobs_list = [{'id': job.id, 'job': job.job} for job in jobs]
    return jsonify({'jobs': jobs_list}), 200

@main_bp.route('/api/populate_table', methods=['POST'])
def populate_table():
    try:
        # Get data from the JSON payload
        data = request.json

        # Extract information from the JSON payload
        csv_file_path = data.get('csv_file_path')
        schema = data.get('schema')
        table_name = data.get('table_name')

        # Check if all required fields are present
        if not csv_file_path or not schema or not table_name:
            return jsonify({'error': 'Incomplete data provided'}), 400

        # Read CSV file and extract data
        with open(csv_file_path, 'r') as file:
            csv_data = csv.reader(file)
            rows = list(csv_data)
        if not rows:
            return jsonify({'error': 'No data found in CSV file'}), 400
        
        # Insert data into the specified database table
        upload_to_db(rows, table_name, schema)

        return jsonify({'message': f'Data inserted into table {table_name} successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

