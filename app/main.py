from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from .database import Base, engine, SessionLocal
from .models import Employee
from .schemas import EmployeeCreate, EmployeeUpdate, EmployeeOut
from .utils import calculate_salary

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Salary Management API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/employees", response_model=EmployeeOut, status_code=status.HTTP_201_CREATED)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    db_employee = Employee(**employee.model_dump())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee


@app.get("/employees", response_model=list[EmployeeOut])
def get_employees(db: Session = Depends(get_db)):
    return db.query(Employee).all()


@app.get("/employees/{employee_id}", response_model=EmployeeOut)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@app.put("/employees/{employee_id}", response_model=EmployeeOut)
def update_employee(employee_id: int, updated_employee: EmployeeUpdate, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    employee.full_name = updated_employee.full_name
    employee.job_title = updated_employee.job_title
    employee.country = updated_employee.country
    employee.salary = updated_employee.salary

    db.commit()
    db.refresh(employee)
    return employee


@app.delete("/employees/{employee_id}", status_code=status.HTTP_200_OK)
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    db.delete(employee)
    db.commit()
    return {"message": "Employee deleted successfully"}


@app.get("/employees/{employee_id}/salary")
def get_employee_salary(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    return calculate_salary(employee.salary, employee.country)


@app.get("/metrics/country/{country}")
def get_country_metrics(country: str, db: Session = Depends(get_db)):
    result = db.query(
        func.min(Employee.salary).label("min_salary"),
        func.max(Employee.salary).label("max_salary"),
        func.avg(Employee.salary).label("avg_salary")
    ).filter(Employee.country == country).first()

    if result is None or result.min_salary is None:
        raise HTTPException(status_code=404, detail="No employees found for this country")

    return {
        "country": country,
        "min_salary": result.min_salary,
        "max_salary": result.max_salary,
        "avg_salary": result.avg_salary
    }


@app.get("/metrics/job-title/{job_title}")
def get_job_title_metrics(job_title: str, db: Session = Depends(get_db)):
    avg_salary = db.query(func.avg(Employee.salary)).filter(Employee.job_title == job_title).scalar()

    if avg_salary is None:
        raise HTTPException(status_code=404, detail="No employees found for this job title")

    return {
        "job_title": job_title,
        "avg_salary": avg_salary
    }