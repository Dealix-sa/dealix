"""
Inventory & Procurement API.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from api.security.auth_deps import get_current_user
from db.session import get_db as get_db_session
from dealix.erp.service import ERPService
from dealix.feature_gating.service import FeatureGate

router = APIRouter(prefix="/api/v1/erp/inventory", tags=["ERP — Inventory"])


class WarehouseCreate(BaseModel):
    name: str
    location: str | None = None


class ItemCreate(BaseModel):
    sku: str
    name: str
    description: str | None = None
    category: str | None = None
    unit_of_measure: str = "piece"
    cost_price: float = 0.0
    selling_price: float = 0.0
    reorder_level: int = 0
    reorder_quantity: int = 0


class StockMovementCreate(BaseModel):
    warehouse_id: str
    item_id: str
    movement_type: str
    quantity: float
    unit_cost: float = 0.0
    notes: str | None = None


class SupplierCreate(BaseModel):
    name: str
    contact_name: str | None = None
    email: str | None = None
    phone: str | None = None
    address: str | None = None
    vat_number: str | None = None


class POCreate(BaseModel):
    supplier_id: str
    warehouse_id: str
    lines: list[dict]
    expected_delivery: str | None = None
    notes: str | None = None


@router.post("/warehouses", dependencies=[Depends(FeatureGate("inventory"))])
async def create_warehouse(
    req: WarehouseCreate,
    session: AsyncSession = Depends(get_db_session),
    current_user=Depends(get_current_user),
) -> dict[str, Any]:
    svc = ERPService(session)
    w = await svc.create_warehouse(current_user.tenant_id, req.dict(exclude_none=True))
    await session.commit()
    return {"id": w.id, "name": w.name}


@router.post("/items", dependencies=[Depends(FeatureGate("inventory"))])
async def create_item(
    req: ItemCreate,
    session: AsyncSession = Depends(get_db_session),
    current_user=Depends(get_current_user),
) -> dict[str, Any]:
    svc = ERPService(session)
    item = await svc.create_inventory_item(current_user.tenant_id, req.dict(exclude_none=True))
    await session.commit()
    return {"id": item.id, "sku": item.sku, "name": item.name}


@router.post("/movements", dependencies=[Depends(FeatureGate("inventory"))])
async def record_movement(
    req: StockMovementCreate,
    session: AsyncSession = Depends(get_db_session),
    current_user=Depends(get_current_user),
) -> dict[str, Any]:
    svc = ERPService(session)
    sm = await svc.record_stock_movement(current_user.tenant_id, {
        **req.dict(exclude_none=True),
        "created_by": current_user.id,
    })
    await session.commit()
    return {"id": sm.id, "quantity": sm.quantity, "movement_type": sm.movement_type}


@router.get("/items/{item_id}/stock")
async def get_stock(
    item_id: str,
    session: AsyncSession = Depends(get_db_session),
    current_user=Depends(get_current_user),
) -> dict[str, Any]:
    svc = ERPService(session)
    stock = await svc.get_stock_for_item(current_user.tenant_id, item_id)
    return {"item_id": item_id, "current_stock": stock}


@router.post("/suppliers", dependencies=[Depends(FeatureGate("inventory"))])
async def create_supplier(
    req: SupplierCreate,
    session: AsyncSession = Depends(get_db_session),
    current_user=Depends(get_current_user),
) -> dict[str, Any]:
    svc = ERPService(session)
    s = await svc.create_supplier(current_user.tenant_id, req.dict(exclude_none=True))
    await session.commit()
    return {"id": s.id, "name": s.name}


@router.post("/purchase-orders", dependencies=[Depends(FeatureGate("inventory"))])
async def create_po(
    req: POCreate,
    session: AsyncSession = Depends(get_db_session),
    current_user=Depends(get_current_user),
) -> dict[str, Any]:
    svc = ERPService(session)
    po = await svc.create_purchase_order(current_user.tenant_id, {
        **req.dict(exclude_none=True),
        "created_by": current_user.id,
    })
    await session.commit()
    return {"id": po.id, "po_number": po.po_number, "total_sar": po.total_sar}
