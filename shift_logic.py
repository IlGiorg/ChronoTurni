import random

class Employee:
    def __init__(self, name):
        self.name = name
        self.restrictions = set()

    def add_restriction(self, restriction):
        self.restrictions.add(restriction)

    def __repr__(self):
        return self.name


class Shift:
    def __init__(self, day, name, num_required):
        self.day = day
        self.name = name
        self.num_required = num_required

    def id(self):
        return f"{self.day}-{self.name}"

    def __repr__(self):
        return f"{self.day} {self.name} ({self.num_required} needed)"


class ShiftManager:
    def __init__(self):
        self.employees = []
        self.shifts = []

    def add_employee(self, name):
        self.employees.append(Employee(name))

    def add_shift(self, day, shift_name, num_required):
        self.shifts.append(Shift(day, shift_name, num_required))

    def add_restriction(self, employee_name, restriction):
        for emp in self.employees:
            if emp.name == employee_name:
                emp.add_restriction(restriction)
                return True
        return False

    def generate_schedule(self):
        schedule = {}

        for shift in self.shifts:
            available = [
                e for e in self.employees if shift.id() not in e.restrictions
            ]

            if len(available) < shift.num_required:
                assigned = available
            else:
                assigned = random.sample(available, shift.num_required)

            schedule[shift.id()] = assigned

        return schedule
