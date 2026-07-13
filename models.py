from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base


# ----------------------------
# User Model
# ----------------------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)

    # Employee Requests
    employee_requests = relationship(
        "ServiceRequest",
        foreign_keys="ServiceRequest.employee_id",
        back_populates="employee"
    )

    # Assigned Support Requests
    support_requests = relationship(
        "ServiceRequest",
        foreign_keys="ServiceRequest.support_id",
        back_populates="support"
    )


# ----------------------------
# Asset Model
# ----------------------------
class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    asset_name = Column(String, nullable=False)
    asset_tag = Column(String, unique=True, nullable=False, index=True)
    asset_type = Column(String, nullable=False)
    serial_number = Column(String, nullable=False)
    status = Column(String, nullable=False)

    requests = relationship(
        "ServiceRequest",
        back_populates="asset",
        cascade="all, delete"
    )


# ----------------------------
# Service Request Model
# ----------------------------
class ServiceRequest(Base):
    __tablename__ = "service_requests"

    id = Column(Integer, primary_key=True, index=True)

    employee_id = Column(Integer, ForeignKey("users.id"))
    asset_id = Column(Integer, ForeignKey("assets.id"))
    support_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    issue_title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    priority = Column(String, nullable=False)
    status = Column(String, default="Open")

    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)

    employee = relationship(
        "User",
        foreign_keys=[employee_id],
        back_populates="employee_requests"
    )

    support = relationship(
        "User",
        foreign_keys=[support_id],
        back_populates="support_requests"
    )

    asset = relationship(
        "Asset",
        back_populates="requests"
    )