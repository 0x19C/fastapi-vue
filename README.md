# Build Services

If you want to change Service hosts or ports, please edit on .env-docker file.

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

### DB Seed
```
docker exec -it corpy_backend python src/database/seed.py
```
