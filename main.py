import random
import csv

class Employee:
    def __init__(self, name):
        self.name = name
        self.restrictions = set()  # e.g. {"Monday-Morning", "Friday-Night"}

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
                return
        print(f"Employee {employee_name} not found.")

    def generate_schedule(self):
        schedule = {}

        for shift in self.shifts:
            available = [
                e for e in self.employees
                if shift.id() not in e.restrictions
            ]

            if len(available) < shift.num_required:
                print(f"⚠️ Warning: Not enough staff for {shift.id()}")
                assigned = available
            else:
                assigned = random.sample(available, shift.num_required)

            schedule[shift.id()] = assigned

        return schedule

    def display_schedule(self, schedule):
        print("\n📅 Generated Schedule:")
        for shift_id, emps in schedule.items():
            names = ", ".join(e.name for e in emps)
            print(f"{shift_id}: {names}")

    def export_to_csv(self, schedule, filename="schedule.csv"):
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Shift", "Assigned Employees"])
            for shift_id, emps in schedule.items():
                writer.writerow([shift_id, ", ".join(e.name for e in emps)])
        print(f"\n✅ Schedule exported to {filename}")


def main():
    manager = ShiftManager()

    while True:
        print("\n--- SHIFT MANAGER ---")
        print("1. Add employee")
        print("2. Add shift")
        print("3. Add restriction")
        print("4. Generate schedule")
        print("5. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            name = input("Employee name: ")
            manager.add_employee(name)
            print(f"Added {name}")

        elif choice == "2":
            day = input("Day (e.g. Monday): ")
            shift_name = input("Shift name (e.g. Morning): ")
            num_required = int(input("Number required: "))
            manager.add_shift(day, shift_name, num_required)
            print("Shift added.")

        elif choice == "3":
            name = input("Employee name: ")
            restriction = input("Restriction (e.g. Monday-Morning): ")
            manager.add_restriction(name, restriction)
            print("Restriction added.")

        elif choice == "4":
            schedule = manager.generate_schedule()
            manager.display_schedule(schedule)
            export = input("Export to CSV? (y/n): ").lower()
            if export == "y":
                manager.export_to_csv(schedule)

        elif choice == "5":
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()