from ninja import NinjaAPI, Form
from typing import List
from demo.schema import EmployeeIn, EmployeeOut
from demo.models import Department, Employee
from django.shortcuts import get_object_or_404
# from ninja_extra import permissions, api_controller

# from ninja_extra.permissions import IsAuthenticated, IsAdminUser




from ninja.security import HttpBearer
from ninja.security import HttpBasicAuth


class AuthCheck:
    def authenticate(self, request, key):
        if key == "supersecret":
            return key


class BearerKey(AuthCheck, HttpBearer):
    def authenticate(self, request, token):
        if token == "supersecret": # run your query to check or validate user
            return token
    


class BasicAuthKey(AuthCheck, HttpBasicAuth):
    def authenticate(self, request, username, password):
        if username == "admin" and password == "secret":
            return username

    
api = NinjaAPI(auth=[BasicAuthKey(), BearerKey()], title="Kweku's API")
# permissions=[permissions.IsAuthenticated, permissions.IsAdminUser]


@api.get("/add")
def add(request, a: int, b: int):
    return {"result": a + b}


@api.post("/employees")
def create_employee(request, response: EmployeeIn):
    employee = Employee.objects.create(**response.dict())
    return {"id": employee. id}


@api.get("/employees/{id}", response=EmployeeOut)
def get_employee(request, id: int):
    employee = Employee.objects.get(id=id)
    return employee

# @api.get("/employees/{id}", response=EmployeeOut)
# def get_employee(request, id: int):
#     employee = get_object_or_404(Employee, id=id)
#     return employee

@api.get("/employees", response=List[EmployeeOut])
def all_employees(request):
    employees = Employee.objects.all()
    return employees


# @api.api_operation(["GET","POST", "DELETE"], "/employees/{id}")

@api.put("/employees/{id}") # permissions=[IsAuthenticated, IsAdminUser]
def update_employee(request, id: int, response: EmployeeIn):
    employee = get_object_or_404(Employee, id = id)
    for attr , value in response.dict().items():
        setattr(employee, attr, value)
    employee.save()
    return {"success": f"Updatted employee with id: {id}"}


# @api_controller("permission", permissions.IsAuthenticated)
# @api.api_operation(["GET","POST", "DELETE"], "/employees/{id}")
@api.delete("/employees/{id}" ) # permissions=([IsAuthenticated, IsAdminUser])
def delete_employee(request, id: int):
    employee = get_object_or_404(Employee, id = id)
    employee.delete()
    return {"success": f"Deleted employee with id: {id}"}

