# Import create_app and db from the main application module.
from app import create_app, db
# Import your database models.
from models.user import User
from models.job import Job

# Create a Flask application instance using the factory function.
# This is crucial because database operations (like db.drop_all(), db.create_all())
# require an active Flask application context.
app = create_app()

# Use app.app_context() to push an application context.
# All operations within this 'with' block will have access to the app's configuration
# and extensions (like 'db').
with app.app_context():
    # -----------------------------------------------------------
    # Database Initialization and Seeding Process
    # -----------------------------------------------------------

    print("--- Starting Database Seeding ---")

    # 1. Drop all existing database tables.
    #    This is useful for development and ensures a clean slate before reseeding.
    #    USE WITH EXTREME CAUTION IN PRODUCTION ENVIRONMENTS, as it deletes all data!
    print("Dropping all existing database tables (if any)...")
    db.drop_all()
    print("Tables dropped.")

    # 2. Create all database tables defined in your models.
    #    SQLAlchemy discovers all db.Model subclasses that have been imported
    #    (like User and Job models via `import models.user` and `import models.job` in `app.py`).
    print("Creating all database tables based on models...")
    db.create_all()
    print("Tables created.")

    # -----------------------------------------------------------
    # 3. Create Sample User (Client) Data
    #    We create sample 'client' users who will post jobs.
    # -----------------------------------------------------------
    print("Adding sample users...")
    # IMPORTANT: In a real application, passwords should ALWAYS be securely hashed
    # using a library like Werkzeug.security (e.g., generate_password_hash)
    # BEFORE storing them in the database. 'secret' is for demonstration only.
    alice = User(name="Alice Tech Solutions", email="alice@example.com", password_hash="hashed_password_alice", role="client", bio="A leading tech company specializing in AI solutions.")
    bob = User(name="Bob's Creative Studio", email="bob@example.com", password_hash="hashed_password_bob", role="client", bio="Innovative design and development agency.")
    charlie = User(name="Charlie Developer", email="charlie@example.com", password_hash="hashed_password_charlie", role="developer", bio="Experienced Python and JavaScript full-stack developer looking for new challenges.")

    # Add the user objects to the database session.
    db.session.add_all([alice, bob, charlie])
    # Commit the changes to the database. This assigns IDs to the new users.
    db.session.commit()
    print("Sample users added and committed.")

    # -----------------------------------------------------------
    # 4. Create Sample Job Data
    #    Jobs are linked to clients using their 'client_id' (foreign key).
    # -----------------------------------------------------------
    print("Adding sample jobs...")
    job1 = Job(title="Senior React Developer for Fintech",
               description="Seeking an experienced React Developer with 5+ years in fintech to build high-performance user interfaces. Experience with Redux/Zustand, TypeScript, and REST APIs is a must.",
               budget=120000.00, # Using a larger number for demonstration of budget
               client_id=alice.id,
               status='open')
    job2 = Job(title="Lead Flask Backend Engineer",
               description="Looking for a lead Python Flask developer to design and implement scalable RESTful APIs. Must have strong experience with SQLAlchemy, microservices, and cloud deployments (AWS/Azure).",
               budget=150000.00,
               client_id=bob.id,
               status='open')
    job3 = Job(title="Full Stack Engineer (React & Node.js)",
               description="Opportunity for a versatile Full Stack Engineer to work on a greenfield SaaS product. Strong skills in React, Node.js (Express), PostgreSQL, and unit testing are highly valued.",
               budget=200000.00,
               client_id=alice.id,
               status='open')
    job4 = Job(title="Mobile App Developer (Flutter/Dart)",
               description="Develop cross-platform mobile applications for iOS and Android using Flutter. Experience with integrating third-party APIs, UI/UX best practices, and push notifications.",
               budget=95000.00,
               client_id=bob.id,
               status='open')
    job5 = Job(title="Cybersecurity Analyst",
               description="Join our security team to identify, assess, and mitigate cybersecurity risks. Experience with penetration testing, vulnerability assessments, and incident response.",
               budget=110000.00,
               client_id=alice.id,
               status='closed') # Example of a closed job

    # Add the job objects to the database session.
    db.session.add_all([job1, job2, job3, job4, job5])
    # Commit the changes to the database.
    db.session.commit()
    print("Sample jobs added and committed.")

    print("\n✅ Database seeded successfully!")
    print("You can now run 'python app.py' to start the server.")

# To run this seed script from your terminal:
# Ensure you are in the 'DCBD' directory.
# Activate your virtual environment first (if using one).
# python seed.py
