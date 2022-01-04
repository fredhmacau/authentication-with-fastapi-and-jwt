from schema_db import db
from bcrypt import checkpw


class Verificator:
    async def authenticate_user(self, username: str, password: str) -> bool:
        db.connect()
        query = "SELECT id,username,password_hash from users where username=:username"
        user = await db.fetch_one(
            query, values={"username": str(username).strip().lower()}
        )
        if not user:
            return False
        if not self.__verify_password(password, user.password_hash):
            return False
        return user

    def __verify_password(self, password: str, hash_password):
        return checkpw(password.encode("utf-8"), hash_password)

    @classmethod
    async def select_user(self, id):

        query = "SELECT * FROM users where id=:id"
        user = await db.fetch_one(query, values={"id": id})
        return user
