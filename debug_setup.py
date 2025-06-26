def check_db_setup():
    print("=== DevConnect DB Setup Debug ===")
    
    # Check for different db locations
    db_locations = []
    
    try:
        from extensions import db as ext_db
        db_locations.append("extensions.db")
        print("✓ Found db in extensions.py")
    except ImportError:
        print("✗ No db in extensions.py")
    
    try:
        from models import db as models_db
        db_locations.append("models.db")
        print("✓ Found db in models/__init__.py")
    except ImportError:
        print("✗ No db in models/__init__.py")
    
    try:
        from app import db as app_db
        db_locations.append("app.db")
        print("✓ Found db in app.py")
    except ImportError:
        print("✗ No db in app.py")
    
    print(f"\nTotal db instances found: {len(db_locations)}")
    
    if len(db_locations) > 1:
        print("⚠️  WARNING: Multiple db instances detected!")

if __name__ == '__main__':
    check_db_setup()