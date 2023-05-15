from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()


# class AuthTokenTable(db.Model):
#     id = db.Column(db.Integer(), primary_key = True)
#     generated_datetime = db.Column(db.DateTime, nullable=False)
#     auth_token = db.Column(db.String(), nullable=False)
#     status = db.Column(db.Float(), nullable=False)

#     def __init__(self, auth_token, status) -> None:
#         self.generated_datetime = datetime.now()
#         self.auth_token = auth_token
#         self.status = status


class GeneratedSchedules(db.Model):
    pass