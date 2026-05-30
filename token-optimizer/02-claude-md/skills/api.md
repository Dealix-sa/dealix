# Dealix — API Context (On-Demand Skill)

## Framework
FastAPI 0.110+ · Pydantic v2 · Bearer JWT auth

## Router Structure
```
api/
├── routes/
│   ├── clients.py    # /api/v1/clients
│   ├── deals.py      # /api/v1/deals
│   ├── contacts.py   # /api/v1/contacts
│   ├── auth.py       # /api/v1/auth
│   └── analytics.py  # /api/v1/analytics
└── deps.py           # shared dependencies (get_db, get_current_user)
```

## Conventions
- All responses: `{"data": ..., "meta": {...}}`
- Error format: `{"detail": "message", "code": "ERROR_CODE"}`
- Auth: `Authorization: Bearer <token>` header
- Pagination: `?page=1&page_size=20`
- Arabic fields suffix: `_ar` (e.g., `name_ar`)

## Adding a New Endpoint
```python
from fastapi import APIRouter, Depends
from api.deps import get_db, get_current_user

router = APIRouter(prefix="/resource", tags=["resource"])

@router.get("/")
async def list_resource(db=Depends(get_db), user=Depends(get_current_user)):
    ...
```
