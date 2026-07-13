from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import crud
import schemas

from dependencies import (
    get_db,
    admin_only
)

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


# ==========================================
# Requests By Employee
# ==========================================
@router.get(
    "/employee/{employee_id}",
    response_model=list[schemas.RequestResponse]
)
def employee_requests(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(admin_only)
):

    return crud.get_requests_by_employee(
        db,
        employee_id
    )


# ==========================================
# Requests By Asset
# ==========================================
@router.get(
    "/asset/{asset_id}",
    response_model=list[schemas.RequestResponse]
)
def asset_requests(
    asset_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(admin_only)
):

    return crud.get_requests_by_asset(
        db,
        asset_id
    )


# ==========================================
# Search + Pagination
# ==========================================
@router.get(
    "/",
    response_model=list[schemas.RequestResponse]
)
def search_requests(
    priority: Optional[str] = None,
    status: Optional[str] = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(admin_only)
):

    return crud.search_requests(
        db,
        priority,
        status,
        page,
        limit
    )