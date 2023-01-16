from datetime import date
from ninja import Schema
# from ninja.orm import create_schema
from demo.models import Department, Employee

# EmployeeSchema = create_schema(Employee)

#same as

class EmployeeIn(Schema):
    first_name: str
    last_name: str
    department_id: int = None
    birthdate: date = None

class EmployeeOut(Schema):
    id: int
    first_name: str
    last_name: str
    department_id: int = None
    birthdate: date = None

class UserLogin(Schema):
    first_name: str
    last_name: str


class TokenSchema(Schema):
    access: str
    