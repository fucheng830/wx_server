# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import redis 

# SQLALCHEMY_DATABASE_URL should be in the format:
# dialect+driver://username:password@host:port/database
# For a simple PostgreSQL connection, it might look like this:
SQLALCHEMY_DATABASE_URL = os.environ["SQLALCHEMY_DATABASE_URL"]

# Create an engine
# echo=True will print all the SQL statements, which is useful for debugging.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    # echo=True,
)

# Each instance of the SessionLocal class will be a database session. 
# The class itself is not a database session yet.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise 
    finally:
        db.close()

REDIS_URL = os.environ.get("REDIS_URL") or "redis://localhost:6379/0"

redis_conn = redis.from_url(REDIS_URL)  # 创建一个 Redis 对象，代表一个连接池

def get_redis_conn():
    return redis_conn  # 直接返回同一个 Redis 对象

