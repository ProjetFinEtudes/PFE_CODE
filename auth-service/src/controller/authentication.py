from sqlalchemy.orm import Session


from schemas.authSchema import AuthSchema
from schemas.userSchema import UserSchema

class Authentication:

    def get_user_info_by_email(self, email: str, db: Session):
        auth_entry = db.query(AuthSchema).filter_by(email=email).first()
        if auth_entry:
            user_entry = db.query(UserSchema).filter_by(uid=auth_entry.uid).first()

            if user_entry:
                return user_entry

        return None