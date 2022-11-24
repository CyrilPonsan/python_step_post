from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQL_ALCHEMY_DATABASE_URL = "mariadb+mariadbconnector://rv8aj31m6t16iarg:f93k9g2wvjz7ax4b@f80b6byii2vwv8cx.chr7pe7iynqr.eu-west-1.rds.amazonaws.com/n52wztum9ono7zpr"
engine = create_engine(SQL_ALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# hello commentaire