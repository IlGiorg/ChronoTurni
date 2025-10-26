from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, Time, Date
from sqlalchemy.orm import relationship
from .database import Base
import datetime


class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String, index=True)
    name = Column(String, index=True)
    role = Column(String)
    weekly_hours_max = Column(Integer, default=40)
    preferences = Column(JSON, default={}) # e.g. unavailable times, days off


class Shift(Base):
    __tablename__ = 'shifts'
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String, index=True)
    date = Column(Date)
    start = Column(String) # ISO time string
    end = Column(String)
    required_roles = Column(JSON, default={})
    assigned_employee_id = Column(Integer, ForeignKey('employees.id'), nullable=True)
    assigned_employee = relationship('Employee')