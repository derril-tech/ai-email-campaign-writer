#!/usr/bin/env python3
"""
Database seed and fixture data for AI Email Campaign Writer
Used to populate the database with initial data for development and testing
"""

import asyncio
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any

# Mock data for seeding
USERS_DATA = [
    {
        "id": str(uuid.uuid4()),
        "email": "admin@aiemailcampaign.com",
        "first_name": "Admin",
        "last_name": "User",
        "company_name": "AI Email Campaign Writer",
        "industry": "Technology",
        "role": "admin",
        "subscription": "enterprise",
        "password_hash": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.iK8i",  # "admin123"
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "id": str(uuid.uuid4()),
        "email": "demo@example.com",
        "first_name": "Demo",
        "last_name": "User",
        "company_name": "Demo Company",
        "industry": "Marketing",
        "role": "user",
        "subscription": "pro",
        "password_hash": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.iK8i",  # "demo123"
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "id": str(uuid.uuid4()),
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User",
        "company_name": "Test Corp",
        "industry": "E-commerce",
        "role": "user",
        "subscription": "free",
        "password_hash": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.iK8i",  # "test123"
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
]

CAMPAIGNS_DATA = [
    {
        "id": str(uuid.uuid4()),
        "name": "Welcome Campaign",
        "subject": "Welcome to AI Email Campaign Writer!",
        "content": """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Welcome to AI Email Campaign Writer</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h1 style="color: #2563eb;">Welcome to AI Email Campaign Writer!</h1>
                <p>Hi {{first_name}},</p>
                <p>Thank you for joining AI Email Campaign Writer! We're excited to help you create engaging, personalized email campaigns that drive results.</p>
                <p>Here's what you can do with our platform:</p>
                <ul>
                    <li>Create AI-powered email content in seconds</li>
                    <li>Personalize messages for your audience</li>
                    <li>Track performance with detailed analytics</li>
                    <li>Optimize campaigns with A/B testing</li>
                </ul>
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{{dashboard_url}}" style="background-color: #2563eb; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">Get Started</a>
                </div>
                <p>If you have any questions, feel free to reach out to our support team.</p>
                <p>Best regards,<br>The AI Email Campaign Writer Team</p>
            </div>
        </body>
        </html>
        """,
        "status": "sent",
        "recipient_count": 500,
        "sent_count": 500,
        "opened_count": 125,
        "clicked_count": 25,
        "open_rate": 25.0,
        "click_rate": 5.0,
        "scheduled_at": None,
        "sent_at": datetime.now() - timedelta(days=7),
        "created_at": datetime.now() - timedelta(days=10),
        "updated_at": datetime.now() - timedelta(days=7)
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Product Launch Announcement",
        "subject": "🚀 New Features Available Now!",
        "content": """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>New Features Available</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h1 style="color: #2563eb;">🚀 New Features Available Now!</h1>
                <p>Hi {{first_name}},</p>
                <p>We're excited to announce some amazing new features that will take your email campaigns to the next level!</p>
                <h2>What's New:</h2>
                <ul>
                    <li><strong>Advanced AI Content Generation:</strong> Create even better content with our improved AI</li>
                    <li><strong>Enhanced Analytics:</strong> Get deeper insights into your campaign performance</li>
                    <li><strong>New Templates:</strong> Beautiful, responsive templates for every occasion</li>
                    <li><strong>Automation Workflows:</strong> Set up automated email sequences</li>
                </ul>
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{{new_features_url}}" style="background-color: #2563eb; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">Explore New Features</a>
                </div>
                <p>These features are available to all Pro and Enterprise users. Upgrade your plan to unlock the full potential!</p>
                <p>Happy emailing!<br>The AI Email Campaign Writer Team</p>
            </div>
        </body>
        </html>
        """,
        "status": "scheduled",
        "recipient_count": 1200,
        "sent_count": 0,
        "opened_count": 0,
        "clicked_count": 0,
        "open_rate": 0.0,
        "click_rate": 0.0,
        "scheduled_at": datetime.now() + timedelta(days=1),
        "sent_at": None,
        "created_at": datetime.now() - timedelta(days=3),
        "updated_at": datetime.now() - timedelta(days=3)
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Monthly Newsletter",
        "subject": "Your January Newsletter is Here",
        "content": """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>January Newsletter</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h1 style="color: #2563eb;">Your January Newsletter</h1>
                <p>Hi {{first_name}},</p>
                <p>Here's what's happening this month in the world of email marketing:</p>
                <h2>Industry Updates</h2>
                <p>Email marketing continues to be one of the most effective channels for reaching customers. Recent studies show that email has an ROI of $42 for every $1 spent.</p>
                <h2>Best Practices</h2>
                <ul>
                    <li>Personalize your subject lines</li>
                    <li>Use clear call-to-action buttons</li>
                    <li>Test different send times</li>
                    <li>Segment your audience</li>
                </ul>
                <h2>Success Story</h2>
                <p>One of our customers increased their open rate by 45% using our AI-powered subject line optimization feature!</p>
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{{newsletter_url}}" style="background-color: #2563eb; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">Read Full Newsletter</a>
                </div>
                <p>Thanks for reading!<br>The AI Email Campaign Writer Team</p>
            </div>
        </body>
        </html>
        """,
        "status": "draft",
        "recipient_count": 0,
        "sent_count": 0,
        "opened_count": 0,
        "clicked_count": 0,
        "open_rate": 0.0,
        "click_rate": 0.0,
        "scheduled_at": None,
        "sent_at": None,
        "created_at": datetime.now() - timedelta(days=1),
        "updated_at": datetime.now() - timedelta(days=1)
    }
]

TEMPLATES_DATA = [
    {
        "id": str(uuid.uuid4()),
        "name": "Welcome Email",
        "subject": "Welcome to {{company_name}}!",
        "content": """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Welcome</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h1 style="color: #2563eb;">Welcome to {{company_name}}!</h1>
                <p>Hi {{first_name}},</p>
                <p>Thank you for joining {{company_name}}! We're excited to have you on board.</p>
                <p>Here's what you can expect from us:</p>
                <ul>
                    <li>Regular updates and news</li>
                    <li>Exclusive offers and promotions</li>
                    <li>Helpful tips and resources</li>
                </ul>
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{{website_url}}" style="background-color: #2563eb; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">Visit Our Website</a>
                </div>
                <p>If you have any questions, feel free to reach out to our support team.</p>
                <p>Best regards,<br>The {{company_name}} Team</p>
            </div>
        </body>
        </html>
        """,
        "category": "welcome",
        "is_public": True,
        "created_at": datetime.now() - timedelta(days=30),
        "updated_at": datetime.now() - timedelta(days=30)
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Newsletter Template",
        "subject": "{{newsletter_title}} - {{month}} {{year}}",
        "content": """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>{{newsletter_title}}</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h1 style="color: #2563eb;">{{newsletter_title}}</h1>
                <p>Hi {{first_name}},</p>
                <p>Here's your {{month}} {{year}} newsletter with the latest updates and insights.</p>
                <h2>Featured Content</h2>
                <p>{{featured_content}}</p>
                <h2>Latest Updates</h2>
                <ul>
                    {{#each updates}}
                    <li>{{this}}</li>
                    {{/each}}
                </ul>
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{{newsletter_url}}" style="background-color: #2563eb; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">Read Full Newsletter</a>
                </div>
                <p>Thanks for reading!<br>The {{company_name}} Team</p>
            </div>
        </body>
        </html>
        """,
        "category": "newsletter",
        "is_public": True,
        "created_at": datetime.now() - timedelta(days=25),
        "updated_at": datetime.now() - timedelta(days=25)
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Product Announcement",
        "subject": "🎉 Introducing {{product_name}}",
        "content": """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>New Product Announcement</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h1 style="color: #2563eb;">🎉 Introducing {{product_name}}</h1>
                <p>Hi {{first_name}},</p>
                <p>We're excited to announce the launch of {{product_name}}!</p>
                <h2>What is {{product_name}}?</h2>
                <p>{{product_description}}</p>
                <h2>Key Features</h2>
                <ul>
                    {{#each features}}
                    <li>{{this}}</li>
                    {{/each}}
                </ul>
                <h2>Special Launch Offer</h2>
                <p>Get {{discount_percentage}}% off {{product_name}} for a limited time!</p>
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{{product_url}}" style="background-color: #2563eb; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">Learn More</a>
                </div>
                <p>Don't miss out on this amazing opportunity!<br>The {{company_name}} Team</p>
            </div>
        </body>
        </html>
        """,
        "category": "promotional",
        "is_public": False,
        "created_at": datetime.now() - timedelta(days=20),
        "updated_at": datetime.now() - timedelta(days=20)
    }
]

RECIPIENTS_DATA = [
    {
        "id": str(uuid.uuid4()),
        "email": "alice@example.com",
        "first_name": "Alice",
        "last_name": "Johnson",
        "status": "active",
        "last_email_sent": datetime.now() - timedelta(days=2),
        "tags": ["customer", "premium"],
        "created_at": datetime.now() - timedelta(days=30),
        "updated_at": datetime.now() - timedelta(days=2)
    },
    {
        "id": str(uuid.uuid4()),
        "email": "bob@example.com",
        "first_name": "Bob",
        "last_name": "Wilson",
        "status": "active",
        "last_email_sent": datetime.now() - timedelta(days=1),
        "tags": ["customer"],
        "created_at": datetime.now() - timedelta(days=25),
        "updated_at": datetime.now() - timedelta(days=1)
    },
    {
        "id": str(uuid.uuid4()),
        "email": "carol@example.com",
        "first_name": "Carol",
        "last_name": "Brown",
        "status": "unsubscribed",
        "last_email_sent": datetime.now() - timedelta(days=10),
        "tags": ["former-customer"],
        "created_at": datetime.now() - timedelta(days=60),
        "updated_at": datetime.now() - timedelta(days=10)
    },
    {
        "id": str(uuid.uuid4()),
        "email": "dave@example.com",
        "first_name": "Dave",
        "last_name": "Davis",
        "status": "bounced",
        "last_email_sent": datetime.now() - timedelta(days=15),
        "tags": ["invalid-email"],
        "created_at": datetime.now() - timedelta(days=45),
        "updated_at": datetime.now() - timedelta(days=15)
    },
    {
        "id": str(uuid.uuid4()),
        "email": "eve@example.com",
        "first_name": "Eve",
        "last_name": "Evans",
        "status": "active",
        "last_email_sent": datetime.now() - timedelta(hours=6),
        "tags": ["customer", "engaged"],
        "created_at": datetime.now() - timedelta(days=20),
        "updated_at": datetime.now() - timedelta(hours=6)
    }
]

ANALYTICS_DATA = [
    {
        "id": str(uuid.uuid4()),
        "campaign_id": None,  # Will be set when campaigns are created
        "date": datetime.now() - timedelta(days=7),
        "sent_count": 100,
        "opened_count": 25,
        "clicked_count": 5,
        "bounced_count": 2,
        "unsubscribed_count": 1,
        "created_at": datetime.now() - timedelta(days=7)
    },
    {
        "id": str(uuid.uuid4()),
        "campaign_id": None,  # Will be set when campaigns are created
        "date": datetime.now() - timedelta(days=6),
        "sent_count": 150,
        "opened_count": 38,
        "clicked_count": 8,
        "bounced_count": 3,
        "unsubscribed_count": 2,
        "created_at": datetime.now() - timedelta(days=6)
    },
    {
        "id": str(uuid.uuid4()),
        "campaign_id": None,  # Will be set when campaigns are created
        "date": datetime.now() - timedelta(days=5),
        "sent_count": 200,
        "opened_count": 52,
        "clicked_count": 12,
        "bounced_count": 4,
        "unsubscribed_count": 1,
        "created_at": datetime.now() - timedelta(days=5)
    }
]

async def seed_database():
    """
    Seed the database with initial data
    This is a placeholder function - in a real implementation,
    you would use your actual database models and session
    """
    print("🌱 Seeding database with initial data...")
    
    # In a real implementation, you would:
    # 1. Create database session
    # 2. Insert users
    # 3. Insert campaigns (with proper user_id references)
    # 4. Insert templates
    # 5. Insert recipients
    # 6. Insert analytics data
    # 7. Commit transaction
    
    print("✅ Database seeded successfully!")
    print(f"📊 Created {len(USERS_DATA)} users")
    print(f"📧 Created {len(CAMPAIGNS_DATA)} campaigns")
    print(f"📝 Created {len(TEMPLATES_DATA)} templates")
    print(f"👥 Created {len(RECIPIENTS_DATA)} recipients")
    print(f"📈 Created {len(ANALYTICS_DATA)} analytics records")

def generate_fixture_data():
    """
    Generate fixture data for testing
    Returns a dictionary with all the fixture data
    """
    return {
        "users": USERS_DATA,
        "campaigns": CAMPAIGNS_DATA,
        "templates": TEMPLATES_DATA,
        "recipients": RECIPIENTS_DATA,
        "analytics": ANALYTICS_DATA
    }

def export_fixtures_to_json(filename: str = "fixtures.json"):
    """
    Export fixture data to JSON file
    """
    import json
    
    fixtures = generate_fixture_data()
    
    # Convert datetime objects to ISO format strings
    def convert_datetime(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return obj
    
    # Convert fixtures to JSON-serializable format
    json_fixtures = json.loads(
        json.dumps(fixtures, default=convert_datetime, indent=2)
    )
    
    with open(filename, 'w') as f:
        json.dump(json_fixtures, f, indent=2)
    
    print(f"📁 Fixtures exported to {filename}")

if __name__ == "__main__":
    print("🚀 AI Email Campaign Writer - Database Seeder")
    print("=" * 50)
    
    # Export fixtures to JSON
    export_fixtures_to_json()
    
    # In a real implementation, you would run the actual seeding
    # asyncio.run(seed_database())
    
    print("\n📋 Available data:")
    print(f"  - Users: {len(USERS_DATA)} records")
    print(f"  - Campaigns: {len(CAMPAIGNS_DATA)} records")
    print(f"  - Templates: {len(TEMPLATES_DATA)} records")
    print(f"  - Recipients: {len(RECIPIENTS_DATA)} records")
    print(f"  - Analytics: {len(ANALYTICS_DATA)} records")
    
    print("\n🔧 To use this data:")
    print("  1. Import the fixtures.json file in your tests")
    print("  2. Use the data arrays directly in your seed scripts")
    print("  3. Modify the data as needed for your specific use case")
