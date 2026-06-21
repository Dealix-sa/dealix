"""
HR API — Employees, Attendance, Leave, Payroll.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from api.security.auth_deps import get_current_user
from db.session import get_db as get_db_session
from dealix.erp.service import ERPService
from dealix.feature_gating.service import FeatureGate

router = APIRouter(prefix="/api/v1/erp/hr", tags=["ERP — HR"])


class EmployeeCreate(BaseModel):
    full_name: str
    email: str | None = None
    phone: str | None = None
    national_id: str | None = None
    department: str | None = None
    job_title: str | None = None
    employment_type: str = "full_time"
    joining_date: str | None = None
    basic_salary_sar: float = 0.0
    housing_allowance_sar: float = 0.0
    transport_allowance_sar: float = 0.0
    bank_iban: str | None = None
    bank_name: str | None = None


class AttendanceCreate(BaseModel):
    employee_id: str
    date: str
    check_in: str | None = None
    check_out: str | None = None
    status: str = "present"
    work_hours: float | None = None


class LeaveCreate(BaseModel):
    employee_id: str
    leave_type: str = Field(..., pattern="^(annual|sick|hajj|maternity|unpaid|emergency)$")
    start_date: str
    end_date: str
    days_count: float = 0.0
    reason: str | None = None


@router.post("/employees", dependencies=[Depends(FeatureGate("hr"))])
async def create_employee(
    req: EmployeeCreate,
    session: AsyncSession = Depends(get_db_session),
    current_user=Depends(get_current_user),
) -> dict[str, Any]:
    svc = ERPService(session)
    e = await svc.create_employee(current_user.tenant_id, req.dict(exclude_none=True))
    await session.commit()
    return {"id": e.id, "full_name": e.full_name, "status": e.status}


@router.get("/employees")
async def list_employees(
    session: AsyncSession = Depends(get_db_session),
    current_user=Depends(get_current_user),
) -> list[dict[str, Any]]:
    svc = ERPService(session)
    employees = await svc.list_employees(current_user.tenant_id)
    return [{"id": e.id, "full_name": e.full_name, "department": e.department, "job_title": e.job_title} for e in employees]


@router.post("/attendance", dependencies=[Depends(FeatureGate("hr"))])
async def record_attendance(
    req: AttendanceCreate,
    session: AsyncSession = Depends(get_db_session),
    current_user=Depends(get_current_user),
) -> dict[str, Any]:
    svc = ERPService(session)
    a = await svc.record_attendance(current_user.tenant_id, req.dict(exclude_none=True))
    await session.commit()
    return {"id": a.id, "date": str(a.date), "status": a.status}


@router.post("/leaves", dependencies=[Depends(FeatureGate("hr"))])
async def create_leave(
    req: LeaveCreate,
    session: AsyncSession = Depends(get_db_session),
    current_user=Depends(get_current_user),
) -> dict[str, Any]:
    svc = ERPService(session)
    l = await svc.create_leave_request(current_user.tenant_id, req.dict(exclude_none=True))
    await session.commit()
    return {"id": l.id, "status": l.status, "days_count": l.days_count}


@router.post("/payroll/run", dependencies=[Depends(FeatureGate("hr"))])
async def run_payroll(
    month: int,
    year: int,
    session: AsyncSession = Depends(get_db_session),
    current_user=Depends(get_current_user),
) -> dict[str, Any]:
    svc = ERPService(session)
    pr = await svc.process_payroll(current_user.tenant_id, month, year)
    await session.commit()
    return {
        "id": pr.id,
        "period": f"{month}/{year}",
        "total_net_salary": pr.total_net_salary,
        "employee_count": len([l for l in pr.lines]) if hasattr(pr, "lines") else 0,
    }
