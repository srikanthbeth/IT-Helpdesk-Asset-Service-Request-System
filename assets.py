from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import crud
import schemas

from dependencies import get_db, admin_only

router = APIRouter(
    prefix="/assets",
    tags=["Assets"]
)


# ==========================================
# Create Asset
# ==========================================
@router.post("/", response_model=schemas.AssetResponse)
def create_asset(
    asset: schemas.AssetCreate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_only)
):
    return crud.create_asset(db, asset)


# ==========================================
# Get All Assets
# ==========================================
@router.get("/", response_model=list[schemas.AssetResponse])
def get_all_assets(
    db: Session = Depends(get_db),
    current_user=Depends(admin_only)
):
    return crud.get_assets(db)


# ==========================================
# Get Asset By ID
# ==========================================
@router.get("/{asset_id}", response_model=schemas.AssetResponse)
def get_asset(
    asset_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(admin_only)
):
    return crud.get_asset(db, asset_id)


# ==========================================
# Update Asset
# ==========================================
@router.put("/{asset_id}", response_model=schemas.AssetResponse)
def update_asset(
    asset_id: int,
    asset: schemas.AssetUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_only)
):
    return crud.update_asset(db, asset_id, asset)


# ==========================================
# Delete Asset
# ==========================================
@router.delete("/{asset_id}")
def delete_asset(
    asset_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(admin_only)
):
    return crud.delete_asset(db, asset_id)