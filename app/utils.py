def calculate_salary(salary: float, country: str) -> dict:
    if country == "India":
        tds = salary * 0.10
    elif country == "USA":
        tds = salary * 0.12
    else:
        tds = 0.0

    net_salary = salary - tds

    return {
        "gross_salary": salary,
        "tds": tds,
        "net_salary": net_salary
    }