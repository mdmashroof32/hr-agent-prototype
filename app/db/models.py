from sqlalchemy import Column, Integer, String, JSON, DateTime, func
from sqlalchemy.orm import relationship
from app.db.session import Base

class ActionRecord(Base):
    __tablename__ = "action_records"
    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(String, unique=True, index=True)
    action_type = Column(String, index=True)
    actor = Column(String)
    payload = Column(JSON)
    status = Column(String, default="pending")
    risk_score = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ApprovalRequest(Base):
    __tablename__ = "approval_requests"
    id = Column(Integer, primary_key=True, index=True)
    action_record_id = Column(Integer)
    status = Column(String, default="pending")  # pending, approved, denied
    approvers = Column(JSON)  # list of approver roles
    decisions = Column(JSON, default=[])  # list of decisions
    created_at = Column(DateTime(timezone=True), server_default=func.now())
