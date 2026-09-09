"""
Database module for SIH MVP Phase 2 - SQLite setup with synthetic industrial data.

This module sets up SQLAlchemy connection to SQLite and provides
functions for database initialization, table creation, and data management.
"""

import os
from datetime import datetime
from typing import Dict, Any, List, Optional

from sqlalchemy import (
    create_engine, Column, Integer, String, Float, DateTime, ForeignKey,
    text, select, update, delete, inspect, MetaData, Table, engine,
    text as sql_text
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
from dotenv import load_dotenv

load_dotenv()

# Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///data/database/sih_mvp.db")

# Create engine with optimizations for file-based SQLite
def get_engine():
    return create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=False,  # Set to True for debugging
        pool_pre_ping=True,
    )

# Initialize SQLAlchemy components
engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Table definitions
class Equipment(Base):
    """Industrial equipment table."""
    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    type = Column(String, nullable=False)
    location = Column(String, nullable=False)
    status = Column(String, nullable=False, default="operational")
    criticality = Column(Integer, nullable=False)  # 1-5 scale
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    maintenance_events = relationship("MaintenanceEvent", back_populates="equipment")
    production_records = relationship("ProductionRecord", back_populates="equipment")

    def __repr__(self):
        return f"<Equipment(id={self.id}, name='{self.name}', type='{self.type}', status='{self.status}')>"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses."""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "location": self.location,
            "status": self.status,
            "criticality": self.criticality,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class MaintenanceEvent(Base):
    """Equipment maintenance events table."""
    __tablename__ = "maintenance_events"

    id = Column(Integer, primary_key=True, index=True)
    equipment_id = Column(Integer, ForeignKey("equipment.id"), nullable=False, index=True)
    date = Column(DateTime, nullable=False, index=True)
    issue = Column(String, nullable=False)
    action_taken = Column(String, nullable=False)
    downtime_hours = Column(Float, nullable=False)
    technician = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    equipment = relationship("Equipment", back_populates="maintenance_events")

    def __repr__(self):
        return f"<MaintenanceEvent(id={self.id}, equipment_id={self.equipment_id}, date='{self.date}')>"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses."""
        return {
            "id": self.id,
            "equipment_id": self.equipment_id,
            "date": self.date,
            "issue": self.issue,
            "action_taken": self.action_taken,
            "downtime_hours": self.downtime_hours,
            "technician": self.technician,
            "created_at": self.created_at,
        }


class ProductionRecord(Base):
    """Production records table."""
    __tablename__ = "production_records"

    id = Column(Integer, primary_key=True, index=True)
    equipment_id = Column(Integer, ForeignKey("equipment.id"), nullable=False, index=True)
    date = Column(DateTime, nullable=False, index=True)
    unit = Column(String, nullable=False)
    production_amount = Column(Float, nullable=False)
    downtime_hours = Column(Float, default=0.0)
    reason = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    equipment = relationship("Equipment", back_populates="production_records")

    def __repr__(self):
        return f"<ProductionRecord(id={self.id}, equipment_id={self.equipment_id}, date='{self.date}', amount={self.production_amount})>"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses."""
        return {
            "id": self.id,
            "equipment_id": self.equipment_id,
            "date": self.date,
            "unit": self.unit,
            "production_amount": self.production_amount,
            "downtime_hours": self.downtime_hours,
            "reason": self.reason,
            "created_at": self.created_at,
        }


class Employee(Base):
    """Employees table for tracking maintenance personnel."""
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    role = Column(String, nullable=False)
    department = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Employee(id={self.id}, name='{self.name}', role='{self.role}')>"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses."""
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "department": self.department,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


def init_database():
    """Initialize database by creating all tables."""
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print(f"✓ Database initialized at {DATABASE_URL}")
        print(f"✓ Tables created: {', '.join(Base.metadata.tables.keys())}")
        return True
    except SQLAlchemyError as e:
        print(f"✗ Error initializing database: {e}")
        return False


@contextmanager
def get_db_session():
    """Context manager for database sessions."""
    session = SessionLocal()
    try:
        yield session
    except SQLAlchemyError as e:
        session.rollback()
        raise e
    finally:
        session.close()


# Database functions for CRUD operations
def get_all_equipment() -> List[Equipment]:
    """Get all equipment records."""
    with get_db_session() as session:
        return session.query(Equipment).all()


def get_equipment_by_id(equipment_id: int) -> Optional[Equipment]:
    """Get equipment by ID."""
    with get_db_session() as session:
        return session.query(Equipment).filter(Equipment.id == equipment_id).first()


def get_maintenance_events_by_equipment(equipment_id: int) -> List[MaintenanceEvent]:
    """Get all maintenance events for a specific equipment."""
    with get_db_session() as session:
        return session.query(MaintenanceEvent).filter(
            MaintenanceEvent.equipment_id == equipment_id
        ).order_by(MaintenanceEvent.date.desc()).all()


def get_production_records_by_equipment(equipment_id: int) -> List[ProductionRecord]:
    """Get all production records for a specific equipment."""
    with get_db_session() as session:
        return session.query(ProductionRecord).filter(
            ProductionRecord.equipment_id == equipment_id
        ).order_by(ProductionRecord.date.desc()).all()


def execute_safe_query(query: str, params: Optional[Dict] = None) -> Any:
    """
    Execute a safe read-only SQL query.

    Rejects destructive operations: INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE, CREATE.
    Only allows SELECT queries for data retrieval.
    """
    # Check for destructive operations
    destructive_ops = [
        "INSERT", "UPDATE", "DELETE", "DROP", "ALTER",
        "TRUNCATE", "CREATE", "RENAME", "ATTACH", "DETACH",
        "PRAGMA", "VACUUM", "COMPACT", "CALL", "EXECUTE",
    ]

    normalized_query = query.strip().upper()
    if any(op in normalized_query for op in destructive_ops):
        raise ValueError(f"Destructive SQL operation not allowed: {query}")

    # Additional safety check for patterns
    if "=" in query and "SELECT" not in normalized_query:
        # Allow WHERE clauses with SELECT
        if normalized_query.startswith("SELECT") and " WHERE " in normalized_query:
            pass
        elif normalized_query.startswith("SELECT") and " WHERE " not in normalized_query:
            pass
        else:
            raise ValueError(f"Unsafe SQL pattern detected: {query}")

    with get_db_session() as session:
        result = session.execute(sql_text(query), params or {})
        return result.fetchall()


def get_table_count(table_name: str) -> int:
    """Get the number of rows in a table."""
    with get_db_session() as session:
        inspector = inspect(session.bind)
        return inspector.get_table_count(table_name) if inspector.has_table(table_name) else 0


def get_all_tables() -> List[str]:
    """Get list of all table names."""
    with get_db_session() as session:
        inspector = inspect(session.bind)
        return inspector.get_table_names()