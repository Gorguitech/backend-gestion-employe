# app/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Forcer l'encodage UTF-8 pour éviter les erreurs de décodage
os.environ['PGCLIENTENCODING'] = 'UTF8'

#  PostgreSQL  en local
# SQLALCHEMY_DATABASE_URL = "postgresql://admin:admin123@localhost:5432/dbdit"

# Postgres conteneurise
SQLALCHEMY_DATABASE_URL = "postgresql://admin:admin123@db-service:5432/dbprod"

#  PostgreSQL  en deploiement avec Docker Compose
# SQLALCHEMY_DATABASE_URL = "postgresql://admin:admin123@db-service:5432/dbemploye"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 

    connect_args={
        "client_encoding": "utf8",
        "options": "-c client_encoding=utf8"
    },
    pool_pre_ping=True

)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()