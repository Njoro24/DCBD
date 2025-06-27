#!/usr/bin/env python3
"""
Enhanced Flask Database Setup Checker
This script will help diagnose and fix database setup issues
"""
import os
import sys

def check_file_exists(filepath):
    """Check if file exists and return its status"""
    if os.path.exists(filepath):
        return True, os.path.getsize(filepath)
    return False, 0

def read_file_content(filepath):
    """Safely read file content"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"

def analyze_python_file(filepath, filename):
    """Analyze a Python file for database-related imports and objects"""
    print(f"\n=== Analyzing {filename} ===")
    
    exists, size = check_file_exists(filepath)
    if not exists:
        print(f"❌ {filename} does not exist")
        return
    
    if size == 0:
        print(f"⚠️  {filename} is empty ({size} bytes)")
        return
    
    print(f"✅ {filename} exists ({size} bytes)")
    
    content = read_file_content(filepath)
    if content.startswith("Error"):
        print(f"❌ {content}")
        return
    
    # Check for various database-related patterns
    patterns = {
        'SQLAlchemy import': ['from flask_sqlalchemy import', 'import flask_sqlalchemy'],
        'db object creation': ['SQLAlchemy()', 'db = SQLAlchemy'],
        'db import': ['from . import db', 'from app import db', 'import db'],
        'db usage': ['db.Model', 'db.Column', 'db.create_all', 'db.session'],
        'Flask app': ['Flask(__name__)', 'app = Flask'],
        'app initialization': ['app.config', 'app.init_app'],
    }
    
    found_patterns = {}
    for pattern_name, searches in patterns.items():
        found = []
        for search in searches:
            if search in content:
                # Find line numbers
                lines = content.split('\n')
                for i, line in enumerate(lines, 1):
                    if search in line:
                        found.append(f"Line {i}: {line.strip()}")
        if found:
            found_patterns[pattern_name] = found
    
    if found_patterns:
        print("🔍 Found database-related code:")
        for pattern, occurrences in found_patterns.items():
            print(f"  • {pattern}:")
            for occurrence in occurrences[:3]:  # Limit to first 3 occurrences
                print(f"    {occurrence}")
    else:
        print("❌ No database-related code found")
    
    # Show first few non-empty lines for context
    lines = [line for line in content.split('\n') if line.strip()]
    if lines:
        print("📝 File preview (first 5 non-empty lines):")
        for i, line in enumerate(lines[:5], 1):
            print(f"  {i}: {line}")

def suggest_fixes():
    """Provide suggestions for common database setup issues"""
    print("\n" + "="*50)
    print("🔧 COMMON FIXES FOR DATABASE SETUP")
    print("="*50)
    
    print("\n1. Basic Flask-SQLAlchemy Setup:")
    print("   In your main app.py or __init__.py:")
    print("   ```python")
    print("   from flask import Flask")
    print("   from flask_sqlalchemy import SQLAlchemy")
    print("   ")
    print("   app = Flask(__name__)")
    print("   app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_db.db'")
    print("   db = SQLAlchemy(app)")
    print("   ```")
    
    print("\n2. If using Application Factory Pattern:")
    print("   In extensions.py:")
    print("   ```python")
    print("   from flask_sqlalchemy import SQLAlchemy")
    print("   db = SQLAlchemy()")
    print("   ```")
    print("   ")
    print("   In __init__.py or app.py:")
    print("   ```python")
    print("   from extensions import db")
    print("   ")
    print("   def create_app():")
    print("       app = Flask(__name__)")
    print("       db.init_app(app)")
    print("       return app")
    print("   ```")
    
    print("\n3. In models/__init__.py:")
    print("   ```python")
    print("   from extensions import db  # or from app import db")
    print("   ```")

def main():
    print("=== Enhanced DevConnect DB Setup Debug ===")
    
    # Get current directory
    current_dir = os.getcwd()
    print(f"📁 Current directory: {current_dir}")
    
    # List all Python files in current directory
    python_files = [f for f in os.listdir('.') if f.endswith('.py')]
    print(f"🐍 Python files found: {python_files}")
    
    # Check key files
    key_files = [
        ('app.py', 'Main application file'),
        ('__init__.py', 'Package initialization'),
        ('extensions.py', 'Extensions file'),
        ('models/__init__.py', 'Models package init'),
        ('models.py', 'Models file'),
        ('config.py', 'Configuration file'),
    ]
    
    for filename, description in key_files:
        analyze_python_file(filename, f"{filename} ({description})")
    
    # Check for models directory
    if os.path.isdir('models'):
        print(f"\n📁 Models directory contents: {os.listdir('models')}")
        model_files = [f for f in os.listdir('models') if f.endswith('.py')]
        for model_file in model_files:
            if model_file != '__init__.py':
                analyze_python_file(f'models/{model_file}', f"models/{model_file}")
    
    suggest_fixes()
    
    print(f"\n{'='*50}")
    print("🎯 NEXT STEPS:")
    print("1. Check the analysis above for missing db imports/objects")
    print("2. Implement the suggested fixes based on your app structure")
    print("3. Run this script again to verify the fixes")
    print("4. Create your database tables with db.create_all()")

if __name__ == "__main__":
    main()