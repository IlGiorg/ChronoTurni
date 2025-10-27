#!/bin/bash
# add a couple of employees
curl -X POST "http://localhost:8000/employees" -H "Content-Type: application/json" -d '{"customer_id":"rist-1","name":"Mario","role":"cameriere","preferences": {"days_off":[]}}'


curl -X POST "http://localhost:8000/shifts" -H "Content-Type: application/json" -d '{"customer_id":"rist-1","date":"2025-11-01","start":"09:00","end":"14:00","required_roles": {"cameriere":2}}'


# generate schedule
curl -X POST "http://localhost:8000/generate_schedule" -H "Content-Type: application/json" -d '{"customer_id":"rist-1"}'