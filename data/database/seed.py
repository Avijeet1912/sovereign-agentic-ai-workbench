"""
Seed script for Phase 2 - Populate SQLite database with synthetic industrial data.

All data in this file is FAKE/SYNTHETIC and is designed only for demonstration
purposes for the SIH MVP. It does not contain any real MRPL information.
"""

from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import SQLAlchemyError

# Database path
DATABASE_PATH = "data/database/sih_mvp.db"

# Create engine and session
engine = create_engine(
    f"sqlite:///{DATABASE_PATH}",
    connect_args={"check_same_thread": False},
)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine, autoflush=False)


class Equipment(Base):
    """Industrial equipment table."""
    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    type = Column(String, nullable=False)
    location = Column(String, nullable=False)
    status = Column(String, nullable=False, default="operational")
    criticality = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Equipment(id={self.id}, name='{self.name}')>"


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

    def __repr__(self):
        return f"<MaintenanceEvent(id={self.id}, equipment_id={self.equipment_id})>"


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

    def __repr__(self):
        return f"<ProductionRecord(id={self.id}, equipment_id={self.equipment_id}, date='{self.date}')>"


class Employee(Base):
    """Employees table for tracking maintenance personnel."""
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    role = Column(String, nullable=False)
    department = Column(String, nullable=False)

    def __repr__(self):
        return f"<Employee(id={self.id}, name='{self.name}', role='{self.role}')>"


