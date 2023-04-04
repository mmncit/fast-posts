# fast-posts

Minimal Post Management System using FastAPI, SQLAlchemy, PostgresDB

## Local Setup:

1.0. Create a virtual environment (optional)

```
python3 -m venv venv
```

- Update python interpreter to venv

- Activate venv for command line

```
source venv/bin/activate
```

1.1. Go inside api directory

```
cd api
```

2. Install python packages

```
make install
```

3. Create .env file containing credentials:

```
# for database connection
export DATABASE=<database name>
export DB_USER=<database username>
export DB_HOST=<hostname, e.g. localhost>
export DB_PASSWORD=<database password>
export DB_URL=<database url>

# for jwt
export SECRET_KEY=<secret pass>
export ALGORITHM=<hashing algorithm>
export ACCESS_TOKEN_EXPIRE_MINUTES=<time to expire access token>

```

Apply environment variables

```

source .env

```

4. Finally, run command using `make`

If `make` is not installed. Then

```
brew install make
```

Run the server implemented with raw SQL with:

```
make run-sql

```

Run the server implemented with Object Relational Mapper (ORM) SQLAlchemy with:

```

make run-orm

```
