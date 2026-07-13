from sqlalchemy.orm import Session
from fastapi import HTTPException, status

import models
import schemas
from auth import hash_password, verify_password


# =====================================================
# Register User
# =====================================================

def register_user(db: Session, user: schemas.UserRegister):

    # Check if email already exists
    existing_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user
    new_user = models.User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# =====================================================
# Login User
# =====================================================

def login_user(db: Session, email: str, password: str):

    user = db.query(models.User).filter(
        models.User.email == email
    ).first()

    if not user:
        return None

    if not verify_password(password, user.password):
        return None

    return user

# =====================================================
# Asset CRUD
# =====================================================

def create_asset(db: Session, asset: schemas.AssetCreate):

    # Check unique asset tag
    existing_asset = db.query(models.Asset).filter(
        models.Asset.asset_tag == asset.asset_tag
    ).first()

    if existing_asset:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Asset Tag already exists"
        )

    new_asset = models.Asset(
        asset_name=asset.asset_name,
        asset_tag=asset.asset_tag,
        asset_type=asset.asset_type,
        serial_number=asset.serial_number,
        status=asset.status
    )

    db.add(new_asset)
    db.commit()
    db.refresh(new_asset)

    return new_asset


def get_assets(db: Session):
    return db.query(models.Asset).all()


def get_asset(db: Session, asset_id: int):

    asset = db.query(models.Asset).filter(
        models.Asset.id == asset_id
    ).first()

    if not asset:
        raise HTTPException(
            status_code=404,
            detail="Asset not found"
        )

    return asset


def update_asset(db: Session, asset_id: int, asset: schemas.AssetUpdate):

    db_asset = db.query(models.Asset).filter(
        models.Asset.id == asset_id
    ).first()

    if not db_asset:
        raise HTTPException(
            status_code=404,
            detail="Asset not found"
        )

    duplicate = db.query(models.Asset).filter(
        models.Asset.asset_tag == asset.asset_tag,
        models.Asset.id != asset_id
    ).first()

    if duplicate:
        raise HTTPException(
            status_code=400,
            detail="Asset Tag already exists"
        )

    db_asset.asset_name = asset.asset_name
    db_asset.asset_tag = asset.asset_tag
    db_asset.asset_type = asset.asset_type
    db_asset.serial_number = asset.serial_number
    db_asset.status = asset.status

    db.commit()
    db.refresh(db_asset)

    return db_asset


def delete_asset(db: Session, asset_id: int):

    asset = db.query(models.Asset).filter(
        models.Asset.id == asset_id
    ).first()

    if not asset:
        raise HTTPException(
            status_code=404,
            detail="Asset not found"
        )

    db.delete(asset)
    db.commit()

    return {"message": "Asset deleted successfully"}

# =====================================================
# Service Request CRUD
# =====================================================

from datetime import datetime


def create_request(db: Session, request: schemas.RequestCreate, employee_id: int):

    asset = db.query(models.Asset).filter(
        models.Asset.id == request.asset_id
    ).first()

    if not asset:
        raise HTTPException(
            status_code=404,
            detail="Asset not found"
        )

    new_request = models.ServiceRequest(
        employee_id=employee_id,
        asset_id=request.asset_id,
        issue_title=request.issue_title,
        description=request.description,
        priority=request.priority,
        status="Open"
    )

    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    return new_request





def get_requests(db: Session, current_user):

    if current_user.role == "Admin":
        return db.query(models.ServiceRequest).all()

    elif current_user.role == "Employee":
        return db.query(models.ServiceRequest).filter(
            models.ServiceRequest.employee_id == current_user.id
        ).all()

    elif current_user.role == "IT Support":
        return db.query(models.ServiceRequest).filter(
            models.ServiceRequest.support_id == current_user.id
        ).all()

    return []

def get_request(
    db: Session,
    request_id: int,
    current_user
):

    request = db.query(models.ServiceRequest).filter(
        models.ServiceRequest.id == request_id
    ).first()

    if not request:
        raise HTTPException(
            status_code=404,
            detail="Request not found"
        )

    if current_user.role == "Employee":

        if request.employee_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="Access Denied"
            )

    if current_user.role == "IT Support":

        if request.support_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="Access Denied"
            )

    return request


from datetime import datetime

def update_request(
    db: Session,
    request_id: int,
    request: schemas.RequestUpdate,
    current_user
):

    db_request = db.query(models.ServiceRequest).filter(
        models.ServiceRequest.id == request_id
    ).first()

    if not db_request:
        raise HTTPException(
            status_code=404,
            detail="Request not found"
        )

    if db_request.status == "Closed":
        raise HTTPException(
            status_code=400,
            detail="Closed requests cannot be edited"
        )

    # Only assigned IT Support can update
    if current_user.role == "IT Support":

        if db_request.support_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="You are not assigned to this request"
            )

    db_request.issue_title = request.issue_title
    db_request.description = request.description
    db_request.priority = request.priority
    db_request.status = request.status

    if request.status == "Resolved":
        db_request.resolved_at = datetime.utcnow()

    db.commit()
    db.refresh(db_request)

    return db_request

# =====================================================
# Assign Request to IT Support
# =====================================================

def assign_request(
    db: Session,
    request_id: int,
    support_id: int
):

    request = db.query(models.ServiceRequest).filter(
        models.ServiceRequest.id == request_id
    ).first()

    if not request:
        raise HTTPException(
            status_code=404,
            detail="Request not found"
        )

    support = db.query(models.User).filter(
        models.User.id == support_id,
        models.User.role == "IT Support"
    ).first()

    if not support:
        raise HTTPException(
            status_code=404,
            detail="IT Support user not found"
        )

    request.support_id = support_id
    request.status = "Assigned"

    db.commit()
    db.refresh(request)

    return request


# =====================================================
# Get Assigned Requests
# =====================================================

def get_support_requests(
    db: Session,
    support_id: int
):

    return db.query(models.ServiceRequest).filter(
        models.ServiceRequest.support_id == support_id
    ).all()

# =====================================================
# Reports
# =====================================================

def get_requests_by_employee(db: Session, employee_id: int):
    return db.query(models.ServiceRequest).filter(
        models.ServiceRequest.employee_id == employee_id
    ).all()


def get_requests_by_asset(db: Session, asset_id: int):
    return db.query(models.ServiceRequest).filter(
        models.ServiceRequest.asset_id == asset_id
    ).all()


def search_requests(
    db: Session,
    priority: str = None,
    status: str = None,
    page: int = 1,
    limit: int = 10
):

    query = db.query(models.ServiceRequest)

    if priority:
        query = query.filter(
            models.ServiceRequest.priority == priority
        )

    if status:
        query = query.filter(
            models.ServiceRequest.status == status
        )

    skip = (page - 1) * limit

    return query.offset(skip).limit(limit).all()