"""
ERP Suite models — Projects, Support, Documents, HR, Inventory, Finance.
نماذج مجموعة ERP — المشاريع، الدعم، المستندات، الموارد البشرية، المخزون، المالية.
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    JSON,
    Boolean,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from core.utils import utcnow
from db.models import Base


# ═══════════════════════════════════════════════════════════════════
# CRM Enhancements — Activities, Meetings, Notes
# ═══════════════════════════════════════════════════════════════════

class ActivityRecord(Base):
    """Activity log for CRM contacts/leads/deals."""
    __tablename__ = "activities"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"), index=True)
    entity_type: Mapped[str] = mapped_column(String(32), index=True)  # lead/deal/contact
    entity_id: Mapped[str] = mapped_column(String(64), index=True)
    activity_type: Mapped[str] = mapped_column(String(32), index=True)  # call/email/meeting/note/task
    subject: Mapped[str] = mapped_column(String(255), default="")
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    performed_by: Mapped[str] = mapped_column(String(64), default="")
    duration_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    outcome: Mapped[str | None] = mapped_column(String(64), nullable=True)  # completed/no_answer/scheduled
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)

    __table_args__ = (Index("ix_activities_tenant_entity", "tenant_id", "entity_type", "entity_id"),)


class MeetingRecord(Base):
    """Scheduled meetings linked to deals/contacts."""
    __tablename__ = "meetings"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"), index=True)
    deal_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    contact_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    title: Mapped[str] = mapped_column(String(255), default="")
    start_at: Mapped[datetime] = mapped_column(index=True)
    end_at: Mapped[datetime | None] = mapped_column(nullable=True)
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    meeting_link: Mapped[str | None] = mapped_column(String(512), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="scheduled")  # scheduled/completed/cancelled/no_show
    created_by: Mapped[str] = mapped_column(String(64), default="")
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)


class NoteRecord(Base):
    """Free-form notes on any entity."""
    __tablename__ = "notes"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"), index=True)
    entity_type: Mapped[str] = mapped_column(String(32), index=True)
    entity_id: Mapped[str] = mapped_column(String(64), index=True)
    content: Mapped[str] = mapped_column(Text, default="")
    created_by: Mapped[str] = mapped_column(String(64), default="")
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)


# ═══════════════════════════════════════════════════════════════════
# Projects & Tasks
# ═══════════════════════════════════════════════════════════════════

class ProjectRecord(Base):
    """Project management."""
    __tablename__ = "projects"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"), index=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="active", index=True)  # active/on_hold/completed/cancelled
    priority: Mapped[str] = mapped_column(String(16), default="medium")  # low/medium/high/urgent
    start_date: Mapped[Date | None] = mapped_column(Date, nullable=True)
    end_date: Mapped[Date | None] = mapped_column(Date, nullable=True)
    budget_sar: Mapped[float | None] = mapped_column(Float, nullable=True)
    actual_cost_sar: Mapped[float] = mapped_column(Float, default=0.0)
    deal_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    client_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_by: Mapped[str] = mapped_column(String(64), default="")
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)
    deleted_at: Mapped[datetime | None] = mapped_column(nullable=True)

    __table_args__ = (Index("ix_projects_tenant_status", "tenant_id", "status"),)


class TaskRecordERP(Base):
    """Tasks within projects."""
    __tablename__ = "project_tasks"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"), index=True)
    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"), index=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="todo", index=True)  # todo/in_progress/review/done
    priority: Mapped[str] = mapped_column(String(16), default="medium")
    assigned_to: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    due_date: Mapped[Date | None] = mapped_column(Date, nullable=True)
    estimated_hours: Mapped[float | None] = mapped_column(Float, nullable=True)
    actual_hours: Mapped[float] = mapped_column(Float, default=0.0)
    parent_task_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_by: Mapped[str] = mapped_column(String(64), default="")
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)
    deleted_at: Mapped[datetime | None] = mapped_column(nullable=True)

    __table_args__ = (Index("ix_project_tasks_tenant_status", "tenant_id", "status"),)


class TimeEntryRecord(Base):
    """Time tracking per task."""
    __tablename__ = "time_entries"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"), index=True)
    task_id: Mapped[str] = mapped_column(ForeignKey("project_tasks.id"), index=True)
    user_id: Mapped[str] = mapped_column(String(64), index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    started_at: Mapped[datetime] = mapped_column()
    ended_at: Mapped[datetime | None] = mapped_column(nullable=True)
    duration_minutes: Mapped[int] = mapped_column(Integer, default=0)
    billable: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)


class MilestoneRecord(Base):
    """Project milestones."""
    __tablename__ = "milestones"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"), index=True)
    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"), index=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    due_date: Mapped[Date | None] = mapped_column(Date, nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)


# ═══════════════════════════════════════════════════════════════════
# Support Desk
# ═══════════════════════════════════════════════════════════════════

class TicketRecord(Base):
    """Customer support tickets."""
    __tablename__ = "tickets"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"), index=True)
    ticket_number: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    subject: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(32), default="open", index=True)  # open/pending/resolved/closed
    priority: Mapped[str] = mapped_column(String(16), default="medium", index=True)  # low/medium/high/urgent
    category: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    source: Mapped[str] = mapped_column(String(32), default="web")  # web/email/whatsapp/phone
    requester_email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    requester_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    assigned_to: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    sla_breach_at: Mapped[datetime | None] = mapped_column(nullable=True)
    resolved_at: Mapped[datetime | None] = mapped_column(nullable=True)
    satisfaction_rating: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)

    __table_args__ = (Index("ix_tickets_tenant_status", "tenant_id", "status"),)


class TicketCommentRecord(Base):
    """Comments/replies on tickets."""
    __tablename__ = "ticket_comments"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"), index=True)
    ticket_id: Mapped[str] = mapped_column(ForeignKey("tickets.id"), index=True)
    author_id: Mapped[str] = mapped_column(String(64))
    is_internal: Mapped[bool] = mapped_column(Boolean, default=False)
    body: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)


class KBArticleRecord(Base):
    """Knowledge base articles."""
    __tablename__ = "kb_articles"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"), index=True)
    category_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    title: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(255), index=True)
    content: Mapped[str] = mapped_column(Text, default="")
    is_published: Mapped[bool] = mapped_column(Boolean, default=False)
    view_count: Mapped[int] = mapped_column(Integer, default=0)
    created_by: Mapped[str] = mapped_column(String(64), default="")
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)


class KBCategoryRecord(Base):
    """Knowledge base categories."""
    __tablename__ = "kb_categories"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"), index=True)
    name: Mapped[str] = mapped_column(String(128))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)


# ═══════════════════════════════════════════════════════════════════
# Document Management
# ═══════════════════════════════════════════════════════════════════

class FolderRecord(Base):
    """Document folders."""
    __tablename__ = "folders"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"), index=True)
    parent_id: Mapped[str | None] = mapped_column(ForeignKey("folders.id"), nullable=True)
    name: Mapped[str] = mapped_column(String(255))
    path: Mapped[str] = mapped_column(String(512), default="")
    created_by: Mapped[str] = mapped_column(String(64), default="")
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)


class DocumentRecord(Base):
    """Uploaded documents."""
    __tablename__ = "documents"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"), index=True)
    folder_id: Mapped[str | None] = mapped_column(ForeignKey("folders.id"), nullable=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    original_name: Mapped[str] = mapped_column(String(255), default="")
    mime_type: Mapped[str] = mapped_column(String(128), default="")
    size_bytes: Mapped[int] = mapped_column(Integer, default=0)
    storage_key: Mapped[str] = mapped_column(String(512), default="")
    storage_provider: Mapped[str] = mapped_column(String(32), default="s3")  # s3/r2/local
    version: Mapped[int] = mapped_column(Integer, default=1)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    created_by: Mapped[str] = mapped_column(String(64), default="")
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)

    __table_args__ = (Index("ix_documents_tenant_folder", "tenant_id", "folder_id"),)


class DocumentPermissionRecord(Base):
    """Per-document access control."""
    __tablename__ = "document_permissions"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"), index=True)
    document_id: Mapped[str] = mapped_column(ForeignKey("documents.id"), index=True)
    user_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    role_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    permission: Mapped[str] = mapped_column(String(16), default="read")  # read/write/admin
    created_at: Mapped[datetime] = mapped_column(default=utcnow)


# ═══════════════════════════════════════════════════════════════════
# HR — Employees, Attendance, Leave, Payroll
# ═══════════════════════════════════════════════════════════════════

class EmployeeRecord(Base):
    """Employee master data."""
    __tablename__ = "employees"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"), index=True)
    user_id: Mapped[str | None] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)
    employee_number: Mapped[str] = mapped_column(String(32), default="")
    full_name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(32), nullable=True)
    national_id: Mapped[str | None] = mapped_column(String(20), nullable=True)
    department: Mapped[str | None] = mapped_column(String(128), nullable=True)
    job_title: Mapped[str | None] = mapped_column(String(128), nullable=True)
    employment_type: Mapped[str] = mapped_column(String(32), default="full_time")  # full_time/part_time/contract
    joining_date: Mapped[Date | None] = mapped_column(Date, nullable=True)
    termination_date: Mapped[Date | None] = mapped_column(Date, nullable=True)
    basic_salary_sar: Mapped[float] = mapped_column(Float, default=0.0)
    housing_allowance_sar: Mapped[float] = mapped_column(Float, default=0.0)
    transport_allowance_sar: Mapped[float] = mapped_column(Float, default=0.0)
    bank_iban: Mapped[str | None] = mapped_column(String(50), nullable=True)
    bank_name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="active", index=True)  # active/on_leave/terminated
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)
    deleted_at: Mapped[datetime | None] = mapped_column(nullable=True)

    __table_args__ = (Index("ix_employees_tenant_status", "tenant_id", "status"),)


class AttendanceRecord(Base):
    """Daily attendance records."""
    __tablename__ = "attendance"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"), index=True)
    employee_id: Mapped[str] = mapped_column(ForeignKey("employees.id"), index=True)
    date: Mapped[Date] = mapped_column(Date, index=True)
    check_in: Mapped[DateTime | None] = mapped_column(DateTime, nullable=True)
    check_out: Mapped[DateTime | None] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="present", index=True)  # present/absent/late/early_leave/on_leave
    work_hours: Mapped[float | None] = mapped_column(Float, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)

    __table_args__ = (
        UniqueConstraint("employee_id", "date", name="uq_attendance_employee_date"),
    )


class LeaveRecord(Base):
    """Leave requests."""
    __tablename__ = "leaves"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"), index=True)
    employee_id: Mapped[str] = mapped_column(ForeignKey("employees.id"), index=True)
    leave_type: Mapped[str] = mapped_column(String(32), index=True)  # annual/sick/hajj/maternity/unpaid/emergency
    start_date: Mapped[Date] = mapped_column(Date)
    end_date: Mapped[Date] = mapped_column(Date)
    days_count: Mapped[float] = mapped_column(Float, default=0.0)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="pending", index=True)  # pending/approved/rejected
    approved_by: Mapped[str | None] = mapped_column(String(64), nullable=True)
    approved_at: Mapped[datetime | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)


class PayrollRunRecord(Base):
    """Monthly payroll run."""
    __tablename__ = "payroll_runs"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"), index=True)
    period_month: Mapped[int] = mapped_column(Integer)  # 1-12
    period_year: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(32), default="draft", index=True)  # draft/processing/approved/paid
    total_basic_salary: Mapped[float] = mapped_column(Float, default=0.0)
    total_allowances: Mapped[float] = mapped_column(Float, default=0.0)
    total_deductions: Mapped[float] = mapped_column(Float, default=0.0)
    total_gosi_employer: Mapped[float] = mapped_column(Float, default=0.0)
    total_gosi_employee: Mapped[float] = mapped_column(Float, default=0.0)
    total_net_salary: Mapped[float] = mapped_column(Float, default=0.0)
    created_by: Mapped[str] = mapped_column(String(64), default="")
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)


class PayrollLineRecord(Base):
    """Individual employee payroll line."""
    __tablename__ = "payroll_lines"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"), index=True)
    payroll_run_id: Mapped[str] = mapped_column(ForeignKey("payroll_runs.id"), index=True)
    employee_id: Mapped[str] = mapped_column(ForeignKey("employees.id"), index=True)
    basic_salary: Mapped[float] = mapped_column(Float, default=0.0)
    housing_allowance: Mapped[float] = mapped_column(Float, default=0.0)
    transport_allowance: Mapped[float] = mapped_column(Float, default=0.0)
    other_earnings: Mapped[float] = mapped_column(Float, default=0.0)
    gosi_employer_pct: Mapped[float] = mapped_column(Float, default=0.0)
    gosi_employee_pct: Mapped[float] = mapped_column(Float, default=0.0)
    gosi_employer_amount: Mapped[float] = mapped_column(Float, default=0.0)
    gosi_employee_amount: Mapped[float] = mapped_column(Float, default=0.0)
    income_tax: Mapped[float] = mapped_column(Float, default=0.0)
    other_deductions: Mapped[float] = mapped_column(Float, default=0.0)
    net_salary: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)


# ═══════════════════════════════════════════════════════════════════
# Inventory & Procurement
# ═══════════════════════════════════════════════════════════════════

class WarehouseRecord(Base):
    """Inventory warehouses."""
    __tablename__ = "warehouses"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"), index=True)
    name: Mapped[str] = mapped_column(String(255))
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)


class InventoryItemRecord(Base):
    """SKU master data."""
    __tablename__ = "inventory_items"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"), index=True)
    sku: Mapped[str] = mapped_column(String(64), index=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    category: Mapped[str | None] = mapped_column(String(64), nullable=True)
    unit_of_measure: Mapped[str] = mapped_column(String(32), default="piece")  # piece/kg/liter/meter
    cost_price: Mapped[float] = mapped_column(Float, default=0.0)
    selling_price: Mapped[float] = mapped_column(Float, default=0.0)
    reorder_level: Mapped[int] = mapped_column(Integer, default=0)
    reorder_quantity: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)

    __table_args__ = (UniqueConstraint("tenant_id", "sku", name="uq_inventory_tenant_sku"),)


class StockMovementRecord(Base):
    """Inventory stock movements (in/out/adjustment)."""
    __tablename__ = "stock_movements"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"), index=True)
    warehouse_id: Mapped[str] = mapped_column(ForeignKey("warehouses.id"), index=True)
    item_id: Mapped[str] = mapped_column(ForeignKey("inventory_items.id"), index=True)
    movement_type: Mapped[str] = mapped_column(String(32), index=True)  # in/out/transfer/adjustment
    quantity: Mapped[float] = mapped_column(Float)
    unit_cost: Mapped[float] = mapped_column(Float, default=0.0)
    reference_type: Mapped[str | None] = mapped_column(String(32), nullable=True)  # purchase_order/sale/return
    reference_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_by: Mapped[str] = mapped_column(String(64), default="")
    created_at: Mapped[datetime] = mapped_column(default=utcnow)


class SupplierRecord(Base):
    """Suppliers for procurement."""
    __tablename__ = "suppliers"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"), index=True)
    name: Mapped[str] = mapped_column(String(255))
    contact_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(32), nullable=True)
    address: Mapped[str | None] = mapped_column(Text, nullable=True)
    vat_number: Mapped[str | None] = mapped_column(String(32), nullable=True)
    payment_terms_days: Mapped[int] = mapped_column(Integer, default=30)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)


class PurchaseOrderRecord(Base):
    """Purchase orders."""
    __tablename__ = "purchase_orders"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"), index=True)
    po_number: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    supplier_id: Mapped[str] = mapped_column(ForeignKey("suppliers.id"), index=True)
    warehouse_id: Mapped[str] = mapped_column(ForeignKey("warehouses.id"), index=True)
    status: Mapped[str] = mapped_column(String(32), default="draft", index=True)  # draft/sent/partial/received/closed/cancelled
    subtotal_sar: Mapped[float] = mapped_column(Float, default=0.0)
    vat_sar: Mapped[float] = mapped_column(Float, default=0.0)
    total_sar: Mapped[float] = mapped_column(Float, default=0.0)
    expected_delivery: Mapped[Date | None] = mapped_column(Date, nullable=True)
    received_at: Mapped[datetime | None] = mapped_column(nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_by: Mapped[str] = mapped_column(String(64), default="")
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)


class PurchaseOrderLineRecord(Base):
    """Lines within a purchase order."""
    __tablename__ = "purchase_order_lines"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"), index=True)
    po_id: Mapped[str] = mapped_column(ForeignKey("purchase_orders.id"), index=True)
    item_id: Mapped[str] = mapped_column(ForeignKey("inventory_items.id"), index=True)
    quantity_ordered: Mapped[float] = mapped_column(Float)
    quantity_received: Mapped[float] = mapped_column(Float, default=0.0)
    unit_price: Mapped[float] = mapped_column(Float, default=0.0)
    total_price: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)


# ═══════════════════════════════════════════════════════════════════
# Finance — General Ledger
# ═══════════════════════════════════════════════════════════════════

class GLAccountRecord(Base):
    """Chart of Accounts."""
    __tablename__ = "gl_accounts"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"), index=True)
    account_code: Mapped[str] = mapped_column(String(32), index=True)
    account_name: Mapped[str] = mapped_column(String(255))
    account_type: Mapped[str] = mapped_column(String(32), index=True)  # asset/liability/equity/revenue/expense
    parent_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    is_bank_account: Mapped[bool] = mapped_column(Boolean, default=False)
    bank_name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    iban: Mapped[str | None] = mapped_column(String(50), nullable=True)
    opening_balance: Mapped[float] = mapped_column(Float, default=0.0)
    current_balance: Mapped[float] = mapped_column(Float, default=0.0)
    currency: Mapped[str] = mapped_column(String(8), default="SAR")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)

    __table_args__ = (UniqueConstraint("tenant_id", "account_code", name="uq_gl_account_tenant_code"),)


class JournalEntryRecord(Base):
    """Double-entry journal entries."""
    __tablename__ = "journal_entries"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"), index=True)
    entry_number: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    date: Mapped[Date] = mapped_column(Date, index=True)
    description: Mapped[str] = mapped_column(Text, default="")
    reference_type: Mapped[str | None] = mapped_column(String(32), nullable=True)  # invoice/payment/payroll/manual
    reference_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    total_debit: Mapped[float] = mapped_column(Float, default=0.0)
    total_credit: Mapped[float] = mapped_column(Float, default=0.0)
    is_reversed: Mapped[bool] = mapped_column(Boolean, default=False)
    reversed_by: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_by: Mapped[str] = mapped_column(String(64), default="")
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)


class JournalEntryLineRecord(Base):
    """Individual lines in a journal entry."""
    __tablename__ = "journal_entry_lines"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"), index=True)
    journal_entry_id: Mapped[str] = mapped_column(ForeignKey("journal_entries.id"), index=True)
    account_id: Mapped[str] = mapped_column(ForeignKey("gl_accounts.id"), index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    debit: Mapped[float] = mapped_column(Float, default=0.0)
    credit: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)


class BankReconciliationRecord(Base):
    """Bank reconciliation statements."""
    __tablename__ = "bank_reconciliations"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"), index=True)
    account_id: Mapped[str] = mapped_column(ForeignKey("gl_accounts.id"), index=True)
    statement_date: Mapped[Date] = mapped_column(Date)
    statement_balance: Mapped[float] = mapped_column(Float)
    book_balance: Mapped[float] = mapped_column(Float)
    difference: Mapped[float] = mapped_column(Float, default=0.0)
    status: Mapped[str] = mapped_column(String(32), default="draft")  # draft/reconciled
    created_by: Mapped[str] = mapped_column(String(64), default="")
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)
