def test_metrics_by_country(client):
    client.post(
        "/employees",
        json={
            "full_name": "Alice",
            "job_title": "Developer",
            "country": "India",
            "salary": 50000
        }
    )
    client.post(
        "/employees",
        json={
            "full_name": "Bob",
            "job_title": "Developer",
            "country": "India",
            "salary": 70000
        }
    )

    response = client.get("/metrics/country/India")
    assert response.status_code == 200

    data = response.json()
    assert data["country"] == "India"
    assert data["min_salary"] == 50000
    assert data["max_salary"] == 70000
    assert data["avg_salary"] == 60000


def test_metrics_by_job_title(client):
    client.post(
        "/employees",
        json={
            "full_name": "Alice",
            "job_title": "Developer",
            "country": "India",
            "salary": 50000
        }
    )
    client.post(
        "/employees",
        json={
            "full_name": "Bob",
            "job_title": "Developer",
            "country": "USA",
            "salary": 70000
        }
    )

    response = client.get("/metrics/job-title/Developer")
    assert response.status_code == 200

    data = response.json()
    assert data["job_title"] == "Developer"
    assert data["avg_salary"] == 60000


def test_metrics_country_not_found(client):
    response = client.get("/metrics/country/USA")
    assert response.status_code == 404
    assert response.json()["detail"] == "No employees found for this country"


def test_metrics_job_title_not_found(client):
    response = client.get("/metrics/job-title/Designer")
    assert response.status_code == 404
    assert response.json()["detail"] == "No employees found for this job title"