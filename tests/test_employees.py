def test_create_employee(client):
    response = client.post(
        "/employees",
        json={
            "full_name": "Alice Johnson",
            "job_title": "Developer",
            "country": "India",
            "salary": 50000
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["full_name"] == "Alice Johnson"
    assert data["job_title"] == "Developer"
    assert data["country"] == "India"
    assert data["salary"] == 50000


def test_get_all_employees(client):
    client.post(
        "/employees",
        json={
            "full_name": "Bob Smith",
            "job_title": "QA Engineer",
            "country": "USA",
            "salary": 60000
        }
    )

    response = client.get("/employees")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_one_employee(client):
    create_response = client.post(
        "/employees",
        json={
            "full_name": "Charlie Brown",
            "job_title": "Manager",
            "country": "India",
            "salary": 70000
        }
    )
    employee_id = create_response.json()["id"]

    response = client.get(f"/employees/{employee_id}")
    assert response.status_code == 200
    assert response.json()["full_name"] == "Charlie Brown"


def test_get_employee_not_found(client):
    response = client.get("/employees/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Employee not found"


def test_update_employee(client):
    create_response = client.post(
        "/employees",
        json={
            "full_name": "David Lee",
            "job_title": "Developer",
            "country": "USA",
            "salary": 80000
        }
    )
    employee_id = create_response.json()["id"]

    update_response = client.put(
        f"/employees/{employee_id}",
        json={
            "full_name": "David Lee Updated",
            "job_title": "Senior Developer",
            "country": "USA",
            "salary": 90000
        }
    )

    assert update_response.status_code == 200
    data = update_response.json()
    assert data["full_name"] == "David Lee Updated"
    assert data["job_title"] == "Senior Developer"
    assert data["salary"] == 90000


def test_delete_employee(client):
    create_response = client.post(
        "/employees",
        json={
            "full_name": "Emma Stone",
            "job_title": "Analyst",
            "country": "India",
            "salary": 55000
        }
    )
    employee_id = create_response.json()["id"]

    delete_response = client.delete(f"/employees/{employee_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Employee deleted successfully"

    get_response = client.get(f"/employees/{employee_id}")
    assert get_response.status_code == 404


def test_salary_endpoint_india(client):
    create_response = client.post(
        "/employees",
        json={
            "full_name": "Farhan Ali",
            "job_title": "Engineer",
            "country": "India",
            "salary": 100000
        }
    )
    employee_id = create_response.json()["id"]

    response = client.get(f"/employees/{employee_id}/salary")
    assert response.status_code == 200
    data = response.json()
    assert data["gross_salary"] == 100000
    assert data["tds"] == 10000
    assert data["net_salary"] == 90000


def test_salary_endpoint_usa(client):
    create_response = client.post(
        "/employees",
        json={
            "full_name": "George King",
            "job_title": "Architect",
            "country": "USA",
            "salary": 100000
        }
    )
    employee_id = create_response.json()["id"]

    response = client.get(f"/employees/{employee_id}/salary")
    assert response.status_code == 200
    data = response.json()
    assert data["gross_salary"] == 100000
    assert data["tds"] == 12000
    assert data["net_salary"] == 88000


def test_invalid_country_validation(client):
    response = client.post(
        "/employees",
        json={
            "full_name": "Henry",
            "job_title": "Admin",
            "country": "UK",
            "salary": 40000
        }
    )
    assert response.status_code == 422


def test_negative_salary_validation(client):
    response = client.post(
        "/employees",
        json={
            "full_name": "Irene",
            "job_title": "Support",
            "country": "India",
            "salary": -100
        }
    )
    assert response.status_code == 422