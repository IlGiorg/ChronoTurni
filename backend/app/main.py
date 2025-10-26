from fastapi import FastAPI, Depends, HTTPException
import os
from . import models
from .database import SessionLocal
from .scheduler import generate_schedule, verify_license_file
from license_utils import validate_customer

app = FastAPI()

app = FastAPI()


@app.post('/shifts')
def create_shift(s: models.ShiftIn):
    db = SessionLocal()
    sh = models.Shift(
        customer_id=s.customer_id,
        date=s.date,
        start=s.start,
        end=s.end,
        required_roles=s.required_roles
    )
    db.add(sh)
    db.commit()
    db.refresh(sh)
    return {"id": sh.id}


@app.post('/generate_schedule')
def api_generate_schedule(payload: dict):
    # payload: {"customer_id":..., "period": {"from":"YYYY-MM-DD","to":"YYYY-MM-DD"}}
    customer_id = payload.get('customer_id')

    # load employees and shifts from DB (minimal)
    db = SessionLocal()
    emps = db.query(models.Employee).filter(models.Employee.customer_id == customer_id).all()
    shs = db.query(models.Shift).filter(models.Shift.customer_id == customer_id).all()

    emplist = []
    shlist = []

    for e in emps:
        emplist.append({
            'id': e.id,
            'name': e.name,
            'role': e.role,
            'preferences': e.preferences
        })

    for s in shs:
        shlist.append({
            'id': s.id,
            'date': s.date.isoformat(),
            'start': s.start,
            'end': s.end,
            'required_roles': s.required_roles
        })

    assignments = generate_schedule(emplist, shlist)
    return {"assignments": assignments}


@app.get("/license_check/{customer_id}")
def license_check(customer_id: str):
    valid, msg = validate_customer(customer_id)
    if not valid:
        raise HTTPException(status_code=403, detail=msg)
    return {"status": "ok", "message": msg}



