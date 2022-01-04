from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base, sessionmaker
from databases import Database


connection_string = "sqlite:///store.db"
Base = declarative_base()
engine = create_engine(connection_string, encoding="utf8", echo=True)
db = Database(connection_string)
Session = sessionmaker(bind=engine)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="id user")
    username = Column(String(length=80), nullable=False, comment="name user")
    password_hash = Column(String(140), nullable=False, comment="password hash user")

    def __str__(self) -> str:
        return f"<User username={self.username}>"


session = Session()


if __name__ == "__main__":
    Base.metadata.create_all(engine)
