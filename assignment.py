from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import crud
import schemas

from dependencies import (
    get_db,
    admin_only
)

router = APIRouter(
    tags=["Assignment"]
)


# ======================================
# Assign Request
# ======================================
@router.post("/requests/{request_id}/assign/{support_id}")
def assign_request(
    request_id: int,
    support_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(admin_only)
):

    return crud.assign_request(
        db,
        request_id,
        support_id
    )


# ======================================
# Support Assigned Requests
# ======================================
@router.get("/support/{support_id}/requests",
response_model=list[schemas.RequestResponse])
def support_requests(
    support_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(admin_only)
):

    return crud.get_support_requests(
        db,
        support_id
    )