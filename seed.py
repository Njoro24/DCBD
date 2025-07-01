from app import create_app
from extensions import db
from models.user import User
from models.client import Client
from models.job import Job, JobStatus
from models.skill import Skill
from models.application import Application, ApplicationStatus
from datetime import datetime

app = create_app()

with app.app_context():
    # Reset the database
    db.drop_all()
    db.create_all()
    print("Database reset and tables created.")

    # ---- Seed Users ----
    user1 = User(
        name="Alice Developer",
        email="alice@devconnect.com",
        role="Developer",
        bio="Experienced frontend developer."
    )
    user1.set_password("password123")

    user2 = User(
        name="Bob Client",
        email="bob@devconnect.com",
        role="Client",
        bio="Startup founder looking for tech talent."
    )
    user2.set_password("securepass")

    db.session.add_all([user1, user2])
    db.session.commit()
    print("Users seeded.")

    # ---- Seed Client Company ----
    client1 = Client(name="TechCorp", email="client@techcorp.com")
    db.session.add(client1)
    db.session.commit()
    print(f"Client seeded with ID: {client1.id}")

    # ---- Seed Jobs ----
    job1 = Job(
        client_id=user2.id,
        title="Full Stack Web Developer",
        description="Build a MERN stack dashboard.",
        requirements="MongoDB, Express, React, Node.js",
        salary_min=1000,
        salary_max=1500,
        location="Remote",
        job_type="Contract",
        status=JobStatus.OPEN,
        is_featured=True
    )

    job2 = Job(
        client_id=user2.id,
        title="Mobile App Developer",
        description="Develop a cross-platform app using Flutter.",
        requirements="Flutter, Firebase, Dart",
        salary_min=800,
        salary_max=1000,
        location="Nairobi",
        job_type="Full-time",
        status=JobStatus.OPEN,
        is_featured=False
    )

    db.session.add_all([job1, job2])
    db.session.commit()
    print("Jobs seeded.")

    # ---- Seed Skills ----
    skill1 = Skill(name="React")
    skill2 = Skill(name="JavaScript")
    skill3 = Skill(name="UI/UX Design")

    user1.skills.extend([skill1, skill2, skill3])
    db.session.add_all([skill1, skill2, skill3])
    db.session.commit()
    print("Skills seeded and linked to developer.")

    # ---- Seed Application ----
    application1 = Application(
        job_id=job1.id,
        applicant_id=user1.id,
        cover_letter="I have 5 years of experience with the MERN stack.",
        status=ApplicationStatus.PENDING,
        created_at=datetime.utcnow()
    )

    db.session.add(application1)
    db.session.commit()
    print("Application seeded.")
