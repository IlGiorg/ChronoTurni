import random
import json
import os

DATA_FILE = "data.json"

class Employee:
    def __init__(self, name):
        self.name = name
        self.restrictions = set()

    def add_restriction(self, restriction):
        self.restrictions.add(restriction)

    def to_dict(self):
        return {"name": self.name, "restrictions": list(self.restrictions)}

    @staticmethod
    def from_dict(data):
        e = Employee(data["name"])
        e.restrictions = set(data.get("restrictions", []))
        return e


class Shift:
    def __init__(self, day, name, num_required):
        self.day = day
        self.name = name
        self.num_required = num_required

    def id(self):
        return f"{self.day}-{self.name}"

    def to_dict(self):
        return {"day": self.day, "name": self.name, "num_required": self.num_required}

    @staticmethod
    def from_dict(data):
        return Shift(data["day"], data["name"], data["num_required"])


import os, json

DATA_FILE = "data.json"

class ShiftManager:
    def __init__(self):
        self.employees = []
        self.shifts = []
        self.load()  # loads from data.json if it exists

    def save(self):
        data = {
            "employees": [e.to_dict() for e in self.employees],
            "shifts": [s.to_dict() for s in self.shifts]
        }
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)

    def load(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r") as f:
                    data = json.load(f)
                    self.employees = [Employee.from_dict(e) for e in data.get("employees", [])]
                    self.shifts = [Shift.from_dict(s) for s in data.get("shifts", [])]
            except json.JSONDecodeError:
                self.employees = []
                self.shifts = []
        else:
            self.employees = []
            self.shifts = []



    def generate_schedule(self):
    schedule = {}
    warnings = []

    for shift in self.shifts:
        available = [e for e in self.employees if shift.id() not in e.restrictions]

        if len(available) < shift.num_required:
            assigned = available
            warnings.append(f"⚠️ Not enough staff for {shift.id()}")
        else:
            assigned = random.sample(available, shift.num_required)

        schedule[shift.id()] = assigned

    return schedule, warnings


    def save(self):
        data = {
            "employees": [e.to_dict() for e in self.employees],
            "shifts": [s.to_dict() for s in self.shifts],
        }
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)

    def load(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                self.employees = [Employee.from_dict(e) for e in data.get("employees", [])]
                self.shifts = [Shift.from_dict(s) for s in data.get("shifts", [])]
