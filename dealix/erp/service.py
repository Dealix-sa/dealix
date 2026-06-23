"""
ERP Suite Service — Projects, Support, Documents, HR, Inventory, Finance.
"""

from __future__ import annotations

import uuid
from datetime import date, datetime, timedelta
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.utils import utcnow
from db.models_erp import (
    ActivityRecord,
    AttendanceRecord,
    DocumentRecord,
    EmployeeRecord,
    FolderRecord,
    GLAccountRecord,
    InventoryItemRecord,
    JournalEntryLineRecord,
    JournalEntryRecord,
    LeaveRecord,
    MilestoneRecord,
    NoteRecord,
    PayrollLineRecord,
    PayrollRunRecord,
    ProjectRecord,
    PurchaseOrderLineRecord,
    PurchaseOrderRecord,
    StockMovementRecord,
    SupplierRecord,
    TaskRecordERP,
    TicketCommentRecord,
    TicketRecord,
    TimeEntryRecord,
    WarehouseRecord,
)


class ERPService:
    """Unified ERP service for all modules."""

    def __init__(self, session: AsyncSession):
        self.session = session

    # ── Projects ───────────────────────────────────────────────────

    async def create_project(self, tenant_id: str, data: dict) -> ProjectRecord:
        p = ProjectRecord(
            id=f"prj_{uuid.uuid4().hex[:12]}",
            tenant_id=tenant_id,
            name=data["name"],
            description=data.get("description"),
            status=data.get("status", "active"),
            priority=data.get("priority", "medium"),
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
            budget_sar=data.get("budget_sar"),
            deal_id=data.get("deal_id"),
            client_id=data.get("client_id"),
            created_by=data.get("created_by", ""),
            created_at=utcnow(),
            updated_at=utcnow(),
        )
        self.session.add(p)
        await self.session.flush()
        return p

    async def list_projects(self, tenant_id: str, status: str | None = None) -> list[ProjectRecord]:
        stmt = select(ProjectRecord).where(
            ProjectRecord.tenant_id == tenant_id,
            ProjectRecord.deleted_at.is_(None),
        )
        if status:
            stmt = stmt.where(ProjectRecord.status == status)
        stmt = stmt.order_by(ProjectRecord.created_at.desc())
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def create_task(self, tenant_id: str, project_id: str, data: dict) -> TaskRecordERP:
        t = TaskRecordERP(
            id=f"tsk_{uuid.uuid4().hex[:12]}",
            tenant_id=tenant_id,
            project_id=project_id,
            name=data["name"],
            description=data.get("description"),
            status=data.get("status", "todo"),
            priority=data.get("priority", "medium"),
            assigned_to=data.get("assigned_to"),
            due_date=data.get("due_date"),
            estimated_hours=data.get("estimated_hours"),
            parent_task_id=data.get("parent_task_id"),
            created_by=data.get("created_by", ""),
            created_at=utcnow(),
            updated_at=utcnow(),
        )
        self.session.add(t)
        await self.session.flush()
        return t

    async def list_tasks(self, tenant_id: str, project_id: str | None = None) -> list[TaskRecordERP]:
        stmt = select(TaskRecordERP).where(
            TaskRecordERP.tenant_id == tenant_id,
            TaskRecordERP.deleted_at.is_(None),
        )
        if project_id:
            stmt = stmt.where(TaskRecordERP.project_id == project_id)
        stmt = stmt.order_by(TaskRecordERP.created_at.desc())
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def create_time_entry(self, tenant_id: str, task_id: str, data: dict) -> TimeEntryRecord:
        te = TimeEntryRecord(
            id=f"te_{uuid.uuid4().hex[:12]}",
            tenant_id=tenant_id,
            task_id=task_id,
            user_id=data["user_id"],
            description=data.get("description"),
            started_at=data.get("started_at", utcnow()),
            ended_at=data.get("ended_at"),
            duration_minutes=data.get("duration_minutes", 0),
            billable=data.get("billable", True),
            created_at=utcnow(),
        )
        self.session.add(te)
        await self.session.flush()
        return te

    # ── Support Desk ───────────────────────────────────────────────

    async def create_ticket(self, tenant_id: str, data: dict) -> TicketRecord:
        ticket_num = f"TKT-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:4].upper()}"
        t = TicketRecord(
            id=f"tkt_{uuid.uuid4().hex[:12]}",
            tenant_id=tenant_id,
            ticket_number=ticket_num,
            subject=data["subject"],
            description=data.get("description", ""),
            priority=data.get("priority", "medium"),
            category=data.get("category"),
            source=data.get("source", "web"),
            requester_email=data.get("requester_email"),
            requester_name=data.get("requester_name"),
            assigned_to=data.get("assigned_to"),
            status="open",
            created_at=utcnow(),
            updated_at=utcnow(),
        )
        self.session.add(t)
        await self.session.flush()
        return t

    async def list_tickets(self, tenant_id: str, status: str | None = None) -> list[TicketRecord]:
        stmt = select(TicketRecord).where(TicketRecord.tenant_id == tenant_id)
        if status:
            stmt = stmt.where(TicketRecord.status == status)
        stmt = stmt.order_by(TicketRecord.created_at.desc())
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def add_ticket_comment(self, tenant_id: str, ticket_id: str, data: dict) -> TicketCommentRecord:
        c = TicketCommentRecord(
            id=f"tc_{uuid.uuid4().hex[:12]}",
            tenant_id=tenant_id,
            ticket_id=ticket_id,
            author_id=data["author_id"],
            is_internal=data.get("is_internal", False),
            body=data["body"],
            created_at=utcnow(),
        )
        self.session.add(c)
        await self.session.flush()
        return c

    # ── Documents ──────────────────────────────────────────────────

    async def create_folder(self, tenant_id: str, data: dict) -> FolderRecord:
        f = FolderRecord(
            id=f"fld_{uuid.uuid4().hex[:12]}",
            tenant_id=tenant_id,
            parent_id=data.get("parent_id"),
            name=data["name"],
            path=data.get("path", ""),
            created_by=data.get("created_by", ""),
            created_at=utcnow(),
            updated_at=utcnow(),
        )
        self.session.add(f)
        await self.session.flush()
        return f

    async def create_document(self, tenant_id: str, data: dict) -> DocumentRecord:
        d = DocumentRecord(
            id=f"doc_{uuid.uuid4().hex[:12]}",
            tenant_id=tenant_id,
            folder_id=data.get("folder_id"),
            name=data["name"],
            original_name=data.get("original_name", ""),
            mime_type=data.get("mime_type", ""),
            size_bytes=data.get("size_bytes", 0),
            storage_key=data.get("storage_key", ""),
            storage_provider=data.get("storage_provider", "s3"),
            created_by=data.get("created_by", ""),
            created_at=utcnow(),
            updated_at=utcnow(),
        )
        self.session.add(d)
        await self.session.flush()
        return d

    async def list_documents(self, tenant_id: str, folder_id: str | None = None) -> list[DocumentRecord]:
        stmt = select(DocumentRecord).where(
            DocumentRecord.tenant_id == tenant_id,
            DocumentRecord.is_deleted == False,
        )
        if folder_id:
            stmt = stmt.where(DocumentRecord.folder_id == folder_id)
        stmt = stmt.order_by(DocumentRecord.created_at.desc())
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    # ── HR ─────────────────────────────────────────────────────────

    async def create_employee(self, tenant_id: str, data: dict) -> EmployeeRecord:
        e = EmployeeRecord(
            id=f"emp_{uuid.uuid4().hex[:12]}",
            tenant_id=tenant_id,
            user_id=data.get("user_id"),
            employee_number=data.get("employee_number", ""),
            full_name=data["full_name"],
            email=data.get("email"),
            phone=data.get("phone"),
            national_id=data.get("national_id"),
            department=data.get("department"),
            job_title=data.get("job_title"),
            employment_type=data.get("employment_type", "full_time"),
            joining_date=data.get("joining_date"),
            basic_salary_sar=data.get("basic_salary_sar", 0.0),
            housing_allowance_sar=data.get("housing_allowance_sar", 0.0),
            transport_allowance_sar=data.get("transport_allowance_sar", 0.0),
            bank_iban=data.get("bank_iban"),
            bank_name=data.get("bank_name"),
            status="active",
            created_at=utcnow(),
            updated_at=utcnow(),
        )
        self.session.add(e)
        await self.session.flush()
        return e

    async def list_employees(self, tenant_id: str) -> list[EmployeeRecord]:
        stmt = (
            select(EmployeeRecord)
            .where(EmployeeRecord.tenant_id == tenant_id, EmployeeRecord.deleted_at.is_(None))
            .order_by(EmployeeRecord.full_name)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def record_attendance(self, tenant_id: str, data: dict) -> AttendanceRecord:
        a = AttendanceRecord(
            id=f"att_{uuid.uuid4().hex[:12]}",
            tenant_id=tenant_id,
            employee_id=data["employee_id"],
            date=data["date"],
            check_in=data.get("check_in"),
            check_out=data.get("check_out"),
            status=data.get("status", "present"),
            work_hours=data.get("work_hours"),
            notes=data.get("notes"),
            created_at=utcnow(),
        )
        self.session.add(a)
        await self.session.flush()
        return a

    async def create_leave_request(self, tenant_id: str, data: dict) -> LeaveRecord:
        l = LeaveRecord(
            id=f"lve_{uuid.uuid4().hex[:12]}",
            tenant_id=tenant_id,
            employee_id=data["employee_id"],
            leave_type=data["leave_type"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            days_count=data.get("days_count", 0.0),
            reason=data.get("reason"),
            status="pending",
            created_at=utcnow(),
            updated_at=utcnow(),
        )
        self.session.add(l)
        await self.session.flush()
        return l

    async def process_payroll(self, tenant_id: str, month: int, year: int) -> PayrollRunRecord:
        # Fetch all active employees
        stmt = select(EmployeeRecord).where(
            EmployeeRecord.tenant_id == tenant_id,
            EmployeeRecord.status == "active",
            EmployeeRecord.deleted_at.is_(None),
        )
        result = await self.session.execute(stmt)
        employees = result.scalars().all()

        pr = PayrollRunRecord(
            id=f"pr_{uuid.uuid4().hex[:12]}",
            tenant_id=tenant_id,
            period_month=month,
            period_year=year,
            status="draft",
            created_at=utcnow(),
            updated_at=utcnow(),
        )
        self.session.add(pr)
        await self.session.flush()

        total_basic = total_allowances = total_gosi_emp = total_gosi_emp_pct = total_net = 0.0

        for emp in employees:
            gosi_emp = emp.basic_salary_sar * 0.0975  # Employee GOSI = 9.75%
            gosi_emp_pct = 0.0975
            gosi_employer = emp.basic_salary_sar * 0.11  # Employer GOSI = 11%
            allowances = emp.housing_allowance_sar + emp.transport_allowance_sar
            net = emp.basic_salary_sar + allowances - gosi_emp

            pl = PayrollLineRecord(
                id=f"pl_{uuid.uuid4().hex[:12]}",
                tenant_id=tenant_id,
                payroll_run_id=pr.id,
                employee_id=emp.id,
                basic_salary=emp.basic_salary_sar,
                housing_allowance=emp.housing_allowance_sar,
                transport_allowance=emp.transport_allowance_sar,
                gosi_employer_pct=0.11,
                gosi_employee_pct=gosi_emp_pct,
                gosi_employer_amount=gosi_employer,
                gosi_employee_amount=gosi_emp,
                net_salary=net,
                created_at=utcnow(),
            )
            self.session.add(pl)

            total_basic += emp.basic_salary_sar
            total_allowances += allowances
            total_gosi_emp += gosi_emp
            total_gosi_emp_pct += gosi_emp
            total_net += net

        pr.total_basic_salary = total_basic
        pr.total_allowances = total_allowances
        pr.total_gosi_employee = total_gosi_emp
        pr.total_net_salary = total_net
        await self.session.flush()
        return pr

    # ── Inventory ──────────────────────────────────────────────────

    async def create_warehouse(self, tenant_id: str, data: dict) -> WarehouseRecord:
        w = WarehouseRecord(
            id=f"wh_{uuid.uuid4().hex[:12]}",
            tenant_id=tenant_id,
            name=data["name"],
            location=data.get("location"),
            created_at=utcnow(),
            updated_at=utcnow(),
        )
        self.session.add(w)
        await self.session.flush()
        return w

    async def create_inventory_item(self, tenant_id: str, data: dict) -> InventoryItemRecord:
        item = InventoryItemRecord(
            id=f"inv_{uuid.uuid4().hex[:12]}",
            tenant_id=tenant_id,
            sku=data["sku"],
            name=data["name"],
            description=data.get("description"),
            category=data.get("category"),
            unit_of_measure=data.get("unit_of_measure", "piece"),
            cost_price=data.get("cost_price", 0.0),
            selling_price=data.get("selling_price", 0.0),
            reorder_level=data.get("reorder_level", 0),
            reorder_quantity=data.get("reorder_quantity", 0),
            created_at=utcnow(),
            updated_at=utcnow(),
        )
        self.session.add(item)
        await self.session.flush()
        return item

    async def record_stock_movement(self, tenant_id: str, data: dict) -> StockMovementRecord:
        sm = StockMovementRecord(
            id=f"sm_{uuid.uuid4().hex[:12]}",
            tenant_id=tenant_id,
            warehouse_id=data["warehouse_id"],
            item_id=data["item_id"],
            movement_type=data["movement_type"],
            quantity=data["quantity"],
            unit_cost=data.get("unit_cost", 0.0),
            reference_type=data.get("reference_type"),
            reference_id=data.get("reference_id"),
            notes=data.get("notes"),
            created_by=data.get("created_by", ""),
            created_at=utcnow(),
        )
        self.session.add(sm)
        await self.session.flush()
        return sm

    async def get_stock_for_item(self, tenant_id: str, item_id: str) -> float:
        stmt = select(func.sum(StockMovementRecord.quantity)).where(
            StockMovementRecord.tenant_id == tenant_id,
            StockMovementRecord.item_id == item_id,
        )
        result = await self.session.execute(stmt)
        return result.scalar() or 0.0

    async def create_supplier(self, tenant_id: str, data: dict) -> SupplierRecord:
        s = SupplierRecord(
            id=f"sup_{uuid.uuid4().hex[:12]}",
            tenant_id=tenant_id,
            name=data["name"],
            contact_name=data.get("contact_name"),
            email=data.get("email"),
            phone=data.get("phone"),
            address=data.get("address"),
            vat_number=data.get("vat_number"),
            payment_terms_days=data.get("payment_terms_days", 30),
            created_at=utcnow(),
            updated_at=utcnow(),
        )
        self.session.add(s)
        await self.session.flush()
        return s

    async def create_purchase_order(self, tenant_id: str, data: dict) -> PurchaseOrderRecord:
        po_num = f"PO-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:4].upper()}"
        po = PurchaseOrderRecord(
            id=f"po_{uuid.uuid4().hex[:12]}",
            tenant_id=tenant_id,
            po_number=po_num,
            supplier_id=data["supplier_id"],
            warehouse_id=data["warehouse_id"],
            status="draft",
            expected_delivery=data.get("expected_delivery"),
            notes=data.get("notes"),
            created_by=data.get("created_by", ""),
            created_at=utcnow(),
            updated_at=utcnow(),
        )
        self.session.add(po)
        await self.session.flush()

        # Add lines
        subtotal = 0.0
        for line in data.get("lines", []):
            total = line["quantity"] * line["unit_price"]
            pol = PurchaseOrderLineRecord(
                id=f"pol_{uuid.uuid4().hex[:12]}",
                tenant_id=tenant_id,
                po_id=po.id,
                item_id=line["item_id"],
                quantity_ordered=line["quantity"],
                unit_price=line["unit_price"],
                total_price=total,
                created_at=utcnow(),
            )
            self.session.add(pol)
            subtotal += total

        po.subtotal_sar = subtotal
        po.vat_sar = round(subtotal * 0.15, 2)
        po.total_sar = po.subtotal_sar + po.vat_sar
        await self.session.flush()
        return po

    # ── Finance GL ─────────────────────────────────────────────────

    async def create_gl_account(self, tenant_id: str, data: dict) -> GLAccountRecord:
        a = GLAccountRecord(
            id=f"gl_{uuid.uuid4().hex[:12]}",
            tenant_id=tenant_id,
            account_code=data["account_code"],
            account_name=data["account_name"],
            account_type=data["account_type"],
            parent_id=data.get("parent_id"),
            is_bank_account=data.get("is_bank_account", False),
            bank_name=data.get("bank_name"),
            iban=data.get("iban"),
            opening_balance=data.get("opening_balance", 0.0),
            current_balance=data.get("opening_balance", 0.0),
            currency=data.get("currency", "SAR"),
            created_at=utcnow(),
            updated_at=utcnow(),
        )
        self.session.add(a)
        await self.session.flush()
        return a

    async def list_gl_accounts(self, tenant_id: str) -> list[GLAccountRecord]:
        stmt = select(GLAccountRecord).where(
            GLAccountRecord.tenant_id == tenant_id,
            GLAccountRecord.is_active == True,
        ).order_by(GLAccountRecord.account_code)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def create_journal_entry(self, tenant_id: str, data: dict) -> JournalEntryRecord:
        entry_num = f"JE-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:4].upper()}"
        je = JournalEntryRecord(
            id=f"je_{uuid.uuid4().hex[:12]}",
            tenant_id=tenant_id,
            entry_number=entry_num,
            date=data.get("date", date.today()),
            description=data.get("description", ""),
            reference_type=data.get("reference_type"),
            reference_id=data.get("reference_id"),
            total_debit=0.0,
            total_credit=0.0,
            created_by=data.get("created_by", ""),
            created_at=utcnow(),
            updated_at=utcnow(),
        )
        self.session.add(je)
        await self.session.flush()

        total_debit = total_credit = 0.0
        for line in data.get("lines", []):
            jl = JournalEntryLineRecord(
                id=f"jel_{uuid.uuid4().hex[:12]}",
                tenant_id=tenant_id,
                journal_entry_id=je.id,
                account_id=line["account_id"],
                description=line.get("description"),
                debit=line.get("debit", 0.0),
                credit=line.get("credit", 0.0),
                created_at=utcnow(),
            )
            self.session.add(jl)
            total_debit += line.get("debit", 0.0)
            total_credit += line.get("credit", 0.0)

            # Update account balance
            account = await self.session.get(GLAccountRecord, line["account_id"])
            if account:
                account.current_balance += line.get("debit", 0.0) - line.get("credit", 0.0)

        je.total_debit = total_debit
        je.total_credit = total_credit
        await self.session.flush()
        return je

    async def get_trial_balance(self, tenant_id: str) -> list[dict[str, Any]]:
        stmt = select(GLAccountRecord).where(
            GLAccountRecord.tenant_id == tenant_id,
            GLAccountRecord.is_active == True,
        ).order_by(GLAccountRecord.account_code)
        result = await self.session.execute(stmt)
        accounts = result.scalars().all()
        return [
            {
                "account_code": a.account_code,
                "account_name": a.account_name,
                "account_type": a.account_type,
                "balance": a.current_balance,
            }
            for a in accounts
        ]
