### **Steps to Handle Migrations with Tortoise-ORM**

#### **1. Install Required Packages**
Install Tortoise-ORM and Aerich:
```bash
pip install tortoise-orm aerich
```

---

#### **2. Configure Tortoise-ORM**
Set up your database configuration and connect it with Tortoise-ORM. For example:

**`src/database/config.py`**
```python
TORTOISE_ORM = {
    "connections": {
        "default": "sqlite://db.sqlite3"  # Replace with your database URL
    },
    "apps": {
        "models": {
            "models": ["src.models", "aerich.models"],  # Include your models and Aerich
            "default_connection": "default",
        },
    },
}
```

---

#### **3. Define Your Models**
Create your models in a file such as `src/database/models.py`:

**`src/database/models.py`**
```python
from tortoise import fields
from tortoise.models import Model

class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    email = fields.CharField(max_length=100, unique=True)
    hashed_password = fields.CharField(max_length=255)
```

---

#### **4. Initialize Aerich**
Aerich is the migration tool for Tortoise-ORM. Initialize it in your project:

1. Run the following command to initialize Aerich in your project:
   ```bash
   aerich init -t src.database.config.TORTOISE_ORM
   ```
   This will create an `aerich.ini` file and a `migrations/` directory.

2. Configure Aerich's `ini` file (`aerich.ini`):
   ```ini
   [aerich]
   tortoise_orm = src.database.config.TORTOISE_ORM
   location = ./migrations
   ```

---

#### **5. Create the First Migration**
After defining your models, generate the migration file:
```bash
aerich init-db
```

This command does two things:
- Creates the initial migration file for your models.
- Applies the migration to your database.

---

#### **6. Apply Subsequent Migrations**
If you make changes to your models later, follow these steps:

1. Detect changes and create a new migration file:
   ```bash
   aerich migrate
   ```

2. Apply the migration to the database:
   ```bash
   aerich upgrade
   ```

---

#### **7. Example Workflow**
- Define or update models in `src/database/models.py`.
- Run `aerich migrate` to generate a migration file.
- Run `aerich upgrade` to apply the migration.

---

#### **8. Using Migrations in Production**
Ensure the `aerich` commands are part of your deployment process to keep the database schema in sync.

---

### **Common Aerich Commands**
| Command             | Description                                |
|---------------------|--------------------------------------------|
| `aerich init`       | Initialize Aerich for the project          |
| `aerich init-db`    | Create the first migration and apply it    |
| `aerich migrate`    | Generate a migration file for model changes |
| `aerich upgrade`    | Apply all pending migrations to the database |
| `aerich downgrade`  | Roll back the last migration               |
| `aerich history`    | Show the migration history                 |

---

### **Example: Running in FastAPI**
Ensure Tortoise-ORM initializes when your FastAPI app starts.

**`src/main.py`**
```python
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from src.database.config import TORTOISE_ORM

app = FastAPI()

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=False,  # Do not auto-generate schemas; use migrations
    add_exception_handlers=True,
)

@app.get("/")
async def root():
    return {"message": "Hello, FastAPI with Tortoise-ORM!"}
```

---
