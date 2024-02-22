from flask import jsonify, Blueprint, request, render_template
from app.models import Employee, Department, Job
import csv
from app import upload_to_db, db
from sqlalchemy import func, and_, extract


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
    
@main_bp.route('/employee_by_quarter', methods=['GET'])
def employee_metrics():
    try:
        # Query the database to get the number of employees hired for each job and department in 2021 divided by quarter
        data = db.session.query(
                        Department.department,
                        Job.job,
                        func.sum(db.case([(extract('month', Employee.datetime).between(1, 3), 1)], else_=0)).label('Q1'),
                        func.sum(db.case([(extract('month', Employee.datetime).between(4, 6), 1)], else_=0)).label('Q2'),
                        func.sum(db.case([(extract('month', Employee.datetime).between(7, 9), 1)], else_=0)).label('Q3'),
                        func.sum(db.case([(extract('month', Employee.datetime).between(10, 12), 1)], else_=0)).label('Q4')
                        ).select_from(Employee).filter(extract('year', Employee.datetime) == 2021).join(Department).join(Job).group_by(Department.department, Job.job).all()

        # Convert the data to a list of dictionaries
        result = [{'department': d.department, 'job': d.job, 'Q1': d.Q1, 'Q2': d.Q2, 'Q3': d.Q3, 'Q4': d.Q4} for d in data]

        return render_template('employees_by_quarter.html', data = result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