def seed_database():
    """Seed the database with synthetic industrial data."""
    try:
        Base.metadata.create_all(bind=engine)

        # Clear existing data (safe for re-seeding)
        session = SessionLocal()
        session.query(ProductionRecord).delete()
        session.query(MaintenanceEvent).delete()
        session.query(Equipment).delete()
        session.query(Employee).delete()
        session.commit()

        # Create equipment
        equipment = [
            Equipment(name="Pump 1", type="Centrifugal Pump", location="Unit 1 - Crude Processing", status="operational", criticality=3),
            Equipment(name="Pump 2", type="Centrifugal Pump", location="Unit 1 - Crude Processing", status="operational", criticality=3),
            Equipment(name="Pump 3", type="Centrifugal Pump", location="Unit 2 - Hydrotreating", status="operational", criticality=4),
            Equipment(name="Pump 4", type="Centrifugal Pump", location="Unit 2 - Hydrotreating", status="degraded", criticality=5),
            Equipment(name="Compressor 1", type="Rotary Screw Compressor", location="Unit 3 - Utilities", status="operational", criticality=4),
            Equipment(name="Reactor 1", type="Fixed Bed Reactor", location="Unit 2 - Hydrotreating", status="operational", criticality=5),
        ]
        session.add_all(equipment)
        session.flush()

        # Create employees
        employees = [
            Employee(name="Ravi Kumar", role="Maintenance Engineer", department="Engineering"),
            Employee(name="Priya Sharma", role="Maintenance Technician", department="Maintenance"),
            Employee(name="Arjun Nair", role="Shift Supervisor", department="Operations"),
            Employee(name="Sunita Devi", role="Process Engineer", department="Engineering"),
            Employee(name="Vikram Patel", role="Safety Officer", department="Safety"),
            Employee(name="Deepika Rao", role="Production Analyst", department="Production"),
        ]
        session.add_all(employees)
        session.commit()

        # Pump 4 maintenance events - the key demo data for repeated shutdowns
        pump4_maintenance = [
            (datetime(2026, 3, 3, 8, 0), "High vibration detected on discharge bearing", "Bearing replaced with high-temperature variant", 2.5, "Priya Sharma"),
            (datetime(2026, 3, 12, 14, 30), "Seal failure - hydraulic fluid leak", "Seal kit replaced, system pressure rechecked", 4.0, "Ravi Kumar"),
            (datetime(2026, 3, 20, 10, 15), "Motor winding insulation resistance below threshold", "Motor rewound and re-insulated", 6.5, "Ravi Kumar"),
            (datetime(2026, 3, 27, 16, 0), "Impeller erosion due to cavitation", "Impeller replaced, suction filter cleaned", 3.0, "Priya Sharma"),
        ]
        for date, issue, action, downtime, tech in pump4_maintenance:
            session.add(MaintenanceEvent(equipment_id=4, date=date, issue=issue, action_taken=action, downtime_hours=downtime, technician=tech))

        # Maintenance events for other equipment
        other_maintenance = [
            (1, datetime(2026, 2, 10, 9, 0), "Minor seal leakage", "Seal tightened", 1.0, "Ravi Kumar"),
            (1, datetime(2026, 3, 15, 11, 0), "Routine bearing inspection", "No action required", 0.5, "Priya Sharma"),
            (2, datetime(2026, 2, 20, 13, 0), "Pump performance below expected", "Impeller cleaned", 2.0, "Ravi Kumar"),
            (2, datetime(2026, 3, 22, 15, 30), "Coupling alignment check", "Alignment corrected", 1.5, "Priya Sharma"),
            (3, datetime(2026, 2, 28, 10, 0), "Flow rate variation", "Valve calibration performed", 1.0, "Arjun Nair"),
            (3, datetime(2026, 3, 18, 8, 30), "Pressure fluctuation", "Control valve adjusted", 2.0, "Arjun Nair"),
            (5, datetime(2026, 3, 5, 9, 0), "Oil level below minimum", "Oil topped up", 0.5, "Arjun Nair"),
            (5, datetime(2026, 3, 25, 14, 0), "Vibration trending slightly high", "Scheduled inspection", 1.0, "Ravi Kumar"),
            (6, datetime(2026, 2, 15, 10, 0), "Catalyst bed temperature reading", "Sensor recalibrated", 2.0, "Sunita Devi"),
            (6, datetime(2026, 3, 12, 9, 0), "Routine reactor inspection", "No action required", 1.0, "Sunita Devi"),
        ]
        for equipment_id, date, issue, action, downtime, tech in other_maintenance:
            session.add(MaintenanceEvent(equipment_id=equipment_id, date=date, issue=issue, action_taken=action, downtime_hours=downtime, technician=tech))

        # Production records for March 2026 - including Pump 4 impact
        production_records = [
            # Pump 4 - March 2026 (repeated shutdowns)
            ProductionRecord(equipment_id=4, date=datetime(2026, 3, 1), unit="Unit 2 - Hydrotreating", production_amount=420.0, downtime_hours=0.0, reason="Normal operation"),
            ProductionRecord(equipment_id=4, date=datetime(2026, 3, 3), unit="Unit 2 - Hydrotreating", production_amount=380.0, downtime_hours=2.5, reason="Bearing replacement"),
            ProductionRecord(equipment_id=4, date=datetime(2026, 3, 12), unit="Unit 2 - Hydrotreating", production_amount=350.0, downtime_hours=4.0, reason="Seal failure - hydraulic leak"),
            ProductionRecord(equipment_id=4, date=datetime(2026, 3, 20), unit="Unit 2 - Hydrotreating", production_amount=300.0, downtime_hours=6.5, reason="Motor winding insulation failure"),
            ProductionRecord(equipment_id=4, date=datetime(2026, 3, 27), unit="Unit 2 - Hydrotreating", production_amount=375.0, downtime_hours=3.0, reason="Impeller erosion - cavitation"),
            # Pump 4 - February 2026 (baseline)
            ProductionRecord(equipment_id=4, date=datetime(2026, 2, 5), unit="Unit 2 - Hydrotreating", production_amount=450.0, downtime_hours=0.0, reason="Normal operation"),
            ProductionRecord(equipment_id=4, date=datetime(2026, 2, 12), unit="Unit 2 - Hydrotreating", production_amount=440.0, downtime_hours=0.0, reason="Normal operation"),
            ProductionRecord(equipment_id=4, date=datetime(2026, 2, 19), unit="Unit 2 - Hydrotreating", production_amount=445.0, downtime_hours=0.0, reason="Normal operation"),
            ProductionRecord(equipment_id=4, date=datetime(2026, 2, 26), unit="Unit 2 - Hydrotreating", production_amount=448.0, downtime_hours=0.0, reason="Normal operation"),
            # Pump 1 - February/March 2026
            ProductionRecord(equipment_id=1, date=datetime(2026, 2, 8), unit="Unit 1 - Crude Processing", production_amount=500.0, downtime_hours=1.0, reason="Minor seal leakage"),
            ProductionRecord(equipment_id=1, date=datetime(2026, 3, 15), unit="Unit 1 - Crude Processing", production_amount=510.0, downtime_hours=0.5, reason="Routine bearing inspection"),
            # Pump 2 - February/March 2026
            ProductionRecord(equipment_id=2, date=datetime(2026, 2, 20), unit="Unit 1 - Crude Processing", production_amount=480.0, downtime_hours=2.0, reason="Impeller cleaning"),
            ProductionRecord(equipment_id=2, date=datetime(2026, 3, 22), unit="Unit 1 - Crude Processing", production_amount=490.0, downtime_hours=1.5, reason="Coupling alignment check"),
            # Pump 3 - February/March 2026
            ProductionRecord(equipment_id=3, date=datetime(2026, 2, 28), unit="Unit 2 - Hydrotreating", production_amount=430.0, downtime_hours=1.0, reason="Valve calibration"),
            ProductionRecord(equipment_id=3, date=datetime(2026, 3, 18), unit="Unit 2 - Hydrotreating", production_amount=425.0, downtime_hours=2.0, reason="Control valve adjustment"),
            # Compressor 1 - February/March 2026
            ProductionRecord(equipment_id=5, date=datetime(2026, 2, 12), unit="Unit 3 - Utilities", production_amount=600.0, downtime_hours=0.0, reason="Normal operation"),
            ProductionRecord(equipment_id=5, date=datetime(2026, 3, 5), unit="Unit 3 - Utilities", production_amount=590.0, downtime_hours=0.5, reason="Oil level check"),
            ProductionRecord(equipment_id=5, date=datetime(2026, 3, 25), unit="Unit 3 - Utilities", production_amount=585.0, downtime_hours=1.0, reason="Vibration trending"),
            # Reactor 1 - February/March 2026
            ProductionRecord(equipment_id=6, date=datetime(2026, 2, 15), unit="Unit 2 - Hydrotreating", production_amount=380.0, downtime_hours=2.0, reason="Sensor recalibration"),
            ProductionRecord(equipment_id=6, date=datetime(2026, 3, 12), unit="Unit 2 - Hydrotreating", production_amount=375.0, downtime_hours=1.0, reason="Routine reactor inspection"),
        ]
        session.add_all(production_records)
        session.commit()

        print(f"✓ Database seeded successfully: {DATABASE_PATH}")
        print(f"✓ Equipment: {len(equipment)} records")
        print(f"✓ Employees: {len(employees)} records")
        print(f"✓ Maintenance events: {len(pump4_maintenance) + len(other_maintenance)} records")
        print(f"✓ Production records: {len(production_records)} records")
        return True

    except SQLAlchemyError as e:
        print(f"✗ Error seeding database: {e}")
        return False


if __name__ == "__main__":
    seed_database()
