def test_salary_calculation(client):
    res = client.post("/employees", json={
        "full_name": "Bob",
        "job_title": "IT",
        "country": "India",
        "salary": 10000
    })

    assert res.status_code == 201
    emp_id = res.json()["id"]

    salary_res = client.get(f"/employees/{emp_id}/salary")
    assert salary_res.status_code == 200

    data = salary_res.json()
    assert data["gross_salary"] == 10000
    assert data["tds"] == 1000
    assert data["net_salary"] == 9000