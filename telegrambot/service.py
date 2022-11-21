import psycopg2
import os
from sqlalchemy import create_engine, Column, Integer, Boolean, String
from sqlalchemy.orm import scoped_session, declarative_base, sessionmaker
from sqlalchemy.exc import PendingRollbackError, IntegrityError

# host = str(os.getenv("HOST"))
# password = str(os.getenv("PASSWORD"))
# database = str(os.getenv("DATABASE"))

HOST = "localhost"
PASSWORD = "postgres"
DATABASE = "youtube_bot"

host = HOST
password = PASSWORD
database = DATABASE

engine = create_engine(f"postgresql+psycopg2://postgres:{password}@{host}/{database}")
session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = session.query_property()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    name = Column(String)
    admin = Column(Boolean, default=False)


Base.metadata.create_all(bind=engine)


def register_user(message):
    username = message.from_user.username if message.from_user.username else None
    user = User(id=int(message.from_user.id), username=username, name=message.from_user.full_name)

    session.add(user)

    try:
        session.commit()
        return True
    except IntegrityError:
        session.rollback()  # откатываем session.add(user)
        return False


def select_user(user_id):
    user = session.query(User).filter(User.id == user_id).first()
    return user


def select_all_users():
    users = session.query(User).all()
    for user in users:
        return user.name


def broadcast(message):
    users = session.query(User).all()
    for user in users:
        return f'Dear {user.name} there is news for you.\n{message.replace("broadcast", "🆘")}'
