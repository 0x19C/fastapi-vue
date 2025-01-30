import asyncio
import os

from tortoise import Tortoise
from src.database.models import Users  # Make sure to import your models here
from passlib.context import CryptContext

async def run():
    # Initialize the database connection
    await Tortoise.init(
        db_url=os.environ.get("DATABASE_URL", "mysql://root@localhost:3306/corpy_test"),
        modules={'models': ['src.database.models']}
    )

    # Generate the schema (create tables if they don't exist)
    await Tortoise.generate_schemas()

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    # Check if the admin user already exists
    admin_exists = await Users.filter(is_admin=True).exists()
    if not admin_exists:
        # Create the admin user
        admin_user = await Users.create(
            username='admin',  # Set the username
            email='admin@ai-model-app.co.jp',  # Set the email
            password=pwd_context.encrypt('YmUyODUyMj'),  # Set a hashed password
            is_admin=True  # Set the user as admin
        )
        print(f"Admin user created: {admin_user.username}")
    else:
        print("Admin user already exists.")

    # Close the database connection
    await Tortoise.close_connections()

if __name__ == '__main__':
    asyncio.run(run())
