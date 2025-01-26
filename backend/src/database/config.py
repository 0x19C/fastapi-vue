import os


TORTOISE_ORM = {
    "connections": {"default": os.environ.get("DATABASE_URL", "mysql://root@localhost:3306/corpy_test")},
    "apps": {
        "models": {
            "models": [
                "src.database.models", "aerich.models"
            ],
            "default_connection": "default"
        }
    }
}
