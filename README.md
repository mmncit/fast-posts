# fast-posts

Minimal Post Management System using FastAPI, SQLAlchemy, PostgresDB

## Setup:

1. Create a virtual environment

```
python3 -m venv venv
```

2. Update python interpreter to venv

3. Activate venv for command line

```
source venv/bin/activate
```

4. Install python packages

```
pip install -r requirements_dev.txt # install the packages
pip freeze # to check the installed packages
```

5. Create .env file containing credentials:

```

export DATABASE=<database name>
export DB_USER=<database username>
export DB_HOST=<hostname, e.g. localhost>
export DB_PASSWORD=<database password>
export DB_URL=<database url>

```

6. Apply environment variables

```

source .env

```

Finally,

Run the server implemented with raw SQL with:

```

uvicorn api.sql.main:app --reload

```

Run the server implemented with Object Relational Mapper (ORM) SQLAlchemy with:

```

uvicorn api.orm.main:app --reload

```
