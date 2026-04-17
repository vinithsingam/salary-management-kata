from pydantic import BaseModel, Field, field_validator, ConfigDict

class EmployeeBase(BaseModel):
    full_name: str = Field(..., min_length=1)
    job_title: str = Field(..., min_length=1)
    country: str = Field(..., min_length=1)
    salary: float = Field(..., gt=0)

    @field_validator("full_name", "job_title", "country")
    @classmethod
    def validate_not_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Field cannot be empty")
        return value



class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(EmployeeBase):
    pass


class EmployeeOut(EmployeeBase):
    id: int
    model_config = ConfigDict(from_attributes=True)