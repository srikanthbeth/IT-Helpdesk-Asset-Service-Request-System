from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import crud
import schemas

from dependencies import (
    get_db,
    employee_only,
    get_current_user
)

router = APIRouter(
    prefix="/requests",
    tags=["Service Requests"]
)


# ======================================
# Create Request
# ======================================
@router.post("/", response_model=schemas.RequestResponse)
def create_request(
    request: schemas.RequestCreate,
    db: Session = Depends(get_db),
    current_user=Depends(employee_only)
):
    return crud.create_request(
        db,
        request,
        current_user.id
    )


# ======================================
# Get All Requests
# ======================================
@router.get("/", response_model=list[schemas.RequestResponse])
def get_requests(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return crud.get_requests(
    db,
    current_user
)


# ======================================
# Get Request By ID
# ======================================
@router.get("/{request_id}", response_model=schemas.RequestResponse)
def get_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return crud.get_request(
    db,
    request_id,
    current_user
)


# ======================================
# Update Request
# ======================================
@router.put("/{request_id}", response_model=schemas.RequestResponse)
def update_request(
    request_id: int,
    request: schemas.RequestUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return crud.update_request(
        db,
        request_id,
        request,
        current_user
    )