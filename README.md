# Build Services

```
cp .env-docker .env
docker-compose up -d
```

# DB Migrate

### DB Create
```
docker exec -it corpy_backend python src/database/ensure_db.py
```

### DB Migrate
```
docker exec -it corpy_backend aerich upgrade
```

