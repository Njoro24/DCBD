from app import create_app
from extensions import db
from models.user import User
from models.client import Client
from models.job import Job
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Drop all and recreate
    db.drop_all()
    db.create_all()

    print("🔄 Database reset and tables created.")

    # ---- Seed Users ----
    user1 = User(
        name="Alice Developer",
        email="alice@devconnect.com",
        password_hash=generate_password_hash("password123"),
        role="developer",
        bio="Experienced frontend developer."
    )

    user2 = User(
        name="Bob Client",
        email="bob@devconnect.com",
        password_hash=generate_password_hash("securepass"),
        role="client",
        bio="Startup founder looking for tech talent."
    )

    db.session.add_all([user1, user2])
    db.session.commit()
    print("✅ Users seeded.")

    # ---- Seed Clients ----
    client1 = Client(name="TechCorp", email="client@techcorp.com")
    db.session.add(client1)
    db.session.commit()
    print(f"✅ Client seeded with ID: {client1.id}")

    # ---- Seed Jobs ----
    job1 = Job(
        client_id=client1.id,
        title="Full Stack Web Developer",
        description="Build a MERN stack dashboard.",
        requirements="MongoDB, Express, React, Node.js",
        budget=1200,
        is_featured=True,
        status="open"
    )

    job2 = Job(
        client_id=client1.id,
        title="Mobile App Developer",
        description="Develop a cross-platform app using Flutter.",
        requirements="Flutter, Firebase, Dart",
        budget=800,
        is_featured=False,
        status="in_progress"
    )

    db.session.add_all([job1, job2])
    db.session.commit()
    print("✅ Jobs seeded.")
