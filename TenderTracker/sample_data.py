"""
Sample data generation script for TenderTide.
Run this after setting up the database to populate it with test data.
"""
import os
import django
from datetime import datetime, timedelta
from django.utils import timezone

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tendertide.settings')
django.setup()

from accounts.models import CustomUser
from tenders.models import Tender

def create_sample_data():
    # Create sample users
    admin_user = CustomUser.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123',
        account_type='admin'
    )

    company_user = CustomUser.objects.create_user(
        username='techcompany',
        email='company@example.com',
        password='company123',
        account_type='company',
        company_name='Tech Solutions Ltd'
    )

    individual_user = CustomUser.objects.create_user(
        username='john_doe',
        email='john@example.com',
        password='user123',
        account_type='user'
    )

    # Create sample tenders
    sample_tenders = [
        {
            'title': 'IT Infrastructure Upgrade',
            'description': 'Complete overhaul of corporate IT infrastructure including servers and networking equipment.',
            'type': 'private',
            'category': 'it',
            'deadline': timezone.now() + timedelta(days=30),
            'value': 500000.00,
            'location': 'New York',
            'requirements': 'ISO 27001 Certification\nMinimum 5 years experience\nProven track record',
            'author': company_user
        },
        {
            'title': 'Healthcare Equipment Supply',
            'description': 'Supply of medical equipment for new hospital wing.',
            'type': 'government',
            'category': 'healthcare',
            'deadline': timezone.now() + timedelta(days=45),
            'value': 1000000.00,
            'location': 'Chicago',
            'requirements': 'FDA Approved\nCE Marking\nISO 13485 Certification',
            'author': company_user
        },
        {
            'title': 'Smart City Project',
            'description': 'Implementation of smart city solutions including IoT sensors and data analytics platform.',
            'type': 'government',
            'category': 'infrastructure',
            'deadline': timezone.now() + timedelta(days=60),
            'value': 2000000.00,
            'location': 'San Francisco',
            'requirements': 'Experience with IoT\nBig Data Analytics\nSmart City Projects',
            'author': company_user
        }
    ]

    for tender_data in sample_tenders:
        tender = Tender.objects.create(**tender_data)
        # Add some favorites for the individual user
        if tender.id % 2 == 0:
            individual_user.favorite_tenders.add(tender)

    print("Sample data created successfully!")
    print("\nLogin credentials:")
    print("Admin - email: admin@example.com, password: admin123")
    print("Company - email: company@example.com, password: company123")
    print("User - email: john@example.com, password: user123")

if __name__ == '__main__':
    create_sample_data()
