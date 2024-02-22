import pytest
from app import create_app, db
from . import TestConfig

@pytest.fixture
def client():
    app = create_app(TestConfig)
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client


def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == {'message': 'Welcome to the Rest API'}

def test_populate_department(client):
    # Example simplified payload; adjust as necessary for your endpoint's expected input
    payload = {
    "csv_file_path": "app/data/departments.csv",
    "schema": {
        "column_mapping": {
            "id": 0,
            "department": 1
        }
    },
    "table_name": "Departments"
}

    response = client.post('/api/populate_table', json=payload)
    print(response.data)

    assert response.status_code == 201, "Expected HTTP 201 status code for successful insert."
    assert response.json.get(
        'message') == 'Data inserted into table Departments successfully', "Unexpected response message."
    
def test_populate_job(client):
    # Example simplified payload; adjust as necessary for your endpoint's expected input
    payload = {
    "csv_file_path": "app/data/jobs.csv",
    "schema": {
        "column_mapping": {
            "id": 0,
            "job": 1
        }
    },
    "table_name": "Jobs"
}

    response = client.post('/api/populate_table', json=payload)
    print(response.data)

    assert response.status_code == 201, "Expected HTTP 201 status code for successful insert."
    assert response.json.get(
        'message') == 'Data inserted into table Jobs successfully', "Unexpected response message."
    
def test_populate_employee(client):
    # Example simplified payload; adjust as necessary for your endpoint's expected input
    payload = {
    "csv_file_path": "app/data/hired_employees.csv",
    "schema": {
        "column_mapping": {
            "id": 0,
            "name": 1,
            "datetime": 2,
            "department_id": 3,
            "job_id": 4
        }
    },
    "table_name": "Employee"
}

    response = client.post('/api/populate_table', json=payload)
    print(response.data)

    assert response.status_code == 201, "Expected HTTP 201 status code for successful insert."
    assert response.json.get(
        'message') == 'Data inserted into table Employee successfully', "Unexpected response message."