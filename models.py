from main import db
from flask_login import UserMixin
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String


class ModDem(db.Model):
    __tablename__ = "ModDem"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    serial_number: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    udid: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    asset_id: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    cover_tag: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    location: Mapped[str] = mapped_column(String, nullable=True)
    technician: Mapped[str] = mapped_column(String, nullable=True)
    time_scanned: Mapped[str] = mapped_column(String, nullable=True)
    owner: Mapped[str] = mapped_column(String, nullable=True)
    returned: Mapped[str] = mapped_column(String, nullable=True)


# Create a User table for all your registered users
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(100), unique=True)