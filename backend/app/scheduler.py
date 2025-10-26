from datetime import date, timedelta, datetime
from typing import List, Dict, Any


# Simple greedy scheduler for MVP


def generate_schedule(employees: List[Dict[str, Any]], shifts: List[Dict[str, Any]]):
    """employees: list of dicts with id, name, role, preferences (days_off list)
    shifts: list of dicts with id, date (YYYY-MM-DD), start, end, required_roles e.g. {"cameriere":2, "cuoco":1}
    Returns: list of assignments: {shift_id: employee_id}
    """
    # Build helper structures
    emp_by_role = {}
    hours_assigned = {e['id']: 0 for e in employees}
    avail = {}
    for e in employees:
        r = e['role']
        emp_by_role.setdefault(r, []).append(e)
        # preferences simple: days_off
        avail[e['id']] = set()
        days_off = set(e.get('preferences', {}).get('days_off', []))
        # We'll compute availability per shift date on the fly


    assignments = {}


    # Sort shifts by date
    sorted_shifts = sorted(shifts, key=lambda s: s['date'])


    for s in sorted_shifts:
        needed = dict(s.get('required_roles', {}))
        s_date = s['date']
    for role, cnt in needed.items():
        candidates = emp_by_role.get(role, [])
        # filter candidates: not day off, not over hours
        filtered = [c for c in candidates if s_date not in set(c.get('preferences', {}).get('days_off', []))]
        # sort by least hours
        filtered.sort(key=lambda x: hours_assigned[x['id']])
        take = filtered[:cnt]
    for t in take:
        assignments.setdefault(s['id'], []).append(t['id'])
        # approximate hours: compute difference
        # assume start/end are HH:MM
        fmt = "%H:%M"
        st = datetime.strptime(s['start'], fmt)
        en = datetime.strptime(s['end'], fmt)
        delta = (en - st).seconds/3600.0
        hours_assigned[t['id']] += delta
    return assignments