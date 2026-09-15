from app.core.security import hash_password
from app.db.session import create_db_and_tables, engine
from app.models import Service, User
from sqlmodel import Session, select


def seed() -> None:
    create_db_and_tables()
    with Session(engine) as session:
        if not session.exec(select(User).where(User.email == "qa.user@example.com")).first():
            session.add(
                User(
                    email="qa.user@example.com",
                    full_name="QA Portfolio User",
                    department="Quality Engineering",
                    password_hash=hash_password("Password123!"),
                )
            )
        existing_services = {service.name for service in session.exec(select(Service)).all()}
        for service in [
            Service(
                name="Building Access Badge",
                category="Access",
                description="Request or replace office entry badge.",
            ),
            Service(
                name="VPN Access",
                category="IT",
                description="Request secure remote access for internal systems.",
            ),
            Service(
                name="Laptop Repair",
                category="IT",
                description="Report hardware issues for company laptops.",
            ),
            Service(
                name="Payroll Question",
                category="HR",
                description="Ask payroll or benefits support for assistance.",
            ),
        ]:
            if service.name not in existing_services:
                session.add(service)
        session.commit()


if __name__ == "__main__":
    seed()
