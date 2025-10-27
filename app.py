from flask import Flask, render_template, request, redirect, url_for
from shift_logic import ShiftManager

app = Flask(__name__)
manager = ShiftManager()

@app.route("/")
def index():
    return render_template("index.html", manager=manager)


@app.route("/add_employee", methods=["GET", "POST"])
def add_employee():
    if request.method == "POST":
        name = request.form["name"]
        manager.add_employee(name)
        return redirect(url_for("index"))
    return render_template("add_employee.html")

@app.route("/add_shift", methods=["GET", "POST"])
def add_shift():
    if request.method == "POST":
        day = request.form["day"]
        shift_name = request.form["shift_name"]
        num_required = int(request.form["num_required"])
        manager.add_shift(day, shift_name, num_required)
        return redirect(url_for("index"))
    return render_template("add_shift.html")

@app.route("/add_restriction", methods=["GET", "POST"])
def add_restriction():
    if request.method == "POST":
        emp = request.form["employee"]
        restriction = request.form["restriction"]
        manager.add_restriction(emp, restriction)
        return redirect(url_for("index"))
    return render_template("add_restriction.html", employees=manager.employees)

@app.route("/schedule")
def schedule():
    schedule = manager.generate_schedule()
    return render_template("schedule.html", schedule=schedule)

if __name__ == "__main__":
    app.run(debug=True)
