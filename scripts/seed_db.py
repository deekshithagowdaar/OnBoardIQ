import sys
import os

# Add backend directory to path
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend'))
sys.path.insert(0, backend_dir)

from app.seed_data import init_db, seed_demo_data

if __name__ == "__main__":
    print("Initializing OnboardIQ database schema...")
    init_db()
    print("Seeding realistic multi-department demo data and historical outcomes...")
    seed_demo_data()
    print("Database seeding completed successfully!")
