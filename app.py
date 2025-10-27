from flask import Flask, render_template, request, redirect, url_for, send_file
from shift_logic import ShiftManager
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import io

app = Flask(__name__)
manager = ShiftManager()  # loads data automatically

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
    schedule_data, warnings = manager.generate_schedule()
    return render_template("schedule.html", schedule=schedule_data, warnings=warnings)


@app.route("/export_pdf")
def export_pdf():
    schedule = manager.generate_schedule()

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph("<b>Shift Schedule</b>", styles["Title"]))
    content.append(Spacer(1, 12))

    for shift_id, employees in schedule.items():
        emp_names = ", ".join(e.name for e in employees)
        line = f"{shift_id}: {emp_names}"
        content.append(Paragraph(line, styles["Normal"]))
        content.append(Spacer(1, 6))

    doc.build(content)
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="schedule.pdf", mimetype="application/pdf")

if __name__ == "__main__":
    app.run(debug=True)
